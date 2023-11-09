from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from gmpy2 import iroot

p = getPrime(512)
q = getPrime(512)
n = (p - 1) * (q - 1) 
e = 3

m = bytes_to_long(b"Hello world hahaha su ba la si Hello world a")

c = pow(m, e, n)
print((m ** e - c) // n)

k = 0
while True:
    m3 = n * k + c
    if iroot(m3, 3)[1]:
        plain = long_to_bytes(iroot(m3, 3)[0]).decode(errors = "ignore")
        if "Hello" in plain:
            print(plain)
            break
    k += 1




