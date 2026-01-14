/**
 * Hash Anchoring Service
 * 
 * Anchors document hashes across multiple blockchains for
 * maximum decentralization and verifiability.
 */

import * as crypto from 'crypto';

export interface HashAnchor {
  documentId: string;
  contentHash: string;
  algorithm: string;
  anchors: AnchorRecord[];
  createdAt: string;
}

export interface AnchorRecord {
  chain: string;
  txId: string;
  blockNumber?: number;
  timestamp: string;
  verified: boolean;
}

export interface AnchorRegistry {
  version: string;
  anchors: HashAnchor[];
}

/**
 * Compute SHA-256 hash of content
 */
export function computeHash(content: string | Buffer): string {
  const hash = crypto.createHash('sha256');
  hash.update(content);
  return hash.digest('hex');
}

/**
 * Create a new hash anchor
 */
export function createHashAnchor(
  documentId: string,
  content: string | Buffer
): HashAnchor {
  return {
    documentId,
    contentHash: computeHash(content),
    algorithm: 'sha256',
    anchors: [],
    createdAt: new Date().toISOString(),
  };
}

/**
 * Add an anchor record to a hash anchor
 */
export function addAnchorRecord(
  anchor: HashAnchor,
  chain: string,
  txId: string,
  blockNumber?: number
): HashAnchor {
  const record: AnchorRecord = {
    chain,
    txId,
    blockNumber,
    timestamp: new Date().toISOString(),
    verified: false,
  };

  return {
    ...anchor,
    anchors: [...anchor.anchors, record],
  };
}

/**
 * Mark an anchor as verified
 */
export function markVerified(
  anchor: HashAnchor,
  chain: string,
  txId: string
): HashAnchor {
  return {
    ...anchor,
    anchors: anchor.anchors.map((a) => {
      if (a.chain === chain && a.txId === txId) {
        return { ...a, verified: true };
      }
      return a;
    }),
  };
}

/**
 * Verify content against a hash anchor
 */
export function verifyContent(
  anchor: HashAnchor,
  content: string | Buffer
): boolean {
  const hash = computeHash(content);
  return hash === anchor.contentHash;
}

/**
 * Create an empty anchor registry
 */
export function createRegistry(): AnchorRegistry {
  return {
    version: '1.0',
    anchors: [],
  };
}

/**
 * Add an anchor to the registry
 */
export function addToRegistry(
  registry: AnchorRegistry,
  anchor: HashAnchor
): AnchorRegistry {
  // Check for existing anchor with same document ID
  const existing = registry.anchors.findIndex(
    (a) => a.documentId === anchor.documentId
  );

  if (existing >= 0) {
    // Merge anchors
    const existingAnchor = registry.anchors[existing];
    const mergedAnchors = [
      ...existingAnchor.anchors,
      ...anchor.anchors.filter(
        (newA) => !existingAnchor.anchors.some(
          (oldA) => oldA.chain === newA.chain && oldA.txId === newA.txId
        )
      ),
    ];

    return {
      ...registry,
      anchors: [
        ...registry.anchors.slice(0, existing),
        { ...existingAnchor, anchors: mergedAnchors },
        ...registry.anchors.slice(existing + 1),
      ],
    };
  }

  return {
    ...registry,
    anchors: [...registry.anchors, anchor],
  };
}

/**
 * Get anchor by document ID
 */
export function getAnchor(
  registry: AnchorRegistry,
  documentId: string
): HashAnchor | undefined {
  return registry.anchors.find((a) => a.documentId === documentId);
}

/**
 * Get verification status for a document
 */
export function getVerificationStatus(
  anchor: HashAnchor
): {
  totalChains: number;
  verifiedChains: number;
  chains: { chain: string; verified: boolean; txId: string }[];
} {
  const chains = anchor.anchors.map((a) => ({
    chain: a.chain,
    verified: a.verified,
    txId: a.txId,
  }));

  return {
    totalChains: chains.length,
    verifiedChains: chains.filter((c) => c.verified).length,
    chains,
  };
}

/**
 * Serialize registry to JSON
 */
export function serializeRegistry(registry: AnchorRegistry): string {
  return JSON.stringify(registry, null, 2);
}

/**
 * Deserialize registry from JSON
 */
export function deserializeRegistry(json: string): AnchorRegistry {
  return JSON.parse(json) as AnchorRegistry;
}

/**
 * Generate a verification proof
 */
export function generateProof(anchor: HashAnchor): string {
  const proof = {
    documentId: anchor.documentId,
    contentHash: anchor.contentHash,
    algorithm: anchor.algorithm,
    anchors: anchor.anchors.map((a) => ({
      chain: a.chain,
      txId: a.txId,
      verified: a.verified,
    })),
    generatedAt: new Date().toISOString(),
  };

  return JSON.stringify(proof, null, 2);
}
