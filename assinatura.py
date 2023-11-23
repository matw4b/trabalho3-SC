'''
Parte II: Assinatura
1. Cálculo de hashes da mensagem em claro (função de hash SHA-3)
2. Assinatura da mensagem (cifração do hash da mensagem)
3. Formatação do resultado (caracteres especiais e informações para verificação em BASE64)
'''

import base64
import hashlib

def calculate_hash(message):
    return hashlib.sha3_256(message.encode('utf-8')).digest()

def sign_message(hash_message, private_key):
    hash_number = int.from_bytes(hash_message, 'big')
    signature = pow(hash_number, private_key[1], private_key[0])
    signature_bytes = signature.to_bytes((signature.bit_length() + 7) // 8, 'big')
    return signature_bytes

def format_base64(signature):
    return base64.b64encode(signature).decode('utf-8')

if __name__ == "__main__":
    message = "teste de mensagem"
    private_key = (123456789, 1234567890)
    hash_message = calculate_hash(message)
    signature = sign_message(hash_message, private_key)
    signature_base64 = format_base64(signature)
    print("Assinatura da mensagem:", signature_base64)