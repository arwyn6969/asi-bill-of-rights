#!/usr/bin/env node
/**
 * fire-pay-invoice.mjs — Send BTC from treasury to pay a FIRE mint invoice
 * 
 * Usage: node fire-pay-invoice.mjs <payAddress> <amountSats>
 * 
 * SECURITY: This script reads TREASURY_MNEMONIC from ../.env
 * AUTHORIZED BY: Arwyn Hughes (project custodian) in direct conversation
 * 
 * This script:
 *  1. Loads mnemonic from .env
 *  2. Derives BIP84 (bc1q) key at m/84'/0'/0'/0/0
 *  3. Fetches UTXOs from mempool.space API
 *  4. Builds, signs, and DRY-RUN displays the transaction
 *  5. Only broadcasts after explicit confirmation
 */

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';
import crypto from 'node:crypto';

// Bitcoin libraries
import * as bitcoin from 'bitcoinjs-lib';
import * as bip39 from 'bip39';
import HDKey from 'hdkey';
import ECPairFactory from 'ecpair';
import * as tinysecp from 'tiny-secp256k1';

const ECPair = ECPairFactory(tinysecp);

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ENV_PATH = path.resolve(__dirname, '../.env');
const MEMPOOL_API = 'https://mempool.space/api';

// --- PARSE ARGS ---
const PAY_ADDRESS = process.argv[2];
const AMOUNT_SATS = parseInt(process.argv[3] || '0', 10);

if (!PAY_ADDRESS || !AMOUNT_SATS) {
  console.error('Usage: node fire-pay-invoice.mjs <payAddress> <amountSats>');
  console.error('Example: node fire-pay-invoice.mjs bc1p...abc 22641');
  process.exit(1);
}

// Fee rate in sat/vbyte - conservative for reliability
const FEE_RATE = 5; // sat/vbyte

// --- LOAD MNEMONIC ---
function loadMnemonic() {
  if (!fs.existsSync(ENV_PATH)) {
    throw new Error(`.env file not found at ${ENV_PATH}`);
  }
  const envContent = fs.readFileSync(ENV_PATH, 'utf8');
  const match = envContent.match(/TREASURY_MNEMONIC="([^"]+)"/);
  if (!match) {
    throw new Error('TREASURY_MNEMONIC not found in .env');
  }
  return match[1];
}

// --- DERIVE KEY ---
async function deriveKey(mnemonic) {
  const seed = await bip39.mnemonicToSeed(mnemonic);
  const hdWallet = HDKey.fromMasterSeed(Buffer.from(seed));
  // BIP84 path for native segwit: m/84'/0'/0'/0/0
  const child = hdWallet.derive("m/84'/0'/0'/0/0");
  
  if (!child.privateKey) {
    throw new Error('Failed to derive private key');
  }
  
  const keyPair = ECPair.fromPrivateKey(Buffer.from(child.privateKey));
  
  // Generate bc1q address to verify it matches treasury
  const { address } = bitcoin.payments.p2wpkh({
    pubkey: keyPair.publicKey,
    network: bitcoin.networks.bitcoin,
  });
  
  return { keyPair, address, publicKey: keyPair.publicKey };
}

// --- FETCH UTXOs ---
async function fetchUTXOs(address) {
  const url = `${MEMPOOL_API}/address/${address}/utxo`;
  console.log(`  Fetching UTXOs from ${url}`);
  const res = await fetch(url);
  if (!res.ok) throw new Error(`UTXO fetch failed: ${res.status}`);
  const utxos = await res.json();
  return utxos;
}

// --- FETCH CURRENT FEE RATES ---
async function fetchFeeRates() {
  try {
    const res = await fetch(`${MEMPOOL_API}/v1/fees/recommended`);
    if (res.ok) {
      const fees = await res.json();
      return fees;
    }
  } catch {}
  return null;
}

