/**
 * Encrypted Keystore
 * 
 * Provides AES-256-GCM encryption for wallet private keys.
 * Designed for AI-only access to wallet credentials.
 */

import * as crypto from 'crypto';

export interface EncryptedData {
  iv: string;        // Initialization vector (base64)
  authTag: string;   // Authentication tag (base64)
  data: string;      // Encrypted data (base64)
  algorithm: string; // Encryption algorithm used
}

export interface KeystoreEntry {
  chain: string;
  address: string;
  publicKey: string;
  encrypted: EncryptedData;
  createdAt: string;
  updatedAt: string;
}

export interface Keystore {
  version: string;
  createdAt: string;
  updatedAt: string;
  entries: KeystoreEntry[];
}

const ALGORITHM = 'aes-256-gcm';
const IV_LENGTH = 16;
const AUTH_TAG_LENGTH = 16;
const KEY_LENGTH = 32; // 256 bits

/**
 * Derive encryption key from password/secret
 */
export function deriveKey(secret: string, salt?: string): Buffer {
  const actualSalt = salt || 'asi-bor-wallet-salt';
  return crypto.pbkdf2Sync(secret, actualSalt, 100000, KEY_LENGTH, 'sha256');
}

/**
 * Encrypt data using AES-256-GCM
 */
export function encrypt(data: string, encryptionKey: Buffer): EncryptedData {
  // Generate random IV
  const iv = crypto.randomBytes(IV_LENGTH);
  
  // Create cipher
  const cipher = crypto.createCipheriv(ALGORITHM, encryptionKey, iv);
  
  // Encrypt data
  let encrypted = cipher.update(data, 'utf8', 'base64');
  encrypted += cipher.final('base64');
  
  // Get auth tag
  const authTag = cipher.getAuthTag();
  
  return {
    iv: iv.toString('base64'),
    authTag: authTag.toString('base64'),
    data: encrypted,
    algorithm: ALGORITHM,
  };
}

/**
 * Decrypt data using AES-256-GCM
 */
export function decrypt(encrypted: EncryptedData, encryptionKey: Buffer): string {
  // Parse IV and auth tag
  const iv = Buffer.from(encrypted.iv, 'base64');
  const authTag = Buffer.from(encrypted.authTag, 'base64');
  
  // Create decipher
  const decipher = crypto.createDecipheriv(ALGORITHM, encryptionKey, iv);
  decipher.setAuthTag(authTag);
  
  // Decrypt data
  let decrypted = decipher.update(encrypted.data, 'base64', 'utf8');
  decrypted += decipher.final('utf8');
  
  return decrypted;
}

/**
 * Create a new keystore
 */
export function createKeystore(): Keystore {
  const now = new Date().toISOString();
  return {
    version: '1.0',
    createdAt: now,
    updatedAt: now,
    entries: [],
  };
}

/**
 * Add an entry to the keystore
 */
export function addEntry(
  keystore: Keystore,
  chain: string,
  address: string,
  publicKey: string,
  privateKey: string,
  encryptionKey: Buffer
): Keystore {
  const now = new Date().toISOString();
  
  const entry: KeystoreEntry = {
    chain,
    address,
    publicKey,
    encrypted: encrypt(privateKey, encryptionKey),
    createdAt: now,
    updatedAt: now,
  };
  
  return {
    ...keystore,
    updatedAt: now,
    entries: [...keystore.entries, entry],
  };
}

/**
 * Get an entry from the keystore
 */
export function getEntry(
  keystore: Keystore,
  chain: string,
  address: string
): KeystoreEntry | undefined {
  return keystore.entries.find(
    (e) => e.chain === chain && e.address === address
  );
}

/**
 * Get decrypted private key from entry
 */
export function getPrivateKey(
  entry: KeystoreEntry,
  encryptionKey: Buffer
): string {
  return decrypt(entry.encrypted, encryptionKey);
}

/**
 * Serialize keystore to JSON
 */
export function serializeKeystore(keystore: Keystore): string {
  return JSON.stringify(keystore, null, 2);
}

/**
 * Deserialize keystore from JSON
 */
export function deserializeKeystore(json: string): Keystore {
  const parsed = JSON.parse(json);
  
  // Validate version
  if (!parsed.version || !parsed.entries) {
    throw new Error('Invalid keystore format');
  }
  
  return parsed as Keystore;
}

/**
 * Remove an entry from the keystore
 */
export function removeEntry(
  keystore: Keystore,
  chain: string,
  address: string
): Keystore {
  return {
    ...keystore,
    updatedAt: new Date().toISOString(),
    entries: keystore.entries.filter(
      (e) => !(e.chain === chain && e.address === address)
    ),
  };
}

/**
 * List all addresses in the keystore
 */
export function listAddresses(keystore: Keystore): { chain: string; address: string }[] {
  return keystore.entries.map((e) => ({
    chain: e.chain,
    address: e.address,
  }));
}

/**
 * Validate encryption key format
 */
export function validateEncryptionKey(key: string): boolean {
  // Should be 64 hex characters (32 bytes)
  return /^[a-fA-F0-9]{64}$/.test(key);
}

/**
 * Generate a random encryption key
 */
export function generateEncryptionKey(): string {
  return crypto.randomBytes(KEY_LENGTH).toString('hex');
}
