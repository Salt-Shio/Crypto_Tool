
from sage.all import * # 在 linux 下載 sage python，interpreter 用 sage python
from Crypto.Cipher import AES

x = GF(2)["x"].gen() 
F = GF(2**128, names='y', modulus = x ** 128 + x ** 7 + x ** 2 + x + 1)


def GCM(plain, key, nonce, auth):
    aes = AES.new(key, AES.MODE_GCM, nonce = nonce).update(auth)
    cipher = aes.encrypt(plain)
    tag = aes.digest()
    return cipher, tag, auth

def zero_padding(cipher):
    if len(cipher) % 16 != 0:
        cipher += bytes(16 - len(cipher) % 16)
    return cipher

def num_to_gf(byte):
    blist = list(bin(byte)[2:].zfill(128))
    return F(blist)


def ghash(cipher, auth, h): # return ax + cx + lx
    # print("h:", h)
    len_cipher = len(cipher)
    len_auth = len(auth)
    cipher = zero_padding(cipher)
    auth = zero_padding(auth)
    f = F()
    blocks = [auth[i : i+16] for i in range(0, len(auth), 16)] + [cipher[i : i+16] for i in range(0, len(cipher), 16)]
    for block in blocks:
        f = (f + num_to_gf(int.from_bytes(block, 'big'))) * h

    length = ((8 * len_auth) << 64) | (8 * len_cipher) # len give the bytes , it needs bits so * 8
    f = (f + num_to_gf(length)) * h
    return f

def poly_to_num(poly):
    num = poly.integer_representation()
    bin_num = bin(num)[2:].zfill(128)[::-1]
    return int(bin_num, 2)



def Get_possible_H(cipher1, auth1, tag1, cipher2, auth2, tag2):
    h = F["h"].gen()
    f1 = ghash(cipher1, auth1, h) + num_to_gf(int.from_bytes(tag1, 'big'))
    f2 = ghash(cipher2, auth2, h) + num_to_gf(int.from_bytes(tag2, 'big'))
    f = f1 + f2
    return f.roots()

def Get_Tag(auth, cipher, know_auth, know_cipher, know_tag, mh):
    ek = poly_to_num(ghash(know_cipher, know_auth, mh)) ^ int.from_bytes(know_tag, 'big')
    ghash2 = poly_to_num(ghash(cipher, auth, mh))
    guess = ek ^ ghash2
    return guess.to_bytes(16, 'big')
