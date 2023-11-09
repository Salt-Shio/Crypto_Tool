import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# exit()
#aaaaa\x0b\x0b\x0b...*11  16#
iv = os.urandom(16)
key = os.urandom(32)

xor = lambda a, b : bytes(i ^ j for i, j in zip(a, b))

def CBC_MAC(text):
    aes = AES.new(key, AES.MODE_CBC, iv)
    pre_mac = aes.encrypt(pad(text, 16))[-16:]
    aes = AES.new(key, AES.MODE_ECB)
    mac = aes.encrypt(pre_mac).hex().rjust(32)
    return mac


def token():
    mac = CBC_MAC(b"user1234@gmail.com")
    return mac

def challenge(email: bytes):
    if CBC_MAC(email) == token():
        if email.split(b'@')[0] == b"admin123" and email.split(b'@')[1][:9] == b"gmail.com":
            print("Hello admin")
        else:
            print("Who are you?")
    else:
        print("Unknow user")

def encrypt(plain):
    cipher = AES.new(key, AES.MODE_CBC, iv = iv)
    return cipher.encrypt(pad(plain, 16)).hex()

def decrypt(cipher):
    aes = AES.new(key, AES.MODE_CBC, iv = iv)
    return aes.decrypt(bytes.fromhex(cipher)).hex()

admin_mail = b"admin123@gmail.com"
user_mail = b"user1234@gmail.com"

challenge(admin_mail)

c = b'\x00' * 16 + b'a' * 16
# sever decrypt
# send c.hex() => me 

D_c_2 = decrypt(c.hex())[32:]
c = b'a' * 16 + b'c' * 16
find_iv = xor(bytes.fromhex(decrypt(c.hex())[:32]), bytes.fromhex(D_c_2))

admin_cipher = encrypt(pad(admin_mail, 16))[32:]
payload = pad(admin_mail, 16) + xor(xor(find_iv, user_mail[:16]), bytes.fromhex(admin_cipher)) + user_mail[-2:]
challenge(payload)
