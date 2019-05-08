# certificator

A simple web API to manage a certification authority in your AD domain.

- The linux server running certificator should belong to your AD.
- You should have an intermediate CA certificate signed by you AD under a directory called secret.
- The secret directory under your project's root :
secret/\
├── intermediate.cert (your CA certificate)\
├── intermediate.key (your CA private key)\
└── passphrase (the passphrase of your private key)

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

