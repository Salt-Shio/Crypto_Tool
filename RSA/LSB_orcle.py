from Crypto.Util.number import bytes_to_long, getPrime, inverse, long_to_bytes

p, q = getPrime(512), getPrime(512)
n, e = p * q, 0x10001
d = inverse(e, (p - 1) * (q - 1))

FLAG = "flag{I'm am a cool flag haha}"

m = bytes_to_long(FLAG.encode())
c = pow(m, e, n)

def decrypt(c, d, n):
    m = pow(c, d, n)
    return m % 3

def LSB_orcle(c, e, n, r):
    """r: server return (m % r)"""
    plain = 0
    exp = 0
    a_inv = 0
    inv = pow(r, -1, n)

    break_count = 0

    while True:
        send_cipher = pow(inv, exp * e, n) * c
        recv_lsb = decrypt(send_cipher, d, n)
        a = (recv_lsb - a_inv % n) % r
        
        if a == 0: # 如果一直是 0 就代表找完了
            break_count += 1
            if break_count == 20:
                break
        else:
            break_count = 0

        plain += (a * (r ** exp))
        a_inv =  (a_inv + a) * inv
        exp += 1

    return long_to_bytes(plain)

print(LSB_orcle(c, e, n, 3).decode())

