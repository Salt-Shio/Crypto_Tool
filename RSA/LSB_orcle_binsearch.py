from Crypto.Util.number import bytes_to_long, getPrime, inverse, long_to_bytes
import decimal

p, q = getPrime(512), getPrime(512)
n, e = p * q, 0x10001
d = inverse(e, (p - 1) * (q - 1))

FLAG = "flag{I'm am a cool flag haha}"

m = bytes_to_long(FLAG.encode())
c = pow(m, e, n)

def decrypt(c, d, n):
    m = pow(c, d, n)
    return m & 1

def LSB_orcle(c: int, e: int, n: int):
    
    low, high = decimal.Decimal(0), decimal.Decimal(n)
    decimal.getcontext().prec = n.bit_length()
    exp = 0

    for _ in range(n.bit_length()):
        exp += 1
        send_cipher = pow(2, exp * e, n) * c
        mid = (low + high) / 2

        if decrypt(send_cipher, d, n) == 0:
            if mid <= low: break
            high = mid
        else:
            if mid >= high: break
            low = mid

    print("High:", long_to_bytes(int(high)).decode(errors = "ignore"))
    print("mid:", long_to_bytes(int(mid)).decode(errors = "ignore"))
    print("low:", long_to_bytes(int(low)).decode(errors = "ignore"))


