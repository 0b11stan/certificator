# certificator

A simple web API to manage a certification authority in your AD domain.

- The linux server running certificator should belong to your AD.
- You should have an intermediate CA certificate signed by you AD under a directory called secret.
- The secret directory under your project's root :\
├── intermediate.cert (your CA certificate)\
├── intermediate.key (your CA private key)\
└── passphrase (the passphrase of your private key)

The usage workflow of certificator api (with a user called john macclane) :
```bash
# create a temporary csr
openssl req -new -newkey rsa:2048 -nodes \
    -keyout /tmp/certificator/ctor.key \
    -out /tmp/certificator/ctor.csr

# get a common user token
curl \
    -H "Content-Type: application/json" \
    -d '{"username":"john.macclane","password":"P@ssw0rd"}' \
    -X POST http://localhost:8080/auth

# push a csr on the platform
curl \
    -H "Authorization: JWT $TOKEN" \
    -d "$(cat /tmp/certificator/ctor.csr)" \
    -X POST http://localhost:8080/cert

# get an administrator token
curl \
    -H "Content-Type: application/json" \
    -d '{"username":"Administrator","password":"P@ssw0rd"}' \
    -X POST http://localhost:8080/auth

# list pending csr
curl \
    -H "Authorization: JWT $TOKEN" \
    -X GET http://localhost:8080/cert?filter=PENDING

# request a csr details
curl \
    -H "Authorization: JWT $TOKEN" \
    -X GET http://localhost:8080/cert/$CERTID

# validate a csr
curl \
    -H "Authorization: JWT $TOKEN" \
    -X POST http://localhost:8080/cert/$CERTID

```

## Done :

| Method | Route        | Query           | Data       | Description                              |
| ------ | ------------ | --------------- | ---------- | ---------------------------------------- |
| GET    | /cert        |                 |            | List all certificates                    |
| GET    | /cert        | ?filter=PENDING |            | List pending certificate signin requests |
| GET    | /cert        | ?filter=ISSUED  |            | List delivered certificates              |
| GET    | /cert        | ?filter=REVOKED |            | List revoked certificates                |
| POST   | /cert        |                 | `<base64>` | Add a new certificate request            |
| POST   | /cert/`<id>` |                 |            | Validate the certificate                 |
| GET    | /cert/`<id>` |                 |            | Show certificate Details                 |

