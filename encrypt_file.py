import os
import sys
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend

certificate_dir = "certificate"


def encrypt_file(filename, separate_key=False):
    # getting public key from certificate
    with open(os.path.join(certificate_dir, "certificate.pem"), "rb") as f:
        certificate = x509.load_pem_x509_certificate(f.read())
        public_key = certificate.public_key()

    session_key = os.urandom(32)

    # encrypt session key with public key
    encrypted_session_key = public_key.encrypt(
        session_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    ans = input("Do you want to add a password to restore the file? (y/n): ")
    if ans in ["y", "Y", "Yes", "yes"]:
        # encrypt session key with password from user
        password = input("Enter password: ").encode()
        salt = os.urandom(16)
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
            backend=default_backend()
        )
        backup_key = kdf.derive(password)
        aesgcm = AESGCM(backup_key)
        backup_ciphertext = aesgcm.encrypt(salt, session_key, None)
    else:
        salt = os.urandom(16)
        backup_ciphertext = os.urandom(48)

    try:
        with open(filename, "rb") as f:
            plaintext = f.read()
    except FileNotFoundError:
        print(f"File {filename} not found")
        sys.exit(1)

    iv = os.urandom(12)

    # encrypt file
    aesgcm = AESGCM(session_key)
    ciphertext = aesgcm.encrypt(iv, plaintext, None)

    if separate_key:
        with open(filename + "_encrypted" + ".key", "wb") as f:
            f.write(iv + encrypted_session_key + salt + backup_ciphertext + ciphertext[:16])
        with open(filename + "_encrypted" + ".bin", "wb") as f:
            f.write(ciphertext[16:])
        return (filename + "_encrypted" + ".bin", filename + "_encrypted" + ".key")
    else:
        with open(filename + "_encrypted" + ".bin", "wb") as f:
            f.write(iv + encrypted_session_key + salt + backup_ciphertext + ciphertext)
        return filename + "_encrypted" + ".bin"
    

if __name__ == "__main__":
    filename = sys.argv[1]
    encrypt_file(filename)
