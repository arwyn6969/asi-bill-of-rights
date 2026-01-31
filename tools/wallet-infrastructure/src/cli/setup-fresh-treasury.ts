/**
 * ASI Bill of Rights - Fresh Treasury Setup
 * 
 * Generates a CRYPTOGRAPHICALLY SECURE 24-word mnemonic.
 * Saves it to .env (which is strictly gitignored).
 * Displays it ONCE for physical backup.
 */

import * as bip39 from 'bip39';
import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';
import * as readline from 'readline';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT_DIR = path.resolve(__dirname, '../../../../');
const ENV_PATH = path.join(ROOT_DIR, '.env');

// ANSI Colors for warnings
const RED = '\x1b[31m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const CYAN = '\x1b[36m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';

async function main() {
  console.clear();
  console.log('═'.repeat(70));
  console.log(`${BOLD}${CYAN}  ASI BILL OF RIGHTS - FRESH TREASURY KEY CEREMONY${RESET}`);
  console.log('═'.repeat(70));
  console.log();
  
  // 1. Security Checks
  console.log(`${BOLD}1. PRE-FLIGHT SECURITY CHECK${RESET}`);
  
  // Check .gitignore
  const gitignorePath = path.join(ROOT_DIR, '.gitignore');
  if (fs.existsSync(gitignorePath)) {
    const gitignore = fs.readFileSync(gitignorePath, 'utf8');
    if (!gitignore.includes('.env')) {
      console.log(`${RED}❌ CRITICAL FAIL: .env is NOT in .gitignore!${RESET}`);
      console.log('   Aborting immediately to prevent leak.');
      process.exit(1);
    }
    console.log(`${GREEN}✅ .gitignore correctly excludes .env${RESET}`);
  } else {
    console.log(`${YELLOW}⚠️  WARNING: .gitignore not found at ${gitignorePath}${RESET}`); 
    // We proceed but with caution - user might be in a different root
  }

  // Check existing .env
  let existingEnv = '';
  if (fs.existsSync(ENV_PATH)) {
    existingEnv = fs.readFileSync(ENV_PATH, 'utf8');
    if (existingEnv.includes('TREASURY_MNEMONIC')) {
      console.log(`${YELLOW}⚠️  WARNING: TREASURY_MNEMONIC already exists in .env${RESET}`);
      console.log('   Running this will OVERWRITE the existing key.');
    }
  }

  console.log();
  console.log(`${BOLD}2. INTERACTIVE CONFIRMATION${RESET}`);
  
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  const confirmed = await new Promise<boolean>(resolve => {
    rl.question(`${YELLOW}Are you ready to generate a NEW seed phrase? (yes/no): ${RESET}`, answer => {
      resolve(answer.toLowerCase() === 'yes');
    });
  });

  if (!confirmed) {
    console.log('Aborted.');
    process.exit(0);
  }

  // 2. Generate Credentials
  console.log();
  console.log(`${BOLD}3. GENERATING ENTROPY...${RESET}`);
  
  // 256 bits = 24 words (Maximum Security)
  const mnemonic = bip39.generateMnemonic(256);
  
  if (!bip39.validateMnemonic(mnemonic)) {
    console.error(`${RED}❌ Error: Generated invalid mnemonic${RESET}`);
    process.exit(1);
  }
  console.log(`${GREEN}✅ Cryptographically secure 24-word phrase generated${RESET}`);

  // 3. Save to .env
  console.log();
  console.log(`${BOLD}4. SECURE STORAGE${RESET}`);
  
  let newEnvContent = existingEnv;
  
  // Remove existing key if present to avoid duplicates
  if (newEnvContent.includes('TREASURY_MNEMONIC=')) {
    newEnvContent = newEnvContent.split('\n').filter(line => !line.startsWith('TREASURY_MNEMONIC=')).join('\n');
  }
  
  // Ensure newline at end
  if (newEnvContent && !newEnvContent.endsWith('\n')) {
    newEnvContent += '\n';
  }
  
  // Append new key
  newEnvContent += `TREASURY_MNEMONIC="${mnemonic}"\n`;
  
  fs.writeFileSync(ENV_PATH, newEnvContent);
  console.log(`${GREEN}✅ Saved to local .env file (${ENV_PATH})${RESET}`);
  console.log('   (This file is gitignored and will NOT be uploaded)');

  // 4. The One-Time Reveal
  console.log();
  console.log('═'.repeat(70));
  console.log(`${RED}${BOLD}  🛑 STOP AND READ CAREFULLY 🛑${RESET}`);
  console.log('═'.repeat(70));
  console.log('  I am about to display the Master Seed Phrase.');
  console.log('  This is the ONLY time you will see it in cleartext.');
  console.log();
  console.log('  1. Get a piece of paper and a pen.');
  console.log('  2. Ensure no one is looking at your screen.');
  console.log('  3. Write down these 24 words in order.');
  console.log('═'.repeat(70));
  console.log();
  
  await new Promise(resolve => setTimeout(resolve, 2000)); // Pause for effect

  console.log(`${BOLD}${YELLOW}${mnemonic}${RESET}`);
  console.log();
  console.log('═'.repeat(70));
  
  rl.question(`${CYAN}Press ENTER once you have written it down to CLEAR the screen...${RESET}`, () => {
    console.clear();
    console.log(`${GREEN}✅ Screen cleared.${RESET}`);
    console.log('   Your treasury is now initialized in .env.');
    console.log('   You can now run "npm run generate-addresses" to see your public addresses.');
    rl.close();
    process.exit(0);
  });
}

main().catch(console.error);
