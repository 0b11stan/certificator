# certificator

NOT PROD READY : this project is under heavy developement

A simple web API to manage a certification authority in your AD domain.

- The linux server running certificator should belong to your AD.
- You sould have an intermediate certificate signed by you AD.

## Done :

| Method | Route | Query           | Data       | Description                              |
| ------ | ----- | --------------- | ---------- | ---------------------------------------- |
| GET    | /cert |                 |            | List all certificates                    |
| GET    | /cert | ?filter=PENDING |            | List pending certificate signin requests |
| GET    | /cert | ?filter=ISSUED  |            | List delivered certificates              |
| GET    | /cert | ?filter=REVOKED |            | List revoked certificates                |
| POST   | /cert |                 | `<base64>` | Add a new certificate request            |

## Todo :

- CLI pour lister les csr
- CLI pour délivrer les certificats
- WEB pour révoker des certificats
