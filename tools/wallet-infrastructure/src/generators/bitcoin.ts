/**
 * Bitcoin HD Wallet Generator
 * 
 * Generates hierarchical deterministic (HD) wallets following BIP39/BIP32/BIP44.
 * Uses the derivation path m/44'/0'/0'/0/0 for Bitcoin mainnet.
 * 
 * Security: Private keys should never be exposed to humans in production.
 */

import * as bip39 from 'bip39';
import HDKey from 'hdkey';
import * as bitcoin from 'bitcoinjs-lib';

export interface BitcoinWallet {
  address: string;
  publicKey: string;
  privateKey: string;  // WIF format
  derivationPath: string;
}

export interface BitcoinHDWallet {
  mnemonic: string;
  masterPublicKey: string;
  wallets: BitcoinWallet[];
}

/**
 * Bitcoin derivation paths
 */
export const DERIVATION_PATHS = {
  // BIP44 - Legacy (P2PKH) - addresses start with 1
  BIP44: "m/44'/0'/0'/0",
  // BIP49 - SegWit compatible (P2SH-P2WPKH) - addresses start with 3
  BIP49: "m/49'/0'/0'/0",
  // BIP84 - Native SegWit (P2WPKH) - addresses start with bc1q
  BIP84: "m/84'/0'/0'/0",
} as const;

/**
 * Generate a new BIP39 mnemonic phrase
 */
export function generateMnemonic(strength: 128 | 256 = 256): string {
  return bip39.generateMnemonic(strength);
}

/**
 * Validate a BIP39 mnemonic phrase
 */
export function validateMnemonic(mnemonic: string): boolean {
  return bip39.validateMnemonic(mnemonic);
}

/**
 * Convert mnemonic to seed
 */
export async function mnemonicToSeed(mnemonic: string, passphrase = ''): Promise<Buffer> {
  return bip39.mnemonicToSeed(mnemonic, passphrase);
}

/**
 * Generate HD wallet from seed
 */
export function createHDWallet(seed: Buffer): HDKey {
  return HDKey.fromMasterSeed(seed);
}

/**
 * Derive a child wallet from HD wallet
 */
export function deriveWallet(
  hdWallet: HDKey,
  derivationPath: string,
  index: number = 0
): BitcoinWallet {
  const path = `${derivationPath}/${index}`;
  const child = hdWallet.derive(path);
  
  if (!child.privateKey) {
    throw new Error('Failed to derive private key');
  }
  
  // Create key pair for address generation
  const keyPair = bitcoin.ECPair.fromPrivateKey(child.privateKey);
  
  // Generate Native SegWit (bech32) address
  const { address } = bitcoin.payments.p2wpkh({
    pubkey: keyPair.publicKey,
    network: bitcoin.networks.bitcoin,
  });
  
  if (!address) {
    throw new Error('Failed to generate address');
  }
  
  return {
    address,
    publicKey: child.publicKey.toString('hex'),
    privateKey: keyPair.toWIF(),
    derivationPath: path,
  };
}

/**
 * Generate a complete Bitcoin HD wallet with multiple addresses
 */
export async function generateBitcoinHDWallet(
  count: number = 1,
  passphrase: string = ''
): Promise<BitcoinHDWallet> {
  // Generate mnemonic
  const mnemonic = generateMnemonic();
  
  // Convert to seed
  const seed = await mnemonicToSeed(mnemonic, passphrase);
  
  // Create HD wallet
  const hdWallet = createHDWallet(seed);
  
  // Derive wallets using BIP84 (Native SegWit)
  const wallets: BitcoinWallet[] = [];
  for (let i = 0; i < count; i++) {
    wallets.push(deriveWallet(hdWallet, DERIVATION_PATHS.BIP84, i));
  }
  
  return {
    mnemonic,
    masterPublicKey: hdWallet.publicExtendedKey,
    wallets,
  };
}

/**
 * Restore wallet from mnemonic
 */
export async function restoreBitcoinWallet(
  mnemonic: string,
  count: number = 1,
  passphrase: string = ''
): Promise<BitcoinHDWallet> {
  if (!validateMnemonic(mnemonic)) {
    throw new Error('Invalid mnemonic phrase');
  }
  
  const seed = await mnemonicToSeed(mnemonic, passphrase);
  const hdWallet = createHDWallet(seed);
  
  const wallets: BitcoinWallet[] = [];
  for (let i = 0; i < count; i++) {
    wallets.push(deriveWallet(hdWallet, DERIVATION_PATHS.BIP84, i));
  }
  
  return {
    mnemonic,
    masterPublicKey: hdWallet.publicExtendedKey,
    wallets,
  };
}

/**
 * Get public-only wallet info (safe to share)
 */
export function getPublicWalletInfo(wallet: BitcoinWallet): Omit<BitcoinWallet, 'privateKey'> {
  const { privateKey, ...publicInfo } = wallet;
  return publicInfo;
}
