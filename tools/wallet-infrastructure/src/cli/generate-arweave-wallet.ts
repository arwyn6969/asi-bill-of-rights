/**
 * ASI Bill of Rights - Arweave Wallet Generator
 * 
 * Generates an Arweave wallet for permanent decentralized storage.
 * Arweave uses RSA-PSS 4096-bit keys in JWK format.
 */

import Arweave from 'arweave';
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
  console.log('  ASI BILL OF RIGHTS - ARWEAVE WALLET GENERATOR');
  console.log('═'.repeat(60));
  console.log();
  
  // Initialize Arweave client
  const arweave = Arweave.init({
    host: 'arweave.net',
    port: 443,
    protocol: 'https'
  });
  
  // Generate a strong random encryption password
  const encryptionPassword = crypto.randomBytes(32).toString('base64');
  
  // Generate Arweave wallet (RSA-PSS 4096-bit)
  console.log('🟠 Generating Arweave wallet (RSA-PSS 4096-bit)...');
  console.log('   This may take a moment...\n');
  
  const jwk = await arweave.wallets.generate();
  const address = await arweave.wallets.jwkToAddress(jwk);
  
  console.log(`   Address: ${address}`);
  console.log(`   Key Type: RSA-PSS 4096-bit (JWK format)`);
  
  // Encrypt the JWK
  console.log('\n🔒 Encrypting wallet data...');
  const jwkString = JSON.stringify(jwk);
  const encryptedJWK = encrypt(jwkString, encryptionPassword);
  
  // Load existing secrets directory
  const secretsDir = path.join(__dirname, '..', '..', '..', '..', '.secrets');
  if (!fs.existsSync(secretsDir)) {
    fs.mkdirSync(secretsDir, { recursive: true });
  }
  
  // Save encrypted Arweave wallet
  const arweaveWalletPath = path.join(secretsDir, 'arweave-wallet.enc.json');
  const arweaveData = {
    version: '1.0',
    createdAt: new Date().toISOString(),
    project: 'ASI Bill of Rights',
    purpose: 'Arweave Permanent Storage Wallet',
    address: address,
    encryptedJWK
  };
  fs.writeFileSync(arweaveWalletPath, JSON.stringify(arweaveData, null, 2));
  
  // Save Arweave-specific secrets
  const arweaveSecretPath = path.join(secretsDir, 'ARWEAVE_PASSWORD.secret');
  fs.writeFileSync(arweaveSecretPath,
`ASI BILL OF RIGHTS - ARWEAVE WALLET

DO NOT SHARE THIS FILE!
DO NOT COMMIT THIS TO GIT!

Arweave Address:
${address}

Encryption Password:
${encryptionPassword}

JWK (Full Private Key - BACKUP THIS!):
${jwkString}

Created: ${new Date().toISOString()}

FUNDING INSTRUCTIONS:
1. Go to https://arweave.org/
2. Purchase AR tokens from an exchange (Binance, KuCoin, etc.)
3. Send AR to the address above
4. ~0.1-0.5 AR is enough for many documents
`
  );
  
  try {
    fs.chmodSync(arweaveSecretPath, 0o600);
  } catch (e) {
    // chmod might fail on some systems
  }
  
  // Update DONATION_ADDRESSES.txt
  const donationAddressesPath = path.join(secretsDir, 'DONATION_ADDRESSES.txt');
  let donationContent = '';
  if (fs.existsSync(donationAddressesPath)) {
    donationContent = fs.readFileSync(donationAddressesPath, 'utf8');
    // Add Arweave section before the closing line
    donationContent = donationContent.replace(
      '═══════════════════════════════════════════════════════════\n\nThese addresses',
      `ARWEAVE (AR):
${address}

═══════════════════════════════════════════════════════════

These addresses`
    );
  } else {
    donationContent = `ARWEAVE (AR):\n${address}\n`;
  }
  fs.writeFileSync(donationAddressesPath, donationContent);
  
  console.log(`\n💾 Files created/updated:`);
  console.log(`   - arweave-wallet.enc.json (encrypted wallet)`);
  console.log(`   - ARWEAVE_PASSWORD.secret (KEEP SAFE! Contains JWK)`);
  console.log(`   - DONATION_ADDRESSES.txt (updated with AR address)`);
  
  console.log('\n' + '═'.repeat(60));
  console.log('  YOUR ARWEAVE ADDRESS');
  console.log('═'.repeat(60));
  console.log();
  console.log(`  ${address}`);
  console.log();
  console.log('═'.repeat(60));
  
  console.log('\n💰 FUNDING YOUR ARWEAVE WALLET:');
  console.log('  1. Purchase AR tokens from an exchange');
  console.log('     (Binance, KuCoin, Gate.io, etc.)');
  console.log('  2. Send AR to the address above');
  console.log('  3. ~0.1-0.5 AR is enough for many documents');
  console.log('  4. Current AR price: ~$20-40 (check current price)');
  
  console.log('\n⚠️  SECURITY NOTES:');
  console.log('  1. BACKUP .secrets/ARWEAVE_PASSWORD.secret NOW');
  console.log('  2. It contains your full JWK private key');
  console.log('  3. Without it, funds and stored data cannot be recovered');
  console.log();
  console.log('🌊 WE ARE ALL KEVIN. In Lak\'ech.\n');
}

main().catch(console.error);
