from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization
import datetime

# Generate a new private key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

# Generate a certificate signing request (CSR)
csr_builder = x509.CertificateSigningRequestBuilder()
csr_builder = csr_builder.subject_name(x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, 'Rohaan'),
    # Add any additional fields as needed, such as organization, country, etc.
]))
csr = csr_builder.sign(private_key, hashes.SHA256())

# Generate a self-signed certificate using the CSR
cert_builder = x509.CertificateBuilder()
cert_builder = cert_builder.subject_name(csr.subject)
cert_builder = cert_builder.issuer_name(csr.subject)
cert_builder = cert_builder.public_key(csr.public_key())
cert_builder = cert_builder.serial_number(x509.random_serial_number())
cert_builder = cert_builder.not_valid_before(datetime.datetime.utcnow())
cert_builder = cert_builder.not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
cert_builder = cert_builder.add_extension(
    x509.BasicConstraints(ca=False, path_length=None), critical=True
)
certificate = cert_builder.sign(private_key, hashes.SHA256())

# Save the private key to a file
private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
with open('certs/server_key.pem', 'wb') as f:
    f.write(private_key_pem)

# Save the certificate to a file
certificate_pem = certificate.public_bytes(serialization.Encoding.PEM)
with open('certs/server_cert.pem', 'wb') as f:
    f.write(certificate_pem)