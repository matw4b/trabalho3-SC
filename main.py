from rsa import gen_keys_pair
from signature import signature, verify_signature
from oaep import encrypt_oaep, decrypt_oaep

message = input("Digite uma mensagem: ")

# gen_keys_pair retorna --> ((n, e), (n,d))
public_key, private_key = gen_keys_pair()

print("\nMensagem Original: ", message)

signature = signature(message, public_key)

print(f"\nAssinatura: {signature}")

ciphertext = encrypt_oaep(message.encode('utf-8'), public_key)
print("\nMensagem Cifrada: ", ciphertext)

plaintext = decrypt_oaep(ciphertext, private_key)

print("\nMensagem Decifrada: ", plaintext.decode('utf-8'))

print("\nResultado da verificacao da assinatura:")
verify_signature(signature, plaintext, private_key)