def detail_certificate(cert_id):
    csr_file = open("certificates/pending/{}.csr".format(cert_id), "r")
    file_content = csr_file.read()
    req = OpenSSL.crypto.load_certificate_request(FILETYPE_PEM, file_content)
    key = req.get_pubkey()
    subject = req.get_subject()
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

