from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import os
from pathlib import Path
import sys

def derive_key(passphrase: str, salt: bytes) -> bytes:
    return PBKDF2(passphrase, salt, dkLen=32, count=1000)

def encrypt_file(file_path: str, passphrase: str) -> str:
    salt = get_random_bytes(16)
    key = derive_key(passphrase, salt)
    cipher = AES.new(key, AES.MODE_GCM)
    with open(file_path, 'rb') as file:
        file_data = file.read()
    ciphertext, tag = cipher.encrypt_and_digest(file_data)
    encrypted_file_path = file_path + '.enc'
    with open(encrypted_file_path, 'wb') as file:
        file.write(salt + cipher.nonce + tag + ciphertext)
    return encrypted_file_path

def decrypt_file(encrypted_file_path: str, passphrase: str) -> str:
    with open(encrypted_file_path, 'rb') as file:
        salt, nonce, tag, ciphertext = [file.read(x) for x in (16, 16, 16, -1)]
    key = derive_key(passphrase, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    decrypted_file_path = encrypted_file_path.rstrip('.enc')
    with open(decrypted_file_path, 'wb') as file:
        file.write(decrypted_data)
    return decrypted_file_path

def secure_delete(file_path: str):
    with open(file_path, 'ba+') as file:
        length = file.tell()
        file.seek(0)
        file.write(os.urandom(length))
    os.remove(file_path)

def print_ascii_art():
    ascii_art = """
██████╗ ██╗   ██╗ ██████╗██████╗ ██╗   ██╗██████╗ ████████╗
██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗╚██╗ ██╔╝██╔══██╗╚══██╔══╝
██████╔╝ ╚████╔╝ ██║     ██████╔╝ ╚████╔╝ ██████╔╝   ██║   
██╔═══╝   ╚██╔╝  ██║     ██╔══██╗  ╚██╔╝  ██╔═══╝    ██║   
██║        ██║   ╚██████╗██║  ██║   ██║   ██║        ██║   
╚═╝        ╚═╝    ╚═════╝╚═╝  ╚═╝   ╚═╝   ╚═╝        ╚═╝   
    """
    print(ascii_art)

def is_restricted_directory(directory):
    restricted_paths = [
        Path.home(),  
        Path('/')    
    ]
    if os.name == 'nt':
        restricted_paths.append(Path('C:\\')) 
    return Path(directory).resolve() in restricted_paths

def process_directory(directory, action, passphrase=None):
    if is_restricted_directory(directory):
        print(f"error: the directory {directory} is restricted.")
        return
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if action == 'encrypt':
                    encrypted_file = encrypt_file(file_path, passphrase)
                    secure_delete(file_path)
                    print(f"file encrypted: {encrypted_file}")
                elif action == 'decrypt':
                    decrypted_file = decrypt_file(file_path, passphrase)
                    print(f"file decrypted: {decrypted_file}")
                elif action == 'delete':
                    secure_delete(file_path)
                    print(f"file securely deleted: {file_path}")
            except Exception as e:
                print(f"an error occurred with {file_path}: {e}")

def main():
    print_ascii_art()
    action = None
    while action != 'exit':
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            print(f"file or directory provided: {file_path}")
            sys.argv = sys.argv[:1] 
        else:
            file_path = input("enter the path of the file or directory: ")

        if not action:
            action = input("enter 'encrypt', 'decrypt', 'delete', or 'exit': ").lower()
        
        if action in ['encrypt', 'decrypt', 'delete']:
            passphrase = input("enter passphrase: ") if action in ['encrypt', 'decrypt'] else None

        if os.path.isdir(file_path):
            process_directory(file_path, action, passphrase)
        elif os.path.isfile(file_path):
            try:
                if action == 'encrypt':
                    encrypted_file = encrypt_file(file_path, passphrase)
                    secure_delete(file_path)
                    print(f"file encrypted to {encrypted_file}")
                elif action == 'decrypt':
                    decrypted_file = decrypt_file(file_path, passphrase)
                    print(f"file decrypted to {decrypted_file}")
                elif action == 'delete':
                    secure_delete(file_path)
                    print(f"file securely deleted: {file_path}")
            except Exception as e:
                print(f"an error occurred: {e}")
        else:
            print("invalid path or action. please try again.")

        if action != 'exit':
            continue_action = input("another? (yes/no): ").lower()
            if continue_action != 'yes':
                action = 'exit'

if __name__ == "__main__":
    main()
