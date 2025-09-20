import os
import hashlib
import json
from ecdsa import SigningKey, SECP256k1

WALLET_DIR = "wallets"

def generate_wallet():
    # Create a new ECDSA keypair
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.get_verifying_key()
    address = hashlib.sha256(vk.to_string()).hexdigest()
    wallet = {
        "address": address,
        "private_key": sk.to_pem().decode(),
        "public_key": vk.to_pem().decode()
    }
    save_wallet(wallet)
    return wallet

def save_wallet(wallet):
    if not os.path.exists(WALLET_DIR):
        os.makedirs(WALLET_DIR)
    with open(f"{WALLET_DIR}/{wallet['address']}.json", "w") as f:
        f.write(json.dumps(wallet))

def load_wallet(address):
    try:
        with open(f"{WALLET_DIR}/{address}.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def sign_transaction(private_key_pem, transaction):
    sk = SigningKey.from_pem(private_key_pem)
    tx_string = json.dumps(transaction, sort_keys=True)
    signature = sk.sign(tx_string.encode()).hex()
    return signature

def verify_transaction_signature(public_key_pem, transaction, signature):
    from ecdsa import VerifyingKey
    vk = VerifyingKey.from_pem(public_key_pem)
    tx_string = json.dumps(transaction, sort_keys=True)
    try:
        return vk.verify(bytes.fromhex(signature), tx_string.encode())
    except Exception:
        return False

def validate_address(address):
    return isinstance(address, str) and len(address) == 64 and all(c in "0123456789abcdef" for c in address)