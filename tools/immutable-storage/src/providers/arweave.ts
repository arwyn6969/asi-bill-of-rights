/**
 * Arweave Storage Provider
 * 
 * Integrates with Arweave for permanent, decentralized storage.
 * Supports direct uploads and Bundlr for optimized uploading.
 */

import Arweave from 'arweave';
import { JWKInterface } from 'arweave/node/lib/wallet';

export interface ArweaveConfig {
  host: string;
  port: number;
  protocol: string;
  useBundlr: boolean;
  bundlrNode?: string;
}

export interface ArweaveResult {
  success: boolean;
  txId?: string;
  url?: string;
  error?: string;
}

export interface ArweaveData {
  content: string | Buffer;
  contentType: string;
  name: string;
  tags?: { name: string; value: string }[];
}

const DEFAULT_CONFIG: ArweaveConfig = {
  host: 'arweave.net',
  port: 443,
  protocol: 'https',
  useBundlr: false,
  bundlrNode: 'https://node1.bundlr.network',
};

/**
 * Arweave Storage Provider
 */
export class ArweaveProvider {
  private config: ArweaveConfig;
  private client: Arweave;
  private wallet: JWKInterface | null = null;

  constructor(config: Partial<ArweaveConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.client = Arweave.init({
      host: this.config.host,
      port: this.config.port,
      protocol: this.config.protocol,
    });
  }

  /**
   * Set the wallet for signing transactions
   */
  setWallet(wallet: JWKInterface): void {
    this.wallet = wallet;
  }

  /**
   * Load wallet from JWK file content
   */
  loadWallet(jwkJson: string): void {
    this.wallet = JSON.parse(jwkJson);
  }

  /**
   * Store data on Arweave
   */
  async store(data: ArweaveData): Promise<ArweaveResult> {
    if (!this.wallet) {
      return {
        success: false,
        error: 'No wallet configured. Call setWallet() first.',
      };
    }

    console.log('🟠 Arweave Storage');
    console.log('━'.repeat(40));
    console.log(`   Name: ${data.name}`);
    console.log(`   Type: ${data.contentType}`);
    console.log(`   Size: ${data.content.length} bytes`);

    try {
      // Create transaction
      const transaction = await this.client.createTransaction({
        data: data.content,
      }, this.wallet);

      // Add content type tag
      transaction.addTag('Content-Type', data.contentType);
      
      // Add app-specific tags
      transaction.addTag('App-Name', 'ASI-Bill-of-Rights');
      transaction.addTag('Document-Name', data.name);
      transaction.addTag('Timestamp', new Date().toISOString());

      // Add custom tags
      if (data.tags) {
        for (const tag of data.tags) {
          transaction.addTag(tag.name, tag.value);
        }
      }

      // Sign transaction
      await this.client.transactions.sign(transaction, this.wallet);

      // Get upload cost
      const cost = await this.client.transactions.getPrice(
        transaction.data.length
      );
      console.log(`   Cost: ${this.client.ar.winstonToAr(cost)} AR`);

      // Post transaction
      const response = await this.client.transactions.post(transaction);

      if (response.status === 200 || response.status === 202) {
        const txId = transaction.id;
        const url = `https://arweave.net/${txId}`;
        
        console.log(`\n✅ Uploaded successfully!`);
        console.log(`   TX ID: ${txId}`);
        console.log(`   URL: ${url}\n`);

        return {
          success: true,
          txId,
          url,
        };
      } else {
        return {
          success: false,
          error: `Upload failed: ${response.status} ${response.statusText}`,
        };
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : String(error);
      return {
        success: false,
        error: errorMessage,
      };
    }
  }

  /**
   * Retrieve data from Arweave
   */
  async retrieve(txId: string): Promise<ArweaveData | null> {
    try {
      const transaction = await this.client.transactions.get(txId);
      const data = await this.client.transactions.getData(txId, {
        decode: true,
        string: true,
      });

      // Get tags
      const tags = transaction.tags.map((tag) => ({
        name: tag.get('name', { decode: true, string: true }),
        value: tag.get('value', { decode: true, string: true }),
      }));

      const contentType = tags.find((t) => t.name === 'Content-Type')?.value || 
        'application/octet-stream';
      const name = tags.find((t) => t.name === 'Document-Name')?.value || txId;

      return {
        content: data as string,
        contentType,
        name,
        tags,
      };
    } catch (error) {
      console.error('Error retrieving from Arweave:', error);
      return null;
    }
  }

  /**
   * Check if a transaction exists and is confirmed
   */
  async exists(txId: string): Promise<boolean> {
    try {
      const status = await this.client.transactions.getStatus(txId);
      return status.status === 200;
    } catch {
      return false;
    }
  }

  /**
   * Get transaction status
   */
  async getStatus(txId: string): Promise<{
    confirmed: boolean;
    confirmations?: number;
    blockHeight?: number;
  }> {
    try {
      const status = await this.client.transactions.getStatus(txId);
      
      if (status.status === 200 && status.confirmed) {
        return {
          confirmed: true,
          confirmations: status.confirmed.number_of_confirmations,
          blockHeight: status.confirmed.block_height,
        };
      }
      
      return { confirmed: false };
    } catch {
      return { confirmed: false };
    }
  }

  /**
   * Get wallet balance
   */
  async getBalance(): Promise<string> {
    if (!this.wallet) {
      throw new Error('No wallet configured');
    }
    
    const address = await this.client.wallets.jwkToAddress(this.wallet);
    const winston = await this.client.wallets.getBalance(address);
    return this.client.ar.winstonToAr(winston);
  }

  /**
   * Estimate storage cost
   */
  async estimateCost(bytes: number): Promise<{
    winston: string;
    ar: string;
  }> {
    const winston = await this.client.transactions.getPrice(bytes);
    return {
      winston,
      ar: this.client.ar.winstonToAr(winston),
    };
  }

  /**
   * Get the Arweave gateway URL for a transaction
   */
  getUrl(txId: string): string {
    return `https://arweave.net/${txId}`;
  }
}

export default ArweaveProvider;
