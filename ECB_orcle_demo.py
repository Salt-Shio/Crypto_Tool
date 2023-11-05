from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

key = b"0123456789abcdef"
secret = b"I'm am a cool secret you should know"

def server(send_msg):
    aes = AES.new(key, AES.MODE_ECB)
    plain = b"Hello " + send_msg + secret
    cipher = aes.encrypt(pad(plain, 16))
    return cipher.hex()

def find_add_length():
    no_pad_length = len(server(b""))
    for add_len in range(1, 17):
        recv = server(b"a" * add_len)
        if no_pad_length != len(recv):
            break
    return add_len, len(recv)

add_len, recv_length = find_add_length()
brute_force_point = 32 
secret_pointer = recv_length - 32
Xpad = b"xxxxxxxxxx"
secret_string = b""

for i in range(1, 50, 1):
    encrypt_secret = server(b'a' * (add_len + i))[secret_pointer: secret_pointer + 32]
    for guess_byte in range(256):
        payload = bytes([guess_byte]) + secret_string[:15]
        if len(payload) < 16: payload = pad(payload, 16)
        guess_rec = server(Xpad + payload)
        if guess_rec[brute_force_point:brute_force_point + 32] == encrypt_secret:
            secret_string = bytes([guess_byte]) + secret_string
            break
    print(secret_string)

# print(secret_string)