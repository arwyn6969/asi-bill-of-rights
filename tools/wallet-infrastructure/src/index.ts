/**
 * Wallet Infrastructure - Main Entry Point
 * 
 * Provides unified access to multi-chain wallet generation,
 * encrypted storage, and transaction signing.
 */

// Generators
export * from './generators/bitcoin';
export * from './generators/ethereum';
export * from './generators/arweave';

// Storage
export * from './storage/encrypted-keystore';

// Registry
export * from './registry/address-registry';

// Wallet Manager
export { WalletManager } from './wallet-manager';
