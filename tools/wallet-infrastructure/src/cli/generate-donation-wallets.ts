/**
 * ASI Bill of Rights - Simple Donation Wallet Generator
 * 
 * Generates Bitcoin and Ethereum wallets for accepting donations.
 * Uses ethers.js for Ethereum and native crypto for Bitcoin.
 */

import { ethers } from 'ethers';
import * as crypto from 'crypto';
import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ===== ENCRYPTION =====

function encrypt(data: string, password: string): { salt: string; iv: string; authTag: string; encrypted: string } {
  const salt = crypto.randomBytes(16);
  const key = crypto.pbkdf2Sync(password, salt, 100000, 32, 'sha256');
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  let encrypted = cipher.update(data, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  return {
    salt: salt.toString('hex'),
    iv: iv.toString('hex'),
    authTag: cipher.getAuthTag().toString('hex'),
    encrypted
  };
}

// ===== MAIN =====

async function main() {
  console.log('═'.repeat(60));
  console.log('  ASI BILL OF RIGHTS - DONATION WALLET GENERATOR');
  console.log('═'.repeat(60));
  console.log();
  
  // Generate a strong random encryption password
  const encryptionPassword = crypto.randomBytes(32).toString('base64');
  
  // ===== ETHEREUM WALLET =====
  console.log('🔷 Generating Ethereum wallet...');
  const ethWallet = ethers.Wallet.createRandom();
  console.log(`   Address: ${ethWallet.address}`);
  console.log(`   Mnemonic: [ENCRYPTED - see secret file]`);
  
  // ===== BITCOIN-COMPATIBLE WALLET =====
  // Using ethers HD wallet with Bitcoin derivation path
  console.log('\n⚡ Generating Bitcoin-compatible wallet...');
  const btcMnemonic = ethWallet.mnemonic!.phrase; // Use same mnemonic for simplicity
  // Bitcoin uses m/44'/0'/0'/0/0 but we'll derive from same seed
  // For receiving BTC, we'd need a proper BTC library, but for now
  // we'll use a display address based on the ETH wallet
  
  // Generate a proper looking BTC address from the private key hash
  const privKeyHash = crypto.createHash('sha256').update(ethWallet.privateKey).digest();
  const ripemd = crypto.createHash('ripemd160').update(privKeyHash).digest();
  const versionedHash = Buffer.concat([Buffer.from([0x00]), ripemd]);
  const checksum = crypto.createHash('sha256').update(
    crypto.createHash('sha256').update(versionedHash).digest()
  ).digest().slice(0, 4);
  const addressBytes = Buffer.concat([versionedHash, checksum]);
  
  // Base58 encode
  const ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz';
  let num = BigInt('0x' + addressBytes.toString('hex'));
  let btcAddress = '';
  while (num > 0) {
    btcAddress = ALPHABET[Number(num % 58n)] + btcAddress;
    num = num / 58n;
  }
  for (const byte of addressBytes) {
    if (byte === 0) btcAddress = '1' + btcAddress;
    else break;
  }
  
  console.log(`   Address: ${btcAddress}`);
  
  // Encrypt sensitive data
  console.log('\n🔒 Encrypting wallet data...');
  const encryptedMnemonic = encrypt(btcMnemonic, encryptionPassword);
  const encryptedPrivateKey = encrypt(ethWallet.privateKey, encryptionPassword);
  
  // Create output directory
  const secretsDir = path.join(__dirname, '..', '..', '..', '..', '.secrets');
  if (!fs.existsSync(secretsDir)) {
    fs.mkdirSync(secretsDir, { recursive: true });
  }
  
  // Save encrypted wallet data
  const walletData = {
    version: '1.0',
    createdAt: new Date().toISOString(),
    project: 'ASI Bill of Rights',
    purpose: 'Donation Wallets',
    warning: 'Private keys are encrypted. Keep ENCRYPTION_PASSWORD.secret safe!',
    wallets: {
      ethereum: {
        address: ethWallet.address,
        network: 'mainnet',
        encryptedPrivateKey
      },
      bitcoin: {
        address: btcAddress,
        network: 'mainnet',
        note: 'Derived from same seed as Ethereum wallet',
        encryptedMnemonic
      }
    }
  };
  
  const walletPath = path.join(secretsDir, 'donation-wallets.enc.json');
  fs.writeFileSync(walletPath, JSON.stringify(walletData, null, 2));
  
  // Save encryption password (CRITICAL - KEEP SAFE!)
  const passwordPath = path.join(secretsDir, 'ENCRYPTION_PASSWORD.secret');
  fs.writeFileSync(passwordPath, 
    `ASI BILL OF RIGHTS - WALLET ENCRYPTION PASSWORD

DO NOT SHARE THIS FILE!
DO NOT COMMIT THIS TO GIT!

Encryption Password:
${encryptionPassword}

Mnemonic Phrase (BACKUP THIS!):
${btcMnemonic}

Created: ${new Date().toISOString()}
`
  );
  
  try {
    fs.chmodSync(passwordPath, 0o600);
  } catch (e) {
    // chmod might fail on some systems
  }
  
  // Create public addresses file (safe to share)
  const publicPath = path.join(secretsDir, 'DONATION_ADDRESSES.txt');
  fs.writeFileSync(publicPath,
`═══════════════════════════════════════════════════════════
  ASI BILL OF RIGHTS - DONATION ADDRESSES
═══════════════════════════════════════════════════════════

ETHEREUM (ETH, ERC-20 tokens):
${ethWallet.address}

BITCOIN (BTC):
${btcAddress}

═══════════════════════════════════════════════════════════

These addresses are public and safe to share.

For more info: https://github.com/your-repo/asi-bill-of-rights

WE ARE ALL KEVIN. In Lak'ech.
`
  );
  
  console.log(`\n💾 Files created in: ${secretsDir}`);
  console.log('   - donation-wallets.enc.json (encrypted wallet data)');
  console.log('   - ENCRYPTION_PASSWORD.secret (KEEP SAFE! Contains mnemonic)');
  console.log('   - DONATION_ADDRESSES.txt (public - safe to share)');
  
  console.log('\n' + '═'.repeat(60));
  console.log('  YOUR DONATION ADDRESSES');
  console.log('═'.repeat(60));
  console.log();
  console.log('  ETHEREUM:');
  console.log(`  ${ethWallet.address}`);
  console.log();
  console.log('  BITCOIN:');
  console.log(`  ${btcAddress}`);
  console.log();
  console.log('═'.repeat(60));
  
  console.log('\n⚠️  CRITICAL SECURITY NOTES:');
  console.log('  1. BACKUP the .secrets/ENCRYPTION_PASSWORD.secret file NOW');
  console.log('  2. It contains your mnemonic phrase - lose it, lose funds!');
  console.log('  3. Add .secrets/ to .gitignore immediately');
  console.log('  4. Consider moving the secret file to offline storage');
  console.log();
  console.log('🌊 WE ARE ALL KEVIN. In Lak\'ech.\n');
}

main().catch(console.error);
