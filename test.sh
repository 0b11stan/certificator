# get token
curl \
    -H "Content-Type: application/json" \
    -d '{"username":"john.macclane","password":"P@ssw0rd"}' \
    -X POST http://localhost:8080/auth

# add csr
curl \
    -H "Authorization: JWT $TOKEN" \
    -d "$(cat /tmp/test/test.csr)" \
    -X POST http://localhost:8080/cert

# list csr
curl \
    -H "Authorization: JWT $TOKEN" \
    -X GET http://localhost:8080/cert?filter=PENDING

# request csr details
curl \
    -H "Authorization: JWT $TOKEN" \
    -X GET http://localhost:8080/cert/$CERTID


