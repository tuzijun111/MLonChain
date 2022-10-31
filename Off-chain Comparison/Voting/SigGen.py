import errno

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

message = b'This message is from me, I promise.'

def Signature_gen():
    try:
        with open('privkey.pem', 'r') as f:
            key = RSA.importKey(f.read())
    except IOError as e:
        if e.errno != errno.ENOENT:
            raise
        # No private key, generate a new one. This can take a few seconds.
        key = RSA.generate(4096)
        with open('privkey.pem', 'wb') as f:
            f.write(key.exportKey('PEM'))
        with open('pubkey.pem', 'wb') as f:
            f.write(key.publickey().exportKey('PEM'))

    hasher = SHA256.new(message)
    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(hasher)
    return signature

def Verify(signature):
    with open('pubkey.pem', 'rb') as f:
        key = RSA.importKey(f.read())
    hasher = SHA256.new(message)
    verifier = PKCS1_v1_5.new(key)
    if verifier.verify(hasher, signature):
        print('Nice, the signature is valid!')
    else:
        print('No, the message was signed with the wrong private key or modified')

if __name__ =='__main__':
    x = Signature_gen()
    Verify(x)
