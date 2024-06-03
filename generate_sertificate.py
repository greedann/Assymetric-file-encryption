import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from datetime import datetime, timedelta
from sslib import shamir


certificate_dir = "certificate"

# check if the certificate directory exists
if not os.path.exists(certificate_dir):
    os.makedirs(certificate_dir)

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)

ans = input("Do you want to split the private key? (y/n): ")
if ans in ["y", "Y", "Yes", "yes"]:
    required_shares = int(input("Enter the number of required shares: "))
    distributed_shares = int(input("Enter the number of distributed shares: "))
    # get private key bytes
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption())
    # split the private key
    data = shamir.split_secret(
        private_key_bytes, required_shares, distributed_shares)
    # save shares
    for idx, share in data['shares']:
        with open(f"{certificate_dir}/share_{idx}.key", "wb") as f:
            f.write(share)
    print("Private key has been split")

subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "PL"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Pomorskie"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Gdansk"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Politechnika Gdanska"),
    x509.NameAttribute(NameOID.COMMON_NAME, "pg.edu.pl"),
])

certificate = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(private_key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.now())
    .not_valid_after(datetime.now() + timedelta(days=365))
    .add_extension(
        x509.SubjectAlternativeName([x509.DNSName("pg.edu.pl")]),
        critical=False,
    )
    .sign(private_key, hashes.SHA256())
)

if not os.path.exists(certificate_dir):
    os.makedirs(certificate_dir)

with open(os.path.join(certificate_dir, "private_key.pem"), "wb") as f:
    f.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
    )

with open(os.path.join(certificate_dir, "certificate.pem"), "wb") as f:
    f.write(
        certificate.public_bytes(serialization.Encoding.PEM)
    )
