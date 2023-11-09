
import os
import sys

from Crypto.Cipher import AES
iv = os.urandom(16)
key = os.urandom(32)


def pad(text):
    padding = 16 - (len(text) % 16)
    return text + bytes([padding]) * padding

def unpad(text):
    padding = text[-1]
    assert 1 <= padding <= 16
    assert text.endswith(bytes([padding]) * padding)
    return text[:-padding]


def encrypt(text):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(text))

def decrypt(text):
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(text))
    except AssertionError:
        return b"Error"

def token():
    text = b"test123_guest"
    return encrypt(text).hex()


def verify(token):
    text = decrypt(bytes.fromhex(token))
    
    if b"test123_guest" in text:
        return b"Hi guest!"
 
    if b"user456_admin" in text:
        print(text)
        print("Hi admin!")
        print(f"Here is your flag: {FLAG}")
        return FLAG

    if b"Error" in text:
        return b"Error QQ"

    return b"Bad hacker"


FLAG = "flag{flags}"
xor = lambda a, b: bytes(i ^ j for (i, j) in zip(a, b))

test_token = bytes.fromhex(token())
rand_bit = bytearray(b"")


t = 1
for i in range(1, 15, 1):
    for guess_byte in range(256):
        print(i, guess_byte)
        send = bytes([guess_byte]) + rand_bit + test_token
        send = send.rjust(32, b"\x00")
        respone = verify(send.hex())
        t += 1
        if b"Bad" in respone:
            rand_bit = bytes([guess_byte]) + rand_bit
            break
    if i == 14:
        break
    for j in range(i):
        rand_bit = bytearray(rand_bit)
        rand_bit[j] ^= i ^ (i + 1) 

c1 = xor(xor(b"yy" + rand_bit, b"xx" + b"\x0e" * 14), pad(b"aauser456_admin"))
print(verify((c1 + test_token).hex()))
print(t + 1)
