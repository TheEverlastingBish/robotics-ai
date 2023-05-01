import sys
import math
import json
import random
import sympy as sp
from sympy import ntheory as nt
import helper as hp


PLAINTEXT = """The journey doesn't end here. Death is just another path, one that we all must take. 
The grey rain-curtain of this world rolls back, and all turns to silver glass, and then you see it. 
White shores, and beyond, a far green country under a swift sunrise.
"""

def main():
    print("Original Message Text:\n", PLAINTEXT)
    print("Original Message Length:", len(PLAINTEXT))

    chunksize = 10
    chunks = hp.chunky(PLAINTEXT, chunksize)
    print(chunks)

    print("\nCombined String Check:\n", ''.join(chunks))

    byte_encoded_message = []
    for chunk in chunks:
        for c in chunk:
            byte_encoded_message.extend(c.encode('ascii'))

    print(byte_encoded_message)

    keys = hp.generate_keys()
    priv = keys['privateKey']
    pub = keys['publicKey']
    print("Private Key:", keys['privateKey'].__dict__)
    print("Public Key :", keys['publicKey'].__dict__)

    encrypted_str = hp.encrypt(pub, byte_encoded_message)
    print("\nEncrypted Message:\n", encrypted_str)

    decrypted_str = hp.decrypt(priv, encrypted_str)
    print("\nDecrypted Message:\n", decrypted_str)
    print("Decrypted Message Length:", len(decrypted_str))

if __name__ == '__main__':
    main()

