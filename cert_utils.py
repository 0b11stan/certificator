def get_pending_cert(cert_id):
    csr_file = open("certificates/pending/{}.csr".format(cert_id), "r")
    file_content = csr_file.read()
    return OpenSSL.crypto.load_certificate_request(FILETYPE_PEM, file_content)


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
    cert = crypto.X509()
    #cert.set_serial_number(serial_no)
    #cert.gmtime_adj_notBefore(notBeforeVal)
    #cert.gmtime_adj_notAfter(notAfterVal)
    cert.set_issuer(ca_cert.get_subject())
    cert.set_subject(client_csr.get_subject())
    cert.set_pubkey(client_csr.get_pubkey())
    cert.sign(ca_private_key, "sha256")
    return cert
