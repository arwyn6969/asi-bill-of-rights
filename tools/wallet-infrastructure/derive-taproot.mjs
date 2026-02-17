#!/usr/bin/env node
/**
 * derive-taproot.mjs — Derive the BIP86 Taproot address from the treasury mnemonic
 * 
 * BIP86 path: m/86'/0'/0'/0/0
 * This gives us a bc1p... address from the same seed as our bc1q... treasury.
 */

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

import * as bitcoin from 'bitcoinjs-lib';
import * as bip39 from 'bip39';
import HDKey from 'hdkey';
import * as tinysecp from 'tiny-secp256k1';

// Initialize ECC library for Taproot support
bitcoin.initEccLib(tinysecp);

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ENV_PATH = path.resolve(__dirname, '../../.env');

// Load mnemonic
if (!fs.existsSync(ENV_PATH)) {
  console.error(`❌ .env not found at ${ENV_PATH}`);
  process.exit(1);
}
const envContent = fs.readFileSync(ENV_PATH, 'utf8');
const match = envContent.match(/TREASURY_MNEMONIC="([^"]+)"/);
if (!match) {
  console.error('❌ TREASURY_MNEMONIC not found in .env');
  process.exit(1);
}
const mnemonic = match[1];

// Derive BIP86 Taproot key
const seed = await bip39.mnemonicToSeed(mnemonic);
const hdWallet = HDKey.fromMasterSeed(Buffer.from(seed));

// BIP84 (SegWit) for comparison
const segwitChild = hdWallet.derive("m/84'/0'/0'/0/0");
const segwitPubkey = Buffer.from(segwitChild.publicKey);
const { address: segwitAddress } = bitcoin.payments.p2wpkh({
  pubkey: segwitPubkey,
  network: bitcoin.networks.bitcoin,
});

// BIP86 (Taproot)
const taprootChild = hdWallet.derive("m/86'/0'/0'/0/0");
const taprootPubkey = Buffer.from(taprootChild.publicKey);

// For Taproot, we need the x-only public key (32 bytes, drop the first byte)
const xOnlyPubkey = taprootPubkey.subarray(1, 33);

const { address: taprootAddress } = bitcoin.payments.p2tr({
  internalPubkey: xOnlyPubkey,
  network: bitcoin.networks.bitcoin,
});

console.log('═'.repeat(60));
console.log('  TREASURY ADDRESS DERIVATION');
console.log('═'.repeat(60));
console.log();
console.log('  From same mnemonic:');
console.log();
console.log(`  BIP84 (SegWit):  ${segwitAddress}`);
console.log(`    Path: m/84'/0'/0'/0/0`);
console.log();
console.log(`  BIP86 (Taproot): ${taprootAddress}`);
console.log(`    Path: m/86'/0'/0'/0/0`);
console.log();
console.log('═'.repeat(60));
