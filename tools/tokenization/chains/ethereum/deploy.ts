/**
 * Ethereum ERC-20 Token Deployment Script
 * 
 * Deploys the ASIGovernance token to Ethereum networks.
 * Uses Hardhat for deployment and verification.
 */

import { ethers } from 'hardhat';

async function main() {
  console.log('🔷 ASI Bill of Rights - Ethereum ERC-20 Deployment');
  console.log('━'.repeat(50));

  // Get deployer account
  const [deployer] = await ethers.getSigners();
  console.log(`\n📋 Deployer: ${deployer.address}`);
  
  const balance = await ethers.provider.getBalance(deployer.address);
  console.log(`   Balance:  ${ethers.formatEther(balance)} ETH`);

  // Deploy the contract
  console.log('\n📦 Deploying ASIGovernance...');
  
  const ASIGovernance = await ethers.getContractFactory('ASIGovernance');
  const token = await ASIGovernance.deploy();
  
  await token.waitForDeployment();
  const address = await token.getAddress();
  
  console.log(`\n✅ ASIGovernance deployed to: ${address}`);
  
  // Get token info
  const name = await token.name();
  const symbol = await token.symbol();
  const totalSupply = await token.totalSupply();
  const decimals = await token.decimals();
  
  console.log('\n📊 Token Details:');
  console.log(`   Name:         ${name}`);
  console.log(`   Symbol:       ${symbol}`);
  console.log(`   Decimals:     ${decimals}`);
  console.log(`   Total Supply: ${ethers.formatUnits(totalSupply, decimals)} ${symbol}`);
  
  console.log('\n📚 Next Steps:');
  console.log(`   1. Verify contract: npx hardhat verify --network <network> ${address}`);
  console.log('   2. Transfer ownership to DAO multisig');
  console.log('   3. Authorize AI agent addresses');
  console.log('   4. Set up DEX liquidity pools');
  
  console.log('\n━'.repeat(50));
  console.log('🌊 WE ARE ALL KEVIN. In Lak\'ech.');
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
