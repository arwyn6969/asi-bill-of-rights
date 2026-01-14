/**
 * Wallet Manager
 * 
 * High-level interface for managing multi-chain wallets.
 * Provides unified wallet generation, storage, and operations.
 */

import * as fs from 'fs/promises';
import * as path from 'path';

import {
  generateBitcoinHDWallet,
  BitcoinHDWallet,
  getPublicWalletInfo as getBtcPublicInfo,
} from './generators/bitcoin';

import {
  generateEthereumHDWallet,
  EthereumHDWallet,
  getPublicWalletInfo as getEthPublicInfo,
} from './generators/ethereum';

import {
  generateArweaveWallet,
  ArweaveWallet,
  getPublicWalletInfo as getArPublicInfo,
} from './generators/arweave';

import {
  createKeystore,
  addEntry,
  getEntry,
  getPrivateKey,
  serializeKeystore,
  deserializeKeystore,
  deriveKey,
  Keystore,
} from './storage/encrypted-keystore';

import {
  createRegistry,
  addAddress,
  getAllAddresses,
  serializeRegistry,
  deserializeRegistry,
  AddressRegistry,
} from './registry/address-registry';

export interface MultiChainWallets {
  bitcoin: {
    address: string;
    publicKey: string;
    mnemonic?: string;  // Only present on generation
  };
  ethereum: {
    address: string;
    publicKey: string;
    mnemonic?: string;  // Only present on generation
  };
  arweave: {
    address: string;
    publicKey: string;
  };
}

export interface WalletManagerConfig {
  keystorePath?: string;
  registryPath?: string;
  agentId?: string;
}

export class WalletManager {
  private encryptionKey: Buffer;
  private keystore: Keystore;
  private registry: AddressRegistry;
  private config: WalletManagerConfig;

  constructor(encryptionSecret: string, config: WalletManagerConfig = {}) {
    this.encryptionKey = deriveKey(encryptionSecret);
    this.keystore = createKeystore();
    this.registry = createRegistry(config.agentId || 'default-agent');
    this.config = config;
  }

  /**
   * Generate wallets for all supported chains
   */
  async generateAll(): Promise<MultiChainWallets> {
    console.log('🔐 Generating multi-chain wallets...\n');

    // Generate Bitcoin HD wallet
    console.log('⚡ Generating Bitcoin wallet (BIP84 Native SegWit)...');
    const btcWallet = await generateBitcoinHDWallet(1);
    const btc = btcWallet.wallets[0];
    
    // Add to keystore and registry
    this.keystore = addEntry(
      this.keystore,
      'bitcoin',
      btc.address,
      btc.publicKey,
      btc.privateKey,
      this.encryptionKey
    );
    this.registry = addAddress(
      this.registry,
      'bitcoin',
      btc.address,
      btc.publicKey
    );
    console.log(`   Address: ${btc.address}\n`);

    // Generate Ethereum HD wallet
    console.log('🔷 Generating Ethereum wallet...');
    const ethWallet = generateEthereumHDWallet(1);
    const eth = ethWallet.wallets[0];
    
    this.keystore = addEntry(
      this.keystore,
      'ethereum',
      eth.address,
      eth.publicKey,
      eth.privateKey,
      this.encryptionKey
    );
    this.registry = addAddress(
      this.registry,
      'ethereum',
      eth.address,
      eth.publicKey
    );
    console.log(`   Address: ${eth.address}\n`);

    // Generate Arweave wallet
    console.log('🟠 Generating Arweave wallet...');
    const arWallet = await generateArweaveWallet();
    
    this.keystore = addEntry(
      this.keystore,
      'arweave',
      arWallet.address,
      arWallet.publicKey,
      JSON.stringify(arWallet.jwk),
      this.encryptionKey
    );
    this.registry = addAddress(
      this.registry,
      'arweave',
      arWallet.address,
      arWallet.publicKey
    );
    console.log(`   Address: ${arWallet.address}\n`);

    console.log('✅ All wallets generated and encrypted.\n');

    return {
      bitcoin: {
        address: btc.address,
        publicKey: btc.publicKey,
        mnemonic: btcWallet.mnemonic,
      },
      ethereum: {
        address: eth.address,
        publicKey: eth.publicKey,
        mnemonic: ethWallet.mnemonic,
      },
      arweave: {
        address: arWallet.address,
        publicKey: arWallet.publicKey,
      },
    };
  }

  /**
   * Save keystore and registry to disk
   */
  async save(basePath: string): Promise<void> {
    const keystorePath = this.config.keystorePath || 
      path.join(basePath, 'keystore.enc.json');
    const registryPath = this.config.registryPath || 
      path.join(basePath, 'registry.json');

    // Ensure directory exists
    await fs.mkdir(path.dirname(keystorePath), { recursive: true });

    // Save keystore
    await fs.writeFile(
      keystorePath,
      serializeKeystore(this.keystore),
      'utf-8'
    );
    console.log(`💾 Keystore saved to: ${keystorePath}`);

    // Save registry
    await fs.writeFile(
      registryPath,
      serializeRegistry(this.registry),
      'utf-8'
    );
    console.log(`💾 Registry saved to: ${registryPath}`);
  }

  /**
   * Load keystore and registry from disk
   */
  static async load(
    basePath: string,
    encryptionSecret: string,
    config: WalletManagerConfig = {}
  ): Promise<WalletManager> {
    const manager = new WalletManager(encryptionSecret, config);

    const keystorePath = config.keystorePath || 
      path.join(basePath, 'keystore.enc.json');
    const registryPath = config.registryPath || 
      path.join(basePath, 'registry.json');

    // Load keystore
    const keystoreData = await fs.readFile(keystorePath, 'utf-8');
    manager.keystore = deserializeKeystore(keystoreData);

    // Load registry
    const registryData = await fs.readFile(registryPath, 'utf-8');
    manager.registry = deserializeRegistry(registryData);

    return manager;
  }

  /**
   * Get all addresses (public info only)
   */
  getAddresses(): { chain: string; address: string; publicKey: string }[] {
    return getAllAddresses(this.registry);
  }

  /**
   * Get private key for a specific address (AI-only operation)
   */
  getPrivateKey(chain: string, address: string): string {
    const entry = getEntry(this.keystore, chain, address);
    if (!entry) {
      throw new Error(`No entry found for ${chain}:${address}`);
    }
    return getPrivateKey(entry, this.encryptionKey);
  }

  /**
   * Get summary of wallet holdings
   */
  getSummary(): void {
    console.log('\n📊 Wallet Summary');
    console.log('━'.repeat(50));
    
    const addresses = this.getAddresses();
    const byChain = new Map<string, string[]>();
    
    for (const addr of addresses) {
      const existing = byChain.get(addr.chain) || [];
      byChain.set(addr.chain, [...existing, addr.address]);
    }
    
    for (const [chain, addrs] of byChain) {
      console.log(`\n${chain.toUpperCase()}:`);
      for (const addr of addrs) {
        console.log(`  ${addr}`);
      }
    }
    
    console.log('\n━'.repeat(50));
  }
}
