from Crypto.Util.number import isPrime, GCD
from gmpy2 import iroot
import gmpy2

def fermat_factor(n):
    if isPrime(n):
        return -1,-1
    a = iroot(n, 2)[0] + 1
    b2 = a * a - n
    while not iroot(b2, 2)[1]:
        a += 1
        b2 = a * a - n
    b = iroot(b2, 2)[0]
    return int(a + b) , int(a - b)

def pollard(n):
    a, m = 2, 2
    
    while not (1 < GCD(a - 1, n) < n):
        a = pow(a, m, n)
        m += 1

    return GCD(a - 1, n)

def williams(n, B=None):
    """B is the largest prime of the factors of p+1 or p-1"""
    def gen_prime():
        yield 3
        i = 5
        while True:
            if isPrime(i):
                yield i
            if isPrime(i+2):
                yield i+2
            i += 6

    def mlucas(b, k):
        """It returns k-th V(b, 1)"""
        v1, v2 = b % n, (b ** 2 - 2) % n
        for bit in bin(k)[3:]:
            if int(bit):
                v1, v2 = (v1 * v2 - b) % n, (v2 ** 2 - 2) % n
            else:
                v1, v2 = (v1 ** 2 - 2) % n, (v1 * v2 - b) % n
        return v1

    B = B or int(gmpy2.isqrt(n))
    for A in gen_prime():
        v = A
        for i in range(1, B+1):
            v = mlucas(v, i)
            g = GCD(v - 2, n)
            if g > 1:
                return g
