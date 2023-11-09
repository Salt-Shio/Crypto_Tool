from Crypto.Cipher import DES, DES3
from Crypto.Util.Padding import pad
from Crypto.Util.number import bytes_to_long, long_to_bytes
import os

xor = lambda x, y: bytes(i ^ j for i, j in zip(x, y))

def bit_bar(data):
    bit_len = len(data) * 8
    return long_to_bytes((bytes_to_long(data) ^ (2 ** bit_len - 1))).rjust(len(data), b'\x00')

def bar_test():
    key = os.urandom(8)
    des = DES.new(key, mode = DES.MODE_ECB)
    plain = pad(b"hello world", 16)
    cipher = des.encrypt(plain)

    key_ = bit_bar(key)
    des_ = DES.new(key_, mode = DES.MODE_ECB)
    plain_ = bit_bar(plain)
    cipher_ = des_.encrypt(plain_)

    print(plain)
    print(plain_)
    print(key)
    print(key_)
    print(cipher)
    print(bit_bar(cipher_))

def weak_key():
    k1 = bytes.fromhex("0101010101010101")
    k2 = bytes.fromhex("FEFEFEFEFEFEFEFE")
    k3 = bytes.fromhex("E0E0E0E0F1F1F1F1")
    secret = pad(b"saltsaltsalt", 16)
    plain = pad(b"hello world", 16)
    
    key = k1 + k2 + k3
    des3 = DES3.new(key, DES.MODE_ECB)
    cipher = xor(des3.encrypt(xor(plain, secret)), secret)

    key2 = k3 + k2 + k1
    des3_2 = DES3.new(key2, DES.MODE_ECB)
    print(xor(des3_2.encrypt(xor(cipher, secret)), secret))

def brute_force():
    # key = "00000000" -> "99999999"
    hello = bytes.fromhex("faa6244d40f3bae7bf771cd62c354a6cfc9fed414dbc1b6f")
    flag = bytes.fromhex("db132bb4b19158d5984de8de199f38a05a2e244a0414988b6e2b5e86e54ea6d3")
    from itertools import product

    for key in list(product([str(i) for i in range(0, 10, 2)], repeat= 8)):
        key_bytes = "".join(key).encode()
        des = DES.new(key_bytes, DES.MODE_ECB)
        if b"Hello" in des.decrypt(hello):
            print(key_bytes)
            print("flag:", des.decrypt(flag))
            break
