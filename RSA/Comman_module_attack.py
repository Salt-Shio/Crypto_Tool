from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime, GCD
from Extended_GCD import Extended_GCD

p = getPrime(1024)
q = getPrime(1024)
n = p * q
phi_n = (p - 1) * (q - 1)

e1 = 65537
e2 = getPrime(17)
while GCD(e2, phi_n) != 1: e2 = getPrime(17)

m = bytes_to_long(b"hello world hahahah su ba la si !")
c1 = pow(m, e1, n)
c2 = pow(m, e2, n)

def comman_module_attack(e1, e2, c1, c2, n):
    s1, s2 = Extended_GCD(e1, e2)
    return long_to_bytes((pow(c1, s1, n) * pow(c2, s2, n)) % n).decode()

print(comman_module_attack(e1, e2, c1, c2, n))