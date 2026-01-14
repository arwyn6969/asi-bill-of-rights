/**
 * Solana Wallet Generator
 * 
 * Generates Solana wallets using ed25519 keys derived from BIP39 mnemonic.
 * Uses the derivation path m/44'/501'/0'/0' for Solana.
 * 
 * Note: Solana uses a different key derivation than Bitcoin/Ethereum.
 * We use the standard Solana derivation which produces ed25519 keys.
 */

import * as bip39 from 'bip39';
import { derivePath } from 'ed25519-hd-key';
import nacl from 'tweetnacl';
import bs58 from 'bs58';

export interface SolanaWallet {
  address: string;           // Base58 public key
  publicKey: string;         // Hex public key
  privateKey: string;        // Base58 secret key (64 bytes)
  derivationPath: string;
}

export interface SolanaHDWallet {
  mnemonic: string;
  wallets: SolanaWallet[];
}

/**
 * Solana derivation path (BIP44)
 * m/44'/501'/account'/change'
 */
export const SOLANA_DERIVATION_PATH = "m/44'/501'/0'/0'";

/**
 * Derive Solana wallet from seed
 */
export function deriveSolanaWallet(
  seed: Buffer,
  derivationPath: string = SOLANA_DERIVATION_PATH
): SolanaWallet {
  // Derive ed25519 key from seed using the path
  const derived = derivePath(derivationPath, seed.toString('hex'));
  
  // Create keypair from derived seed
  const keypair = nacl.sign.keyPair.fromSeed(derived.key);
  
  // Solana address is the base58-encoded public key
  const address = bs58.encode(keypair.publicKey);
  
  // Secret key in Solana is 64 bytes (32 byte private + 32 byte public)
  const secretKey = bs58.encode(keypair.secretKey);
  
  return {
    address,
    publicKey: Buffer.from(keypair.publicKey).toString('hex'),
    privateKey: secretKey,
    derivationPath,
  };
}

/**
 * Generate a new Solana HD wallet
 */
export async function generateSolanaHDWallet(
  count: number = 1,
  passphrase: string = ''
): Promise<SolanaHDWallet> {
  // Generate mnemonic
  const mnemonic = bip39.generateMnemonic(256);
  
  // Convert to seed
  const seed = await bip39.mnemonicToSeed(mnemonic, passphrase);
  
  const wallets: SolanaWallet[] = [];
  for (let i = 0; i < count; i++) {
    const path = `m/44'/501'/${i}'/0'`;
    wallets.push(deriveSolanaWallet(seed, path));
  }
  
  return {
    mnemonic,
    wallets,
  };
}

/**
 * Restore Solana wallet from mnemonic
 */
export async function restoreSolanaWallet(
  mnemonic: string,
  count: number = 1,
  passphrase: string = ''
): Promise<SolanaHDWallet> {
  if (!bip39.validateMnemonic(mnemonic)) {
    throw new Error('Invalid mnemonic phrase');
  }
  
  const seed = await bip39.mnemonicToSeed(mnemonic, passphrase);
  
  const wallets: SolanaWallet[] = [];
  for (let i = 0; i < count; i++) {
    const path = `m/44'/501'/${i}'/0'`;
    wallets.push(deriveSolanaWallet(seed, path));
  }
  
  return {
    mnemonic,
    wallets,
  };
}

/**
 * Get public wallet info (safe to share)
 */
export function getPublicWalletInfo(wallet: SolanaWallet): Omit<SolanaWallet, 'privateKey'> {
  const { privateKey, ...publicInfo } = wallet;
  return publicInfo;
}
