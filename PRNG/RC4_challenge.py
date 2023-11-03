from Crypto.Cipher import ARC4

FLAG = "flag{rc4_fms_attack}"

def send_cmd(ciphertext, nonce):
    ciphertext = bytes.fromhex(ciphertext)
    nonce = bytes.fromhex(nonce)

    cipher = ARC4.new(nonce + FLAG.encode())
    cmd = cipher.decrypt(ciphertext)

    if cmd == b"hello":
        return "world"
    else:
        return cmd.hex()

print(send_cmd("00", "123456"))