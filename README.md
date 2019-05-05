GET /cert
    /cert?filter=PENDING
    /cert?filter=ISSUED
    /cert?filter=REVOKED

POST /cert --data '{"request":"<base64certificate>"}'
