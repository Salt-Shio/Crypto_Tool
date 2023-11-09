import os
import sys

from Crypto.Cipher import AES

# from secret import FLAG
FLAG = "flag{flag_flags_flag}"

xor = lambda a, b: bytes(i ^ j for (i, j) in zip(a, b))
iv = os.urandom(16)
key = os.urandom(32)


def pad(text):
    padding = 16 - (len(text) % 16)
    return text + bytes([padding]) * padding


def unpad(text):
    padding = text[-1]
    assert 0 < padding <= 16
    assert text.endswith(bytes([padding]) * padding)
    return text[:-padding]


def encrypt(username, is_admin=b"0"):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    enc = cipher.encrypt(pad(username) + pad(is_admin))
    return enc

def decrypt(text):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    text = cipher.decrypt(text)
    return text[:-16], unpad(text[-16:])


def login(username: str):
    return encrypt(username.encode()).hex()


def verify(token: str):
    token = bytes.fromhex(token)
    username, is_admin = decrypt(token)
    if is_admin == b"1":
        print("FLAG:", FLAG)

token = login("salt")
token = bytes.fromhex(token)
c1, c2 = token[:16], token[16:]
p2 = b"0" + b"\x0f" * 15
hack = b"1" + b"\x0f" * 15
hack_c1 = xor(xor(c1, p2), hack)
verify((hack_c1 + c2).hex())

# C1 = E(iv ^ pad(user)) user+pad
# C2 = E(C1 ^ pad(admin)) 0 + pad

# P1 = D(C1) ^ iv
# P2 = D(C2) ^ C1
# C1 = C1 ^ P2 ^ hack
