/**
 * Ethereum Wallet Generator
 * 
 * Generates Ethereum wallets using ethers.js.
 * Supports both random generation and HD derivation.
 * 
 * Security: Private keys should never be exposed to humans in production.
 */

import { ethers, HDNodeWallet, Mnemonic, Wallet } from 'ethers';

export interface EthereumWallet {
  address: string;
  publicKey: string;
  privateKey: string;
  derivationPath?: string;
}

export interface EthereumHDWallet {
  mnemonic: string;
  wallets: EthereumWallet[];
}

/**
 * Ethereum derivation path (BIP44)
 */
export const ETH_DERIVATION_PATH = "m/44'/60'/0'/0";

/**
 * Generate a random Ethereum wallet
 */
export function generateRandomWallet(): EthereumWallet {
  const wallet = Wallet.createRandom();
  
  return {
    address: wallet.address,
    publicKey: wallet.signingKey.publicKey,
    privateKey: wallet.privateKey,
  };
}

/**
 * Generate an Ethereum HD wallet with mnemonic
 */
export function generateEthereumHDWallet(count: number = 1): EthereumHDWallet {
  // Generate random mnemonic
  const mnemonic = Mnemonic.fromEntropy(ethers.randomBytes(32));
  
  const wallets: EthereumWallet[] = [];
  
  for (let i = 0; i < count; i++) {
    const path = `${ETH_DERIVATION_PATH}/${i}`;
    const wallet = HDNodeWallet.fromMnemonic(mnemonic, path);
    
    wallets.push({
      address: wallet.address,
      publicKey: wallet.signingKey.publicKey,
      privateKey: wallet.privateKey,
      derivationPath: path,
    });
  }
  
  return {
    mnemonic: mnemonic.phrase,
    wallets,
  };
}

/**
 * Restore Ethereum HD wallet from mnemonic
 */
export function restoreEthereumWallet(
  mnemonicPhrase: string,
  count: number = 1
): EthereumHDWallet {
  const mnemonic = Mnemonic.fromPhrase(mnemonicPhrase);
  
  const wallets: EthereumWallet[] = [];
  
  for (let i = 0; i < count; i++) {
    const path = `${ETH_DERIVATION_PATH}/${i}`;
    const wallet = HDNodeWallet.fromMnemonic(mnemonic, path);
    
    wallets.push({
      address: wallet.address,
      publicKey: wallet.signingKey.publicKey,
      privateKey: wallet.privateKey,
      derivationPath: path,
    });
  }
  
  return {
    mnemonic: mnemonicPhrase,
    wallets,
  };
}

/**
 * Create wallet from private key
 */
export function walletFromPrivateKey(privateKey: string): EthereumWallet {
  const wallet = new Wallet(privateKey);
  
  return {
    address: wallet.address,
    publicKey: wallet.signingKey.publicKey,
    privateKey: wallet.privateKey,
  };
}

/**
 * Sign a message with the wallet
 */
export async function signMessage(
  privateKey: string,
  message: string
): Promise<string> {
  const wallet = new Wallet(privateKey);
  return wallet.signMessage(message);
}

/**
 * Sign a transaction
 */
export async function signTransaction(
  privateKey: string,
  transaction: ethers.TransactionRequest
): Promise<string> {
  const wallet = new Wallet(privateKey);
  return wallet.signTransaction(transaction);
}

/**
 * Get public-only wallet info (safe to share)
 */
export function getPublicWalletInfo(wallet: EthereumWallet): Omit<EthereumWallet, 'privateKey'> {
  const { privateKey, ...publicInfo } = wallet;
  return publicInfo;
}

/**
 * Validate an Ethereum address
 */
export function isValidAddress(address: string): boolean {
  return ethers.isAddress(address);
}

/**
 * Get checksum address
 */
export function getChecksumAddress(address: string): string {
  return ethers.getAddress(address);
}
