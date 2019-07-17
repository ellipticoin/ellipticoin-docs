The Ellipitcoin API
===================
The Ellipticoin API runs on top of HTTP and is designed to be a simple as
possible without being any simpler. Parameters are encoded with [CBOR](http://cbor.io/) and the
resulting binary is encoded into hexadecimal format when necessary.


### Authentication

All state changing methods (POST and PUT requests) must have the following Authorization Header:

    Authorization: Signature <hex encoded public key> <hex encoded signature> <hex encoded nonce>

|Key| Value|
|----------|-------------------------------------------------------------|
|Public Key| The public key of the account your signing from. |
|Signature| The [Ed25519](https://ed25519.cr.yp.to/) signature of the message. |
|Nonce| The [nonce](https://en.wikipedia.org/wiki/Nonce) of the account you're sending from.|


### Deploy a new contract

Deploys a wasm binary contract to the specified name and address.

    PUT /:address/:contract_name  
    Body: {
            code: <WASM binary>,
            params: [<constructor params>],
          }

### Call a state changing contract function

    POST /:address/:contract_name  
    Body : {
      method: <method>,
      params: [<params>]
    }

### Call to a read-only contract function

Read-only contract functions don't update state and therefore don't need to be
considered in consensus. These functions are free and should be run by edge
nodes. Note: the CBOR encoded parameters must be encoded as hex because http
[doesn't support raw binary in URLs](https://stackoverflow.com/a/1892044/1356670).

    GET /:address/:contract?<{method: <method>, params: [<params>]} encoded as hex>
