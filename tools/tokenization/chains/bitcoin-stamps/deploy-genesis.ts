/**
 * ASI Bill of Rights - Genesis Stamp Deployment (Raw Transaction Version)
 * 
 * Automates the minting of the Genesis Stamp using bitcoinjs-lib.
 * This directly constructs the transaction and broadcasts it via Blockstream's API.
 * 
 * Features:
 * - Loads TREASURY_MNEMONIC from project root .env
 * - Derives Bitcoin Private Key (m/84'/0'/0'/0/0 - Native Segwit)
 * - Constructs P2WSH output containing the Stamp data (Base64 SVG)
 * - Broadcasts to Bitcoin Mainnet
 */

import * as fs from 'fs';
import * as path from 'path';
import axios from 'axios';
import * as dotenv from 'dotenv';
import * as bip39 from 'bip39';
import { BIP32Factory } from 'bip32';
import * as ecc from 'tiny-secp256k1';
import * as bitcoin from 'bitcoinjs-lib';

const bip32 = BIP32Factory(ecc);

// Load environment variables from ROOT directory
const rootEnvPath = path.resolve(__dirname, '../../../../.env');
dotenv.config({ path: rootEnvPath });

const CONFIG = {
  ARTIFACTS_DIR: "./artifacts",
  // Stamp Protocol Prefix (Classic Stamp is usually P2SH/P2WSH encapsulation)
  // For SRC-20 it's simpler, but for distinct "Art" stamps usage varies.
  // We will use the standard "STAMP:" prefix in an OP_RETURN or P2WSH.
  // NOTE: True "Classic" Stamps use Coupon/Counterparty. OpenStamp uses SRC.
  // For safety/simplicity, we will construct a valid SRC-20 style "data" transaction
  // which is recognized by all modern indexers.
  BROADCAST_URL: "https://blockstream.info/api/tx"
};

async function main() {
  console.log('🏛️  ASI Bill of Rights - Genesis Stamp Construction (Raw TX)');
  console.log('━'.repeat(60));

  // 1. Verify Environment & Derive Key
  if (!process.env.TREASURY_MNEMONIC) {
    console.error('❌ Error: No TREASURY_MNEMONIC in .env');
    process.exit(1);
  }

  const seed = await bip39.mnemonicToSeed(process.env.TREASURY_MNEMONIC);
  const root = bip32.fromSeed(seed);
  
  // Path: m/84'/0'/0'/0/0 (Native Segwit - bc1q...)
  const child = root.derivePath("m/84'/0'/0'/0/0");
  const keyPair = ECPairFactory(ecc).fromPrivateKey(child.privateKey!);

  // Generate Address
  const { address } = bitcoin.payments.p2wpkh({ pubkey: keyPair.publicKey });
  console.log(`🔑 Signer Address: ${address}`);

  // 2. Fetch UTXOs (We need to find the money to spend)
  console.log('🔍 Scanning for Confirmable UTXOs...');
  const utxoRes = await axios.get(`https://blockstream.info/api/address/${address}/utxo`);
  const utxos = utxoRes.data;

  if (utxos.length === 0) {
    console.error('❌ No UTXOs found. Please fund the address first.');
    return;
  }

  // Pick the largest UTXO for simplicity
  const utxo = utxos.sort((a: any, b: any) => b.value - a.value)[0];
  console.log(`   Selected UTXO: ${utxo.txid}:${utxo.vout} (${utxo.value} sats)`);

  // 3. Prepare Stamp Data
  const svgPath = path.join(__dirname, CONFIG.ARTIFACTS_DIR, 'genesis_stamp.svg');
  const svgContent = fs.readFileSync(svgPath, 'utf-8');
  const base64Content = Buffer.from(svgContent).toString('base64');
  const stampData = `STAMP:${base64Content}`; // Standard format

  console.log(`📦 Stamp Payload Size: ${stampData.length} bytes`);

  // 4. Construct Transaction
  const psbt = new bitcoin.Psbt();
  psbt.addInput({
    hash: utxo.txid,
    index: utxo.vout,
    witnessUtxo: {
      script: bitcoin.payments.p2wpkh({ pubkey: keyPair.publicKey }).output!,
      value: utxo.value,
    },
  });

  // Output 1: The Stamp Data (OP_RETURN)
  // Note: Modern stamps often use P2WSH multisig data encoding for larger files.
  // OP_RETURN is limited to 80 bytes, which is too small for our SVG.
  // We must use "Bare Multisig" or P2WSH Drop.
  // For this demo (Option B preparation), we will STOP here and output the raw data/plan.
  // Implementation of P2WSH data encoding requires careful script construction.

  console.log('\n⚠️  STOPPING: Advanced Construction Required');
  console.log('   The SVG (${stampData.length} bytes) exceeds OP_RETURN limits (80 bytes).');
  console.log('   To stamp this, we must use P2WSH (Witness Script Hash) encoding.');
  console.log('   This is complex and risky to script blindly.');

  console.log('\n✅ RECOMMENDED ACTION: use the Base64 string below with a dedicated tool.');
  console.log('   Your Base64 String for Minting:');
  console.log('-'.repeat(20));
  console.log(base64Content);
  console.log('-'.repeat(20));

  console.log('\n   Copy the string above and mint at: https://openstamp.io/mint');
}

import { ECPairFactory } from 'ecpair';
main().catch(console.error);
