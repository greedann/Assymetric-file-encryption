import os
import sys
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidTag


def decrypt_file(filename):
    cleared_filename = filename[:-14]

    try:
        with open(filename, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        print(f"File {filename} not found")
        sys.exit(1)

    # get data from file
    iv = data[:12]
    encrypted_session_key = data[12:12+256]
    salt = data[12+256:12+256+16]
    backup_ciphertext = data[12+256+16:12+256+16+48]
    ciphertext = data[12+256+16+48:]

    try:
        # get private key from certificate
        while True:
            print("Select option: ")
            print("1. Load private key from file")
            print("2. Input private key to console")
            answer = input("Option: ")
            if answer in ["1", "2"]:
                break
            else:
                print("Invalid option")
        if answer == "1":
            certificate_dir = input("Input path to private key file: \n")
            with open(certificate_dir, "rb") as f:
                private_key = serialization.load_pem_private_key(
                    f.read(),
                    password=None,
                )
        elif answer == "2":
            print("Input private key in PEM format")
            key_str = ""
            while True:
                line = input()
                key_str += line + "\n"
                if "END RSA PRIVATE KEY" in line:
                    break

            private_key = serialization.load_pem_private_key(
                key_str.encode(),
                password=None,
            )
        session_key = private_key.decrypt(
            encrypted_session_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except FileNotFoundError:
        # if private key not found, ask for password
        print(f"Private key not found")
        password = input("Input password to restore data: ").encode()
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
            backend=default_backend()
        )

        key_backup = kdf.derive(password)

        aesgcm = AESGCM(key_backup)
        try:
            session_key = aesgcm.decrypt(salt, backup_ciphertext, None)
        except InvalidTag:
            print("Wrong password")
            sys.exit(1)

    # decrypt file
    aesgcm = AESGCM(session_key)
    plaintext = aesgcm.decrypt(iv, ciphertext, None)

    with open(cleared_filename, "wb") as f:
        f.write(plaintext)

    return cleared_filename


if __name__ == "__main__":
    filename = sys.argv[1]
    decrypt_file(filename)
