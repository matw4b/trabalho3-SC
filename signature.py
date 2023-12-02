import base64
from hashlib import sha3_256
from rsa import encrypt_rsa, decrypt_rsa

def encode_base64(signature):
    return base64.b64encode(signature).decode("ascii")

def decode_base64(signature):
    return base64.b64decode(signature)

def signature(message, public_key):
    hashed = sha3_256(message.encode('utf-8')).digest()
    signature = encrypt_rsa(int.from_bytes(hashed, "big"), public_key)
    signature_bytes = signature.to_bytes((signature.bit_length() + 7) // 8, 'big')
    return encode_base64(signature_bytes)

def verify_signature(signature, message, private_key):
    signature = decode_base64(signature)
    hashed = sha3_256(message).digest()
    if decrypt_rsa(int.from_bytes(signature, "big"), private_key) == int.from_bytes(hashed, "big"):
        print("assinatura válida :)")
    else:
        print("assinatura inválida :(")
