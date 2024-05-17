import os
import sys
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

sertificate_dir = "sertificate"

with open(os.path.join(sertificate_dir, "private_key.pem"), "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None,
    )

filename = sys.argv[1]
cleared_filename = filename[10:-4]

try:
    with open(filename, "rb") as f:
        data = f.read()
except FileNotFoundError:
    print(f"File {filename} not found")
    sys.exit(1)

iv = data[:12]
encrypted_session_key = data[12:12+256]
ciphertext = data[12+256:]

session_key = private_key.decrypt(
    encrypted_session_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

aesgcm = AESGCM(session_key)
plaintext = aesgcm.decrypt(iv, ciphertext, None)

with open("decrypted_" + cleared_filename, "wb") as f:
    f.write(plaintext)
