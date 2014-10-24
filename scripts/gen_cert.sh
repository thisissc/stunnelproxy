#!/bin/sh

set -x

mkdir `date "+%Y%m%d"`
cd `date "+%Y%m%d"`

openssl req -days 365 -out ca.pem -new -x509
echo '00' > file.srl

openssl genrsa -out server.key 1024
openssl req -days 365 -key server.key -new -out server.req
openssl x509 -req -in server.req -CA ca.pem -CAkey privkey.pem -CAserial file.srl -out server.pem

openssl genrsa -out client.key 1024
openssl req -days 365 -key client.key -new -out client.req
openssl x509 -req -in client.req -CA ca.pem -CAkey privkey.pem -CAserial file.srl -out client.pem
