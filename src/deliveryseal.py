#!/usr/bin/env python3
"""
DeliverySeal — Local-first material delivery, receipt, and quantity verification evidence sealer.
Offline. Deterministic. Pay once.
Compatible with QuantumGuard CONTRACT-v1.
"""

import argparse
import json
import hashlib
import base64
import os
from datetime import datetime, timezone
from pathlib import Path

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    CRYPTO = True
except ImportError:
    CRYPTO = False

CONTRACT_VERSION = "1"
ALG = "ed25519"

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def load_or_generate_key(key_path: str = "deliveryseal_key.pem"):
    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            priv = serialization.load_pem_private_key(f.read(), password=None)
        return priv
    if not CRYPTO:
        raise SystemExit("cryptography package required for signing. pip install cryptography")
    priv = ed25519.Ed25519PrivateKey.generate()
    pem = priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open(key_path, "wb") as f:
        f.write(pem)
    print(f"Generated new key: {key_path}")
    return priv

def get_public_key_hex(priv):
    pub = priv.public_key()
    raw = pub.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return raw.hex()

def sign_payload(priv, payload_hash: bytes) -> str:
    sig = priv.sign(payload_hash)
    return sig.hex()

def build_payload(record: dict) -> bytes:
    # Canonical JSON for determinism
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return canonical

def seal_record(record: dict, priv, out_path: str):
    payload = build_payload(record)
    payload_hash = hashlib.sha256(payload).digest()
    payload_hash_hex = payload_hash.hex()
    signature = sign_payload(priv, payload_hash)
    public_key = get_public_key_hex(priv)

    bundle = {
        "version": CONTRACT_VERSION,
        "payload": base64.b64encode(payload).decode("ascii"),
        "payload_hash": payload_hash_hex,
        "signature": signature,
        "public_key": public_key,
        "alg": ALG,
    }
    with open(out_path, "w") as f:
        json.dump(bundle, f, indent=2)
    print(f"Sealed delivery record written to {out_path}")
    print(f"Verify with: qg verify {out_path}")

def demo_record():
    return {
        "type": "delivery_receipt",
        "job_id": "JOB-2026-042",
        "site": "Site Alpha — Springfield, MO",
        "po_number": "PO-2026-1187",
        "ticket": "DEL-88421",
        "supplier": "Midwest Materials Co.",
        "received_at": "2026-11-13T09:45:00Z",
        "receiver": "Operator A",
        "items": [
            {
                "sku": "CONDUIT-2IN",
                "description": "2\" EMT Conduit",
                "qty_ordered": 50,
                "qty_received": 48,
                "unit": "sticks",
                "condition": "2 sticks damaged ends — noted on ticket"
            },
            {
                "sku": "COUPLING-2IN",
                "description": "2\" EMT Couplings",
                "qty_ordered": 50,
                "qty_received": 50,
                "unit": "ea",
                "condition": "Good"
            }
        ],
        "notes": "Driver waited 10 min. Partial short on conduit noted. Photo of damage taken (hash below).",
        "media_hashes": ["a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456"],
        "sealed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tool": "DeliverySeal/0.1.0"
    }

def main():
    parser = argparse.ArgumentParser(description="DeliverySeal — seal delivery receipts into QuantumGuard packs.")
    parser.add_argument("--demo", action="store_true", help="Run demo and seal sample record")
    parser.add_argument("--json", help="Path to JSON delivery record file to seal")
    parser.add_argument("--out", default="sealed-delivery.json", help="Output sealed bundle path")
    parser.add_argument("--key", default="deliveryseal_key.pem", help="Path to Ed25519 private key PEM")
    args = parser.parse_args()

    if args.demo:
        record = demo_record()
        print("Demo record:")
        print(json.dumps(record, indent=2))
    elif args.json:
        with open(args.json) as f:
            record = json.load(f)
    else:
        parser.print_help()
        return

    priv = load_or_generate_key(args.key)
    seal_record(record, priv, args.out)

if __name__ == "__main__":
    main()
