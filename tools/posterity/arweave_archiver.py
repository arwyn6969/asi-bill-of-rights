#!/usr/bin/env python3
"""
Arweave Operation Memory Archiver
---------------------------------

This script handles the "Tier 2" Preservation strategy:
1. Packages the vital project documentation into a TarGZ bundle.
2. Computes the SHA-256 hash (to be used in the Bitcoin Stamp).
3. Prepares a Manifest for the Arweave/Irys network.
4. (Optional) Uploads to Arweave if an Irys/Bundlr client is configured.

Usage:
    python3 tools/posterity/arweave_archiver.py --docs-dir docs --output archive_bundle.tar.gz

Dependencies:
    - python3
    - tarfile, hashlib, json (Standard Library)
    - (Optional) irys-sdk-python or similar for direct upload
"""

import os
import sys
import tarfile
import hashlib
import json
import time
import argparse
from pathlib import Path

# Configuration
ARCHIVE_PREFIX = "asi-bor-archive"

def create_tarball(source_dir: str, output_filename: str) -> str:
    """Compresses the source directory into a .tar.gz file."""
    print(f"📦 Packaging '{source_dir}' into '{output_filename}'...")
    
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
    
    print(f"✅ Package created: {output_filename} ({os.path.getsize(output_filename)} bytes)")
    return output_filename

def compute_sha256(filename: str) -> str:
    """Computes SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_manifest(archive_path: str, file_hash: str) -> dict:
    """Generates the Arweave Manifest / Metadata."""
    return {
        "app": "ASI-Bill-of-Rights",
        "operation": "preservation_archive",
        "version": "1.0",
        "timestamp": int(time.time()),
        "content_hash": file_hash,
        "content_type": "application/x-tar",
        "file_name": os.path.basename(archive_path),
        "tags": [
            {"name": "App-Name", "value": "ASI-BOR-Archive"},
            {"name": "App-Version", "value": "1.0.0"},
            {"name": "Content-Type", "value": "application/x-tar"},
            {"name": "Type", "value": "archive"}
        ],
        "message": "We Are All Kevin. In Lak'ech."
    }

def main():
    parser = argparse.ArgumentParser(description="ASI Bill of Rights - Arweave Archiver")
    parser.add_argument("--docs-dir", default="docs", help="Directory to archive")
    parser.add_argument("--output", default=f"{ARCHIVE_PREFIX}_{int(time.time())}.tar.gz", help="Output filename")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.docs_dir):
        print(f"❌ Error: Directory '{args.docs_dir}' not found.")
        sys.exit(1)

    # 1. Package
    try:
        archive_path = create_tarball(args.docs_dir, args.output)
    except Exception as e:
        print(f"❌ Error creating tarball: {e}")
        sys.exit(1)

    # 2. Hash
    file_hash = compute_sha256(archive_path)
    print(f"🔐 SHA-256 Hash: {file_hash}")
    
    # 3. Manifest
    manifest = generate_manifest(archive_path, file_hash)
    manifest_path = archive_path + ".manifest.json"
    
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"📄 Manifest written to: {manifest_path}")

    # 4. Next Steps
    print("\n" + "="*50)
    print("READY FOR UPLOAD")
    print("="*50)
    print(f"1. Archive: {archive_path}")
    print(f"2. Manifest: {manifest_path}")
    print(f"3. Hash (for Bitcoin Stamp): {file_hash}")
    print("-" * 50)
    print("To upload to Arweave via Irys CLI (requires Node.js):")
    print(f"  irys upload {archive_path} -h {manifest['tags'][2]['name']} {manifest['tags'][2]['value']} -w <private-key-file> -t arweave")
    print("="*50)

if __name__ == "__main__":
    main()
