import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Function to generate a random key for AES encryption (16 bytes for AES-128)
def generate_key():
    return os.urandom(16)

# Function to encrypt a file using AES encryption
def encrypt_file(file_path, key):
    # Generate a random IV (initialization vector)
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Read the file content
    with open(file_path, 'rb') as f:
        file_data = f.read()

    # Encrypt the file content
    encrypted_data = encryptor.update(file_data) + encryptor.finalize()

    # Save the encrypted file with the .enc extension
    encrypted_file_path = file_path + '.enc'
    with open(encrypted_file_path, 'wb') as enc_file:
        enc_file.write(iv + encrypted_data)

    return encrypted_file_path

# Function to decrypt an encrypted file using AES
def decrypt_file(encrypted_file_path, key):
    with open(encrypted_file_path, 'rb') as enc_file:
        iv = enc_file.read(16)  # Read the IV
        encrypted_data = enc_file.read()  # Read the encrypted data

    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the file content
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Save the decrypted file by removing the '.enc' extension
    decrypted_file_path = encrypted_file_path.replace('.enc', '_decrypted')
    with open(decrypted_file_path, 'wb') as dec_file:
        dec_file.write(decrypted_data)

    return decrypted_file_path
