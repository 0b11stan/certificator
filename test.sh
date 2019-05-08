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


