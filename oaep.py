import hashlib
import os
from math import ceil
from rsa import encrypt_rsa, decrypt_rsa, gen_keys_pair

def sha1(b_message):
    return hashlib.sha1(b_message).digest()

def i2osp(x, xlen):
    return x.to_bytes(xlen, 'big')

def os2ip(x):
    return int.from_bytes(x, 'big')

def mgf1(seed, mlen):
    hlen = len(sha1(b''))
    return b''.join(sha1(seed + i2osp(c, 4)) for c in range(0, ceil(mlen / hlen)))[:mlen]

def xor(data, mask):
    return bytes((d ^ m) for d, m in zip(data, mask))

def oaep_encode(b_message, k, label=b''):
    db = sha1(label) + b'\x00' * (k - len(b_message) - 2 * len(sha1(label)) - 2) + b'\x01' + b_message
    seed = os.urandom(len(sha1(label)))
    db_mask = mgf1(seed, k - len(sha1(label)) - 1)
    masked_db = xor(db, db_mask)
    seed_mask = mgf1(masked_db, len(sha1(label)))
    masked_seed = xor(seed, seed_mask)
    return b'\x00' + masked_seed + masked_db

def oaep_decode(ciphertext, k, label=b''):
    masked_seed, masked_db = ciphertext[1:1 + len(sha1(label))], ciphertext[1 + len(sha1(label)):]
    seed_mask = mgf1(masked_db, len(sha1(label)))
    seed = xor(masked_seed, seed_mask)
    db_mask = mgf1(seed, k - len(sha1(label)) - 1)
    db = xor(masked_db, db_mask)
    for i in range(len(sha1(label)), len(db)):
        if db[i] == 0:
            continue
        elif db[i] == 1:
            break

    return db[i + 1:]

def encrypt_oaep(b_message, public_key):
    n, _ = public_key
    k = (n.bit_length() + 7) // 8
    return i2osp(encrypt_rsa(os2ip(oaep_encode(b_message, k)), public_key), k)

def decrypt_oaep(ciphertext, private_key):
    n, _ = private_key
    k = (n.bit_length() + 7) // 8
    return oaep_decode(i2osp(decrypt_rsa(os2ip(ciphertext), private_key), k), k)

if __name__ == "__main__":
    public_key, private_key = gen_keys_pair()
    message = "teste de mensagem"
    b_message = message.encode('utf-8')
    ciphertext = encrypt_oaep(b_message, public_key)
    print(ciphertext)
    plaintext = decrypt_oaep(ciphertext, private_key)
    print(plaintext)