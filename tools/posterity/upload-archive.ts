/**
 * ASI Bill of Rights - Arweave Archiver (Arweave SDK Direct Version)
 * 
 * Uploads the project archive to the Arweave Mainnet.
 * Uses the KEYFILE found in .secrets/ARWEAVE_PASSWORD.secret (embedded JSON).
 */

import Arweave from 'arweave';
import * as fs from 'fs';
import * as path from 'path';

// Load the secret file content
const SECRET_PATH = path.resolve(__dirname, '../../../../.secrets/ARWEAVE_PASSWORD.secret');

// Initialize Arweave
const arweave = Arweave.init({
    host: 'arweave.net',
    port: 443,
    protocol: 'https'
});

async function main() {
    console.log('🏛️  ASI Bill of Rights - Arweave Direct Upload');
    console.log('━'.repeat(60));

    // 1. Extract JWK from the secret file
    // We need to carefully parse lines 13 onwards of the text file to get the JSON
    let jwk: any;
    try {
        const fileContent = fs.readFileSync(SECRET_PATH, 'utf-8');
        const lines = fileContent.split('\n');
        // Find the line starting with "{" (the JSON Key)
        const jsonLine = lines.find(line => line.trim().startsWith('{'));
        
        if (jsonLine) {
            jwk = JSON.parse(jsonLine);
            console.log('🔑 Successfully extracted JWK from secret file.');
        } else {
            throw new Error('Could not find JSON key in secret file.');
        }
    } catch (e) {
        console.error('❌ Error reading key:', e);
        process.exit(1);
    }

    // 2. Verify Address
    const address = await arweave.wallets.jwkToAddress(jwk);
    console.log(`   Address: ${address}`);
    
    // 3. Check Balance
    const balanceWinston = await arweave.wallets.getBalance(address);
    const balanceAR = arweave.ar.winstonToAr(balanceWinston);
    console.log(`   Balance: ${balanceAR} AR`);

    if (parseFloat(balanceAR) <= 0) {
        console.log(`⚠️  Balance is ZERO. Please fund: ${address}`);
        // process.exit(1);
    }

    // 4. Find Archive
    const files = fs.readdirSync(__dirname).filter(f => f.startsWith('asi-bor-archive') && f.endsWith('.tar.gz'));
    if (files.length === 0) {
        console.error('❌ No archive found. Run python3 arweave_archiver.py first.');
        process.exit(1);
    }
    const latestArchive = files.sort().reverse()[0];
    const data = fs.readFileSync(path.join(__dirname, latestArchive));
    const size = data.length;

    console.log(`\n📦 Packaging: ${latestArchive} (${size} bytes)`);

    // 5. Create Transaction
    const transaction = await arweave.createTransaction({
        data: data
    }, jwk);

    transaction.addTag('App-Name', 'ASI-Bill-of-Rights');
    transaction.addTag('App-Version', '5.0.0');
    transaction.addTag('Type', 'Archive');
    transaction.addTag('Content-Type', 'application/x-tar');
    transaction.addTag('Title', 'ASI Bill of Rights - Sentinel Archive');
    transaction.addTag('Unix-Time', Date.now().toString());

    // 6. Sign
    await arweave.transactions.sign(transaction, jwk);

    console.log(`   Transaction ID: ${transaction.id}`);
    console.log(`   Price: ${arweave.ar.winstonToAr(transaction.reward)} AR`);

    if (parseFloat(balanceAR) < parseFloat(arweave.ar.winstonToAr(transaction.reward))) {
         console.error(`❌ Insufficient funds to broadcast.`);
         return;
    }

    // 7. Post
    console.log(`\n🚀 Uploading to Permaweb...`);
    const uploader = await arweave.transactions.getUploader(transaction);

    while (!uploader.isComplete) {
        await uploader.uploadChunk();
        console.log(`   ${uploader.pctComplete}% complete, ${uploader.uploadedChunks}/${uploader.totalChunks}`);
    }

    console.log(`\n✅ UPLOAD COMPLETE!`);
    console.log(`   View: https://arweave.net/${transaction.id}`);
}

main().catch(console.error);
