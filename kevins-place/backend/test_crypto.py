from coincurve import PrivateKey, PublicKey, PublicKeyXOnly
import hashlib

print("Testing coincurve Schnorr with PublicKeyXOnly...")

msg = b"hello"
msg_hash = hashlib.sha256(msg).digest()
priv = PrivateKey()

# Get x-only pubkey
pub_xonly = PublicKeyXOnly(priv.public_key.format(compressed=True)[1:]) 
# OR just from the private key directly if supported?

sig = priv.sign_schnorr(msg_hash)
print(f"Sig len: {len(sig)}")

try:
    # verify(signature, message) - message here usually means the digest! 
    # check docstring if possible? no.
    ret = pub_xonly.verify(sig, msg_hash)
    print(f"Verify result: {ret}")
except Exception as e:
    print(f"Verify failed: {e}")