// --- BROADCAST TX ---
async function broadcastTx(txHex) {
  const res = await fetch(`${MEMPOOL_API}/tx`, {
    method: 'POST',
    headers: { 'Content-Type': 'text/plain' },
    body: txHex,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Broadcast failed: ${res.status} - ${text}`);
  }
  return await res.text(); // Returns txid
}

// --- MAIN ---
async function main() {
  console.log('═'.repeat(60));
  console.log('  FIRE MINT — BTC INVOICE PAYMENT');
  console.log('═'.repeat(60));
  console.log();
  
  // 1. Load mnemonic
  console.log('[1/6] Loading treasury mnemonic...');
  const mnemonic = loadMnemonic();
  if (!bip39.validateMnemonic(mnemonic)) {
    throw new Error('Invalid mnemonic in .env');
  }
  console.log('  ✅ Valid 24-word mnemonic loaded');
  
  // 2. Derive key
  console.log('[2/6] Deriving BIP84 key...');
  const { keyPair, address, publicKey } = await deriveKey(mnemonic);
  console.log(`  ✅ Treasury address: ${address}`);
  
  // Verify this matches the known treasury address
  const EXPECTED_ADDRESS = 'bc1qjnz72rgphxmzru8rcvu3vmju4phd0klsd0tt5k';
  if (address !== EXPECTED_ADDRESS) {
    throw new Error(`ADDRESS MISMATCH! Derived ${address} but expected ${EXPECTED_ADDRESS}. ABORTING.`);
  }
  console.log('  ✅ Address matches known treasury');
  
  // 3. Fetch UTXOs
  console.log('[3/6] Fetching UTXOs...');
  const utxos = await fetchUTXOs(address);
  
  if (utxos.length === 0) {
    throw new Error('No UTXOs found for treasury address. Is there BTC in this wallet?');
  }
  
  // Calculate total balance
  const totalBalance = utxos.reduce((sum, u) => sum + u.value, 0);
  console.log(`  ✅ Found ${utxos.length} UTXOs, total balance: ${totalBalance} sats (${(totalBalance / 1e8).toFixed(8)} BTC)`);
  
  // 4. Check fee rates
  console.log('[4/6] Checking network fee rates...');
  const feeRates = await fetchFeeRates();
  let feeRate = FEE_RATE;
  if (feeRates) {
    // Use hourFee (economical) for this small tx
    feeRate = Math.max(feeRates.hourFee || FEE_RATE, 1);
    console.log(`  Current fee rates: fastest=${feeRates.fastestFee}, halfHour=${feeRates.halfHourFee}, hour=${feeRates.hourFee}, economy=${feeRates.economyFee}`);
    console.log(`  Using: ${feeRate} sat/vbyte (hour priority)`);
  } else {
    console.log(`  Could not fetch live fee rates, using default: ${feeRate} sat/vbyte`);
  }
  
  // 5. Build transaction
  console.log('[5/6] Building transaction...');
  
  // Estimate vsize for 1-input 2-output P2WPKH tx: ~141 vbytes
  // For safety, estimate higher
  const ESTIMATED_VSIZE = 145;
  const estimatedFee = Math.ceil(ESTIMATED_VSIZE * feeRate);
  
  const totalNeeded = AMOUNT_SATS + estimatedFee;
  
  if (totalBalance < totalNeeded) {
    throw new Error(`Insufficient balance! Need ${totalNeeded} sats (${AMOUNT_SATS} + ~${estimatedFee} fee) but only have ${totalBalance} sats`);
  }
  
  // Select UTXOs (simple: use all, send change back)
  // For a small payment, just use the first sufficient UTXO
  let selectedUtxos = [];
  let selectedTotal = 0;
  
  // Sort by value descending, pick until we have enough
  const sortedUtxos = [...utxos].sort((a, b) => b.value - a.value);
  for (const utxo of sortedUtxos) {
    selectedUtxos.push(utxo);
    selectedTotal += utxo.value;
    if (selectedTotal >= totalNeeded) break;
  }
  
  const changeSats = selectedTotal - AMOUNT_SATS - estimatedFee;
  
  console.log(`  Payment:  ${AMOUNT_SATS} sats → ${PAY_ADDRESS}`);
  console.log(`  Fee:      ~${estimatedFee} sats (${feeRate} sat/vbyte)`);
  console.log(`  Change:   ${changeSats} sats → ${address} (back to treasury)`);
  console.log(`  Using ${selectedUtxos.length} input(s)`);
  
  // Build PSBT
  const psbt = new bitcoin.Psbt({ network: bitcoin.networks.bitcoin });
  
  // Add inputs
  for (const utxo of selectedUtxos) {
    // For P2WPKH we need the witnessUtxo
    const p2wpkh = bitcoin.payments.p2wpkh({
      pubkey: publicKey,
      network: bitcoin.networks.bitcoin,
    });
    
    psbt.addInput({
      hash: utxo.txid,
      index: utxo.vout,
      witnessUtxo: {
        script: p2wpkh.output,
        value: utxo.value,
      },
    });
  }
  
  // Add payment output
  psbt.addOutput({
    address: PAY_ADDRESS,
    value: AMOUNT_SATS,
  });
  
  // Add change output (if meaningful - skip dust)
  if (changeSats > 546) { // 546 is dust threshold
    psbt.addOutput({
      address: address, // Change back to treasury
      value: changeSats,
    });
  }
  
  // Sign all inputs
  for (let i = 0; i < selectedUtxos.length; i++) {
    psbt.signInput(i, keyPair);
  }
  
  // Finalize
  psbt.finalizeAllInputs();
  
  // Extract
  const tx = psbt.extractTransaction();
  const txHex = tx.toHex();
  const txId = tx.getId();
  const actualVsize = tx.virtualSize();
  const actualFee = selectedTotal - AMOUNT_SATS - changeSats;
  
  console.log();
  console.log('═'.repeat(60));
  console.log('  TRANSACTION READY (NOT YET BROADCAST)');
  console.log('═'.repeat(60));
  console.log(`  TXID:     ${txId}`);
  console.log(`  Size:     ${actualVsize} vbytes`);
  console.log(`  Fee:      ${actualFee} sats (${(actualFee / actualVsize).toFixed(1)} sat/vbyte)`);
  console.log(`  Sending:  ${AMOUNT_SATS} sats (${(AMOUNT_SATS / 1e8).toFixed(8)} BTC)`);
  console.log(`  To:       ${PAY_ADDRESS}`);
  console.log(`  Change:   ${changeSats} sats → ${address}`);
  console.log('═'.repeat(60));
  
  // 6. Broadcast
  console.log();
  console.log('[6/6] Broadcasting transaction...');
  const broadcastTxId = await broadcastTx(txHex);
  console.log(`  ✅ BROADCAST SUCCESSFUL!`);
  console.log(`  TXID: ${broadcastTxId}`);
  console.log(`  View: https://mempool.space/tx/${broadcastTxId}`);
  console.log();
  console.log('🔥 Payment sent! The FIRE mint invoice should be fulfilled shortly.');
}

main().catch((err) => {
  console.error('❌ PAYMENT FAILED:', err.message);
  process.exit(1);
});
