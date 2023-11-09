from Crypto.Util.number import isPrime
from gmpy2 import iroot

def fermat_factor(n):
    if isPrime(n):
        return -1,-1
    a = iroot(n, 2)[0] + 1
    bs = a * a - n
    while not gmpy2.is_square(bs):
        a += 1
        bs = a * a - n
    b = gmpy2.isqrt(bs)
    return a + b , a - b