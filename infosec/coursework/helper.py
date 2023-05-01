import sys
import math
import random
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Tuple
import sympy as sp
from sympy import ntheory as nt


class PrivateKey(object):
    def __init__(self, p=None, g=None, x=None, iNumBits=0):
        self.p = p
        self.g = g
        self.x = x
        self.iNumBits = iNumBits

class PublicKey(object):
    def __init__(self, p=None, g=None, h=None, iNumBits=0):
        self.p = p
        self.g = g
        self.h = h
        self.iNumBits = iNumBits


def find_prime():
    rand_prime = nt.generate.randprime(10e19, 10e20)
    # print("Random Prime:", rand_prime)

    p = sp.nextprime(rand_prime)
    # print("Next Prime:", p)

    return p


def primitive_root(p: int, alpha: int) -> int:
    """Finding the primitove root of a prime number p 
       such that it is greater than alpha.
    """
    a = sp.nextprime(alpha)

    while not (nt.residue_ntheory.is_primitive_root(a, p)):
        a = sp.nextprime(a)
    
    return a


def modexp( base, exp, modulus ):
	return pow(base, exp, modulus)


def chunky(s, chunksize):
    assert isinstance(s, str)
    assert isinstance(chunksize, int)

    chunkindex = 0 
    l = [s[i: i+chunksize] for i in range(0, len(s), chunksize)]

    return l


#generates public key K1 (p, g, h) and private key K2 (p, g, x)
def generate_keys(iNumBits=256):
    # p is the prime
    # g is the primitve root
    # x is random in (0, p-1) inclusive
    # h = g ^ x mod p

    alpha = nt.generate.randprime(10e5, 10e6)

    p = find_prime()
    g = primitive_root(p, alpha)
    g = modexp( g, 2, p )
    x = random.randint( 1, (p-1) // 2 )
    h = modexp( g, x, p )

    publicKey = PublicKey(p, g, h, iNumBits)
    privateKey = PrivateKey(p, g, x, iNumBits)

    return {'privateKey': privateKey, 'publicKey': publicKey}


def decode(aiPlaintext, iNumBits):
    bytes_array = []

    #same deal as in the encode function.
    #each encoded integer is a linear combination of k message bytes
    #k must be the number of bits in the prime divided by 8 because each
    #message byte is 8 bits long
    k = iNumBits // 8

    # num is an integer in list aiPlaintext
    for num in aiPlaintext:
        #get the k message bytes from the integer, i counts from 0 to k-1
        for i in range(k):
                #temporary integer
                temp = num
                #j goes from i+1 to k-1
                for j in range(i+1, k):
                        #get remainder from dividing integer by 2^(8*j)
                        temp = temp % (2**(8*j))
                #message byte representing a letter is equal to temp divided by 2^(8*i)
                letter = temp // (2**(8*i))
                #add the message byte letter to the byte array
                bytes_array.append(letter)
                #subtract the letter multiplied by the power of two from num so
                #so the next message byte can be found
                num = num - (letter*(2**(8*i)))

    decodedText = bytearray(b for b in bytes_array).decode('utf-16')

    return decodedText


#encrypts a string sPlaintext using the public key k
def encrypt(key, encodedMessage):

	# cipher_pairs list will hold pairs (c, d) corresponding to each integer in z
    cipher_pairs = []
    # i is an integer in z
    for i in encodedMessage:
        # pick random y from (0, p-1) inclusive
        y = random.randint( 0, key.p )
        # c = g^y mod p
        c = modexp( key.g, y, key.p )
        # d = ih^y mod p
        d = (i*modexp( key.h, y, key.p)) % key.p
        # add the pair to the cipher pairs list
        cipher_pairs.append( [c, d] )

    encryptedStr = ""
    for pair in cipher_pairs:
        encryptedStr += str(pair[0]) + ' ' + str(pair[1]) + ' '

    return encryptedStr


def decrypt(key, cipher):
    # decrpyts each pair and adds the decrypted integer to list of plaintext integers
    plaintext = []

    cipherArray = cipher.split()
    if (not len(cipherArray) % 2 == 0):
        return "Malformed Cipher Text"
    for i in range(0, len(cipherArray), 2):
        #c = first number in pair
        c = int(cipherArray[i])
        #d = second number in pair
        d = int(cipherArray[i+1])

        #s = c^x mod p
        s = modexp( c, key.x, key.p )
        #plaintext integer = ds^-1 mod p
        plain = (d*modexp( s, key.p-2, key.p)) % key.p
        #add plain to list of plaintext integers
        plaintext.append( plain )

    decryptedText = decode(plaintext, key.iNumBits)

    #remove trailing null bytes
    decryptedText = "".join([ch for ch in decryptedText if ch != '\x00'])

    return decryptedText

