import os
import sys
from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes

sertificate_dir = "sertificate"

with open(os.path.join(sertificate_dir, "certificate.pem"), "rb") as f:
    certificate = x509.load_pem_x509_certificate(f.read())
    public_key = certificate.public_key()

session_key = os.urandom(32)

encrypted_session_key = public_key.encrypt(
    session_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

filename = sys.argv[1]

try:
    with open(filename, "rb") as f:
        plaintext = f.read()
except FileNotFoundError:
    print(f"File {filename} not found")
    sys.exit(1)

iv = os.urandom(12)

aesgcm = AESGCM(session_key)
ciphertext = aesgcm.encrypt(iv, plaintext, None)

with open("encrypted_" + filename + ".bin", "wb") as f:
    f.write(iv + encrypted_session_key + ciphertext)
