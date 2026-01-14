/**
 * Address Registry
 * 
 * Tracks all wallet addresses across chains for the AI agent.
 * Provides a unified view of multi-chain wallet holdings.
 */

export interface AddressEntry {
  chain: string;
  address: string;
  publicKey: string;
  label?: string;
  createdAt: string;
  lastUsed?: string;
  balance?: string;
  balanceUpdatedAt?: string;
}

export interface AddressRegistry {
  version: string;
  agentId: string;
  createdAt: string;
  updatedAt: string;
  addresses: AddressEntry[];
}

/**
 * Create a new address registry
 */
export function createRegistry(agentId: string): AddressRegistry {
  const now = new Date().toISOString();
  return {
    version: '1.0',
    agentId,
    createdAt: now,
    updatedAt: now,
    addresses: [],
  };
}

/**
 * Add an address to the registry
 */
export function addAddress(
  registry: AddressRegistry,
  chain: string,
  address: string,
  publicKey: string,
  label?: string
): AddressRegistry {
  const now = new Date().toISOString();
  
  // Check for duplicates
  const exists = registry.addresses.some(
    (a) => a.chain === chain && a.address === address
  );
  
  if (exists) {
    throw new Error(`Address ${address} already exists on ${chain}`);
  }
  
  const entry: AddressEntry = {
    chain,
    address,
    publicKey,
    label,
    createdAt: now,
  };
  
  return {
    ...registry,
    updatedAt: now,
    addresses: [...registry.addresses, entry],
  };
}

/**
 * Get addresses by chain
 */
export function getAddressesByChain(
  registry: AddressRegistry,
  chain: string
): AddressEntry[] {
  return registry.addresses.filter((a) => a.chain === chain);
}

/**
 * Get all addresses
 */
export function getAllAddresses(registry: AddressRegistry): AddressEntry[] {
  return registry.addresses;
}

/**
 * Get address by chain and address
 */
export function getAddress(
  registry: AddressRegistry,
  chain: string,
  address: string
): AddressEntry | undefined {
  return registry.addresses.find(
    (a) => a.chain === chain && a.address === address
  );
}

/**
 * Update balance for an address
 */
export function updateBalance(
  registry: AddressRegistry,
  chain: string,
  address: string,
  balance: string
): AddressRegistry {
  const now = new Date().toISOString();
  
  return {
    ...registry,
    updatedAt: now,
    addresses: registry.addresses.map((a) => {
      if (a.chain === chain && a.address === address) {
        return {
          ...a,
          balance,
          balanceUpdatedAt: now,
        };
      }
      return a;
    }),
  };
}

/**
 * Mark address as used
 */
export function markUsed(
  registry: AddressRegistry,
  chain: string,
  address: string
): AddressRegistry {
  const now = new Date().toISOString();
  
  return {
    ...registry,
    updatedAt: now,
    addresses: registry.addresses.map((a) => {
      if (a.chain === chain && a.address === address) {
        return { ...a, lastUsed: now };
      }
      return a;
    }),
  };
}

/**
 * Remove an address from the registry
 */
export function removeAddress(
  registry: AddressRegistry,
  chain: string,
  address: string
): AddressRegistry {
  return {
    ...registry,
    updatedAt: new Date().toISOString(),
    addresses: registry.addresses.filter(
      (a) => !(a.chain === chain && a.address === address)
    ),
  };
}

/**
 * Get summary of all chains
 */
export function getChainSummary(registry: AddressRegistry): {
  chain: string;
  count: number;
  addresses: string[];
}[] {
  const chains = new Map<string, string[]>();
  
  for (const entry of registry.addresses) {
    const existing = chains.get(entry.chain) || [];
    chains.set(entry.chain, [...existing, entry.address]);
  }
  
  return Array.from(chains.entries()).map(([chain, addresses]) => ({
    chain,
    count: addresses.length,
    addresses,
  }));
}

/**
 * Serialize registry to JSON
 */
export function serializeRegistry(registry: AddressRegistry): string {
  return JSON.stringify(registry, null, 2);
}

/**
 * Deserialize registry from JSON
 */
export function deserializeRegistry(json: string): AddressRegistry {
  const parsed = JSON.parse(json);
  
  if (!parsed.version || !parsed.agentId || !parsed.addresses) {
    throw new Error('Invalid registry format');
  }
  
  return parsed as AddressRegistry;
}
