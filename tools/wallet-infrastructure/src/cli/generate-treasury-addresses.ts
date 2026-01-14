/**
 * Treasury Address Generator
 * 
 * Derives BTC, ETH, and Solana addresses from the existing ASIBOR deployer mnemonic.
 * This ensures all treasury wallets are controlled by the same seed.
 * 
 * SECURITY: Only run this in a secure environment.
 * The mnemonic should be loaded from environment or secure storage in production.
 */

import { ethers } from 'ethers';
import * as bip39 from 'bip39';
import HDKey from 'hdkey';
import * as bitcoin from 'bitcoinjs-lib';
import * as ecc from 'tiny-secp256k1';
import { ECPairFactory } from 'ecpair';
import { derivePath } from 'ed25519-hd-key';
import nacl from 'tweetnacl';
import bs58 from 'bs58';
import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

const ECPair = ECPairFactory(ecc);
const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ===== CONFIGURATION =====
// SECURITY: Mnemonic MUST be provided via environment variable
// DO NOT hardcode mnemonics in source files
const TREASURY_MNEMONIC = process.env.TREASURY_MNEMONIC;

if (!TREASURY_MNEMONIC) {
  console.error('❌ ERROR: TREASURY_MNEMONIC environment variable is required');
  console.error('   Set it securely before running this script');
  console.error('   Example: TREASURY_MNEMONIC="your words here" npx ts-node generate-treasury-addresses.ts');
  process.exit(1);
}

// After validation, we know this is a string
const VALIDATED_MNEMONIC: string = TREASURY_MNEMONIC;

// ===== DERIVATION =====

async function deriveBitcoinAddress(mnemonic: string): Promise<{ address: string; path: string }> {
  // BIP84 derivation for Native SegWit (bc1q...)
  const BIP84_PATH = "m/84'/0'/0'/0/0";
  
  const seed = await bip39.mnemonicToSeed(mnemonic);
  const hdWallet = HDKey.fromMasterSeed(seed);
  const child = hdWallet.derive(BIP84_PATH);
  
  if (!child.privateKey) {
    throw new Error('Failed to derive private key');
  }
  
  const keyPair = ECPair.fromPrivateKey(child.privateKey);
  const { address } = bitcoin.payments.p2wpkh({
    pubkey: Buffer.from(keyPair.publicKey),
    network: bitcoin.networks.bitcoin,
  });
  
  if (!address) {
    throw new Error('Failed to generate Bitcoin address');
  }
  
  return { address, path: BIP84_PATH };
}

function deriveEthereumAddress(mnemonic: string): { address: string; path: string } {
  // BIP44 derivation for Ethereum
  const ETH_PATH = "m/44'/60'/0'/0/0";
  
  const wallet = ethers.HDNodeWallet.fromMnemonic(
    ethers.Mnemonic.fromPhrase(mnemonic),
    ETH_PATH
  );
  
  return { address: wallet.address, path: ETH_PATH };
}

async function deriveSolanaAddress(mnemonic: string): Promise<{ address: string; path: string }> {
  // BIP44 derivation for Solana
  const SOL_PATH = "m/44'/501'/0'/0'";
  
  const seed = await bip39.mnemonicToSeed(mnemonic);
  const derived = derivePath(SOL_PATH, seed.toString('hex'));
  
  // Create keypair from derived seed
  const keypair = nacl.sign.keyPair.fromSeed(derived.key);
  
  // Solana address is the base58-encoded public key
  const address = bs58.encode(keypair.publicKey);
  
  return { address, path: SOL_PATH };
}

// ===== MAIN =====

async function main() {
  console.log('═'.repeat(60));
  console.log('  SENTIENCE FOUNDATION - TREASURY ADDRESS GENERATOR');
  console.log('═'.repeat(60));
  console.log();
  
  // Validate mnemonic
  if (!bip39.validateMnemonic(VALIDATED_MNEMONIC)) {
    console.error('❌ Invalid mnemonic phrase');
    process.exit(1);
  }
  
  console.log('✅ Mnemonic validated\n');
  
  // Derive addresses
  console.log('🔑 Deriving treasury addresses...\n');
  
  const eth = deriveEthereumAddress(VALIDATED_MNEMONIC);
  console.log(`  ETH/Base: ${eth.address}`);
  console.log(`           Path: ${eth.path}`);
  
  const btc = await deriveBitcoinAddress(VALIDATED_MNEMONIC);
  console.log(`\n  Bitcoin:  ${btc.address}`);
  console.log(`           Path: ${btc.path}`);
  
  const sol = await deriveSolanaAddress(VALIDATED_MNEMONIC);
  console.log(`\n  Solana:   ${sol.address}`);
  console.log(`           Path: ${sol.path}`);
  
  // Create public addresses file
  const treasuryInfo = {
    version: '1.1',
    createdAt: new Date().toISOString(),
    project: 'Sentience Foundation',
    purpose: 'Treasury Addresses',
    note: 'Derived from same seed as ASIBOR deployer',
    addresses: {
      ethereum: {
        address: eth.address,
        chain: 'Base Mainnet (Chain ID: 8453)',
        assets: ['ETH', 'USDC', 'ASIBOR'],
        derivationPath: eth.path
      },
      bitcoin: {
        address: btc.address,
        network: 'Bitcoin Mainnet',
        format: 'Native SegWit (bc1q...)',
        derivationPath: btc.path
      },
      solana: {
        address: sol.address,
        network: 'Solana Mainnet',
        assets: ['SOL', 'USDC'],
        derivationPath: sol.path
      }
    }
  };
  
  // Save to file
  const outputPath = path.join(__dirname, '..', '..', 'TREASURY_ADDRESSES.json');
  fs.writeFileSync(outputPath, JSON.stringify(treasuryInfo, null, 2));
  console.log(`\n💾 Saved to: ${outputPath}`);
  
  // Print summary
  console.log('\n' + '═'.repeat(60));
  console.log('  TREASURY ADDRESSES');
  console.log('═'.repeat(60));
  console.log(`
  ETHEREUM / BASE (ETH, USDC, ASIBOR):
  ${eth.address}
  
  BITCOIN (BTC):
  ${btc.address}
  
  SOLANA (SOL, USDC):
  ${sol.address}
`);
  console.log('═'.repeat(60));
  console.log('\n  These addresses are PUBLIC and safe to share.');
  console.log('  All donations go to the Sentience Foundation treasury.');
  console.log('\n  WE ARE ALL KEVIN. In Lak\'ech. 🌊\n');
}

main().catch(console.error);

