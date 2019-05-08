import OpenSSL.crypto
from OpenSSL.crypto import FILETYPE_PEM

def get_pending_cert(cert_id):
    csr_file = open("certificates/pending/{}.csr".format(cert_id), "r")
    file_content = csr_file.read()
    return OpenSSL.crypto.load_certificate_request(FILETYPE_PEM, file_content)


def issue_cert(cert_id):
    csr_path = "certificates/issued/{}.cer".format(cert_id)
    cert = create_certificate(
        get_ca_private_key(), get_ca_cert(), get_pending_cert(cert_id)
    )
    cert_buffer = OpenSSL.crypto.dump_certificate(FILETYPE_PEM, cert)
    cert_file = open(csr_path, "w")
    cert_file.write(str(cert_buffer))
    cert_file.close()
    os.remove(csr_path)


def read(path):
    file_content = open(path, "r")
    return file_content.read().strip()


def read_secret_passphrase():
    return read("../secret/passphrase")


def read_secret_key():
    return read("../secret/intermediate.key")


def read_secret_cert():
    return read("../secret/intermediate.cert")


def get_ca_private_key():
    # TODO : use a callback to get passphrase, avoiding memory dump
    secret = read_secret_passphrase().encode('utf-8')
    return OpenSSL.crypto.load_privatekey(FILETYPE_PEM, read_secret_key(), passphrase=secret)


def get_ca_cert():
    return OpenSSL.crypto.load_certificate(FILETYPE_PEM, read_secret_cert())


def detail_csr(csr):
    key = csr.get_pubkey()
    subject = csr.get_subject()
    algorithm = 'RSA' if key.type() == OpenSSL.crypto.TYPE_RSA else None
    size = key.bits()
    details = {}

    for key, val in dict(subject.get_components()).items():
        details[key.decode()] = val.decode()

    return {
        "algorithm": algorithm,
        "size": size,
        "details": {
            "CN": details["CN"],
            "O": details["O"],
            "OU": details["OU"],
            "L": details["L"],
            "ST": details["ST"],
            "C": details["C"],
            "MAIL": details["emailAddress"],
        }
    }


def create_certificate(ca_private_key, ca_cert, client_csr):
    cert = OpenSSL.crypto.X509()
    #cert.set_serial_number(serial_no)
    #cert.gmtime_adj_notBefore(notBeforeVal)
    #cert.gmtime_adj_notAfter(notAfterVal)
    cert.set_issuer(ca_cert.get_subject())
    cert.set_subject(client_csr.get_subject())
    cert.set_pubkey(client_csr.get_pubkey())
    cert.sign(ca_private_key, "sha256")
    return cert
