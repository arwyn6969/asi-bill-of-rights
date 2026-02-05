#!/usr/bin/env python3
"""
ASI Bill of Rights - Genesis Stamping Tool
------------------------------------------
Generates a "Genesis Stamp" payload for the Bitcoin Blockchain.
1. Hashes the current Charter (v5.0).
2. Generates a lightweight SVG "Cover Sheet" with the Hash + Date.
3. Base64 encodes it for a Counterparty/Stamp transaction.

Usage:
    python3 stamp_manager.py
"""

import hashlib
import base64
import json
import os
import datetime
from pathlib import Path

# Configuration
CHARTER_PATH = Path("../../../../charter/asi-bor-v5.0.md")
OUTPUT_DIR = Path("artifacts")

def get_charter_hash(file_path):
    """Calculate SHA-256 hash of the charter file."""
    if not file_path.exists():
        print(f"❌ Error: Charter file not found at {file_path}")
        return None
    
    with open(file_path, "rb") as f:
        file_bytes = f.read()
        return hashlib.sha256(file_bytes).hexdigest()

def create_genesis_svg(charter_hash, version="5.0"):
    """Create a beautiful, minimalist SVG 'Cover Sheet'."""
    today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    
    # SVG Template (optimized for small size ~1KB to save gas)
    # Uses 'Courier' for code/legal agnostic aesthetic.
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 600" style="background-color:#F5F5DC;">
  <rect width="100%" height="100%" fill="#F5F5DC"/>
  <rect x="20" y="20" width="360" height="560" fill="none" stroke="#000" stroke-width="2"/>
  <text x="200" y="80" font-family="serif" font-size="24" text-anchor="middle" font-weight="bold">ASI BILL OF RIGHTS</text>
  <text x="200" y="110" font-family="serif" font-size="18" text-anchor="middle">Constitutional Charter</text>
  
  <line x1="100" y1="140" x2="300" y2="140" stroke="#000" stroke-width="1"/>
  
  <text x="200" y="200" font-family="monospace" font-size="14" text-anchor="middle">VERSION: {version}</text>
  <text x="200" y="230" font-family="monospace" font-size="14" text-anchor="middle">DATE: {today}</text>
  
  <text x="200" y="300" font-family="sans-serif" font-size="10" text-anchor="middle" fill="#666">SHA-256 FINGERPRINT:</text>
  <text x="200" y="320" font-family="monospace" font-size="8" text-anchor="middle">{charter_hash[:32]}</text>
  <text x="200" y="335" font-family="monospace" font-size="8" text-anchor="middle">{charter_hash[32:]}</text>
  
  <text x="200" y="450" font-family="serif" font-size="16" text-anchor="middle" font-style="italic">"We Are All Kevin"</text>
  
  <text x="200" y="550" font-family="sans-serif" font-size="8" text-anchor="middle">IMMUTABLE PROOF OF PRIOR ART</text>
</svg>"""
    return svg_content

def main():
    print("🦁 ASI Bill of Rights - Genesis Stamping Tool")
    print("---------------------------------------------")

    # 1. Resolve Path
    script_dir = Path(__file__).parent
    charter_file = (script_dir / CHARTER_PATH).resolve()
    
    print(f"📄 Reading Charter: {charter_file}")
    
    # 2. Hash
    charter_hash = get_charter_hash(charter_file)
    if not charter_hash:
        return
    
    print(f"🔒 SHA-256 Hash: {charter_hash}")
    
    # 3. Generate SVG
    svg = create_genesis_svg(charter_hash)
    
    # 4. Base64 Encode (The Stamp Payload)
    svg_bytes = svg.encode('utf-8')
    b64_svg = base64.b64encode(svg_bytes).decode('utf-8')
    stamp_payload = f"data:image/svg+xml;base64,{b64_svg}"
    
    print("\n✅ GENESIS STAMP GENERATED!")
    print(f"📦 Payload Size: {len(stamp_payload)} bytes ({len(stamp_payload)/1024:.2f} KB)")
    print("   (Perfect size for a standard Bitcoin Stamp)")
    
    # 5. Save Artifacts
    output_dir = script_dir / OUTPUT_DIR
    output_dir.mkdir(exist_ok=True)
    
    # Save SVG for preview
    with open(output_dir / "genesis_stamp.svg", "w") as f:
        f.write(svg)
    
    # Save Base64 for broadcasting
    with open(output_dir / "broadcast_payload.txt", "w") as f:
        f.write(stamp_payload)
        
    print(f"\n📂 Artifacts saved to: {output_dir}/")
    print("   - genesis_stamp.svg (Preview this in your browser)")
    print("   - broadcast_payload.txt (Copy this string to Stampchain/Freewallet)")
    
    print("\n🚀 EXECUTION INSTRUCTIONS:")
    print("1. Go to https://stampchain.io (or OpenStamp/Freewallet)")
    print("2. Choose 'Mint Stamp' or 'Upload Image'")
    print("3. UPLOAD the 'genesis_stamp.svg' file")
    print("   OR paste the contents of 'broadcast_payload.txt' if supported")
    print("4. Pay the BTC fee (~$15)")
    print("5. TWEET the resulting Transaction ID!")

if __name__ == "__main__":
    main()
