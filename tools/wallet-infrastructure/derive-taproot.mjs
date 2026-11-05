#!/usr/bin/env node
/**
 * derive-taproot.mjs — Derive the BIP86 Taproot address from the treasury mnemonic
 *
 * BIP86 path: m/86'/0'/0'/0/0
 * This gives us a bc1p... address from the same seed as our bc1q... treasury.
 *
 * SECURITY: By default the mnemonic is typed at a hidden prompt and never read
 *   from disk. Reading TREASURY_MNEMONIC from .env is opt-in (--from-env-file)
 *   and refused unless the file is owner-only (chmod 600).
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
const FROM_ENV_FILE = process.argv.includes('--from-env-file');

function loadMnemonicFromEnvFile() {
  if (!fs.existsSync(ENV_PATH)) {
    throw new Error(`.env file not found at ${ENV_PATH}`);
  }
  const mode = fs.statSync(ENV_PATH).mode & 0o777;
  if (mode & 0o077) {
    throw new Error(`Refusing to read ${ENV_PATH}: permissions ${mode.toString(8)} allow other users. Run: chmod 600 ${ENV_PATH}`);
  }
  const envContent = fs.readFileSync(ENV_PATH, 'utf8');
  const match = envContent.match(/TREASURY_MNEMONIC="([^"]+)"/);
  if (!match) {
    throw new Error('TREASURY_MNEMONIC not found in .env');
  }
  return match[1];
}

function promptHidden(question) {
  return new Promise((resolve, reject) => {
    if (!process.stdin.isTTY) {
      reject(new Error('No terminal for hidden prompt. Run interactively, or pass --from-env-file.'));
      return;
    }
    process.stdout.write(question);
    const stdin = process.stdin;
    stdin.setRawMode(true);
    stdin.resume();
    stdin.setEncoding('utf8');
    let input = '';
    const onData = (ch) => {
      if (ch === '\r' || ch === '\n' || ch === '\u0004') {
        stdin.setRawMode(false);
        stdin.pause();
        stdin.removeListener('data', onData);
        process.stdout.write('\n');
        resolve(input.trim().replace(/\s+/g, ' '));
      } else if (ch === '\u0003') {
        stdin.setRawMode(false);
        process.exit(130);
      } else if (ch === '\u007f' || ch === '\b') {
        input = input.slice(0, -1);
      } else {
        input += ch;
      }
    };
    stdin.on('data', onData);
  });
}

async function loadMnemonic() {
  if (FROM_ENV_FILE) return loadMnemonicFromEnvFile();
  return promptHidden('Treasury mnemonic (input hidden): ');
}

const mnemonic = await loadMnemonic();
if (!bip39.validateMnemonic(mnemonic)) {
  console.error('Invalid mnemonic');
  process.exit(1);
}

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
