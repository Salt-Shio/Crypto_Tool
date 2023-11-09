from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

iv = os.urandom(16)
key = os.urandom(32)

secret = b"hello world123456" #11 + 6 = 17

def server(inp1, inp2):
    plain = pad(inp1 + secret, 16) + pad(inp2, 16)
    aes = AES.new(key, AES.MODE_CBC, iv = iv) 
    cipher = aes.encrypt(plain).hex()
    return cipher

xor = lambda a, b: bytes(i^j for (i, j) in zip(a, b))

for add_len in range(16):
    cipher = server(b"a" * add_len, b"")
    if len(cipher) != 96:
        break

flag = b''

for i in range(1, 18, 1):
    input1 = b'a' * (add_len + i)
    cipher = server(input1, pad(b"", 16)) # len(pad(pad(b"", 16)).hex()) = 64 
    flag_front = bytes.fromhex(cipher[-96: -64]) # 需要 input2 前面那一塊的 cipher
    secret_front = bytes.fromhex(cipher[32: 64]) # 需要要找的明文的前一塊 cipher

    for guess_byte in range(256):
        sendmsg = bytes([guess_byte]) + flag[:16]
        
        if len(flag) < 15:
            sendmsg = pad(sendmsg, 16)

        sendmsg = xor(xor(sendmsg, secret_front), flag_front)
        cipher = server(input1, sendmsg)

        secret_cipher = cipher[64: 96] # secret_cipher 的位置
        guess_cipher = cipher[-64: -32] # 猜測的位置

        if guess_cipher == secret_cipher:
            flag = bytes([guess_byte]) + flag
            break

print(flag)