/**
 * Arweave Wallet Generator
 * 
 * Generates Arweave wallets using arweave-js.
 * Arweave uses RSA-PSS 4096-bit keys stored in JWK format.
 * 
 * Security: JWK private keys should never be exposed to humans in production.
 */

import Arweave from 'arweave';
import { JWKInterface } from 'arweave/node/lib/wallet';

export interface ArweaveWallet {
  address: string;
  publicKey: string;  // n component of JWK
  jwk: JWKInterface;  // Full JWK (private + public)
}

export interface ArweavePublicWallet {
  address: string;
  publicKey: string;
}

/**
 * Initialize Arweave client
 */
export function createArweaveClient(
  host: string = 'arweave.net',
  port: number = 443,
  protocol: string = 'https'
): Arweave {
  return Arweave.init({
    host,
    port,
    protocol,
  });
}

/**
 * Generate a new Arweave wallet
 * 
 * @param arweave - Arweave client instance
 * @returns Promise resolving to ArweaveWallet
 */
export async function generateArweaveWallet(
  arweave?: Arweave
): Promise<ArweaveWallet> {
  const client = arweave || createArweaveClient();
  
  // Generate new JWK key pair
  const jwk = await client.wallets.generate();
  
  // Get wallet address from JWK
  const address = await client.wallets.jwkToAddress(jwk);
  
  return {
    address,
    publicKey: jwk.n,  // RSA modulus (public key component)
    jwk,
  };
}

/**
 * Restore wallet from JWK
 */
export async function restoreFromJWK(
  jwk: JWKInterface,
  arweave?: Arweave
): Promise<ArweaveWallet> {
  const client = arweave || createArweaveClient();
  const address = await client.wallets.jwkToAddress(jwk);
  
  return {
    address,
    publicKey: jwk.n,
    jwk,
  };
}

/**
 * Get wallet balance in AR
 */
export async function getBalance(
  address: string,
  arweave?: Arweave
): Promise<string> {
  const client = arweave || createArweaveClient();
  const winston = await client.wallets.getBalance(address);
  return client.ar.winstonToAr(winston);
}

/**
 * Get wallet balance in Winston (smallest unit)
 */
export async function getBalanceWinston(
  address: string,
  arweave?: Arweave
): Promise<string> {
  const client = arweave || createArweaveClient();
  return client.wallets.getBalance(address);
}

/**
 * Sign data with the wallet
 */
export async function signData(
  jwk: JWKInterface,
  data: Uint8Array,
  arweave?: Arweave
): Promise<Uint8Array> {
  const client = arweave || createArweaveClient();
  return client.crypto.sign(jwk, data);
}

/**
 * Create and sign a transaction
 */
export async function createTransaction(
  jwk: JWKInterface,
  data: string | Uint8Array,
  arweave?: Arweave,
  tags?: { name: string; value: string }[]
): Promise<{
  id: string;
  signedTransaction: any;
}> {
  const client = arweave || createArweaveClient();
  
  // Create transaction
  const transaction = await client.createTransaction({
    data: typeof data === 'string' ? data : data,
  }, jwk);
  
  // Add tags if provided
  if (tags) {
    for (const tag of tags) {
      transaction.addTag(tag.name, tag.value);
    }
  }
  
  // Sign transaction
  await client.transactions.sign(transaction, jwk);
  
  return {
    id: transaction.id,
    signedTransaction: transaction,
  };
}

/**
 * Post a signed transaction
 */
export async function postTransaction(
  signedTransaction: any,
  arweave?: Arweave
): Promise<{ status: number; statusText: string }> {
  const client = arweave || createArweaveClient();
  const response = await client.transactions.post(signedTransaction);
  return {
    status: response.status,
    statusText: response.statusText,
  };
}

/**
 * Get public-only wallet info (safe to share)
 */
export function getPublicWalletInfo(wallet: ArweaveWallet): ArweavePublicWallet {
  return {
    address: wallet.address,
    publicKey: wallet.publicKey,
  };
}

/**
 * Validate an Arweave address format
 */
export function isValidAddress(address: string): boolean {
  // Arweave addresses are 43 characters, base64url encoded
  return /^[a-zA-Z0-9_-]{43}$/.test(address);
}

/**
 * Convert JWK to base64 string for storage
 */
export function jwkToBase64(jwk: JWKInterface): string {
  return Buffer.from(JSON.stringify(jwk)).toString('base64');
}

/**
 * Convert base64 string back to JWK
 */
export function base64ToJWK(base64: string): JWKInterface {
  return JSON.parse(Buffer.from(base64, 'base64').toString('utf-8'));
}
