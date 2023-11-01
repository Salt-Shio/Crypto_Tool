from Crypto.Util.number import inverse
from math import gcd
from pwn import *

def  get_m_nums(nonce):
    m_nums = []
    for i in range(13):
        num=(nonce[i] - nonce[i + 1]) * (nonce[ i + 2 ] - nonce[i + 3]) - (nonce[i + 1] - nonce[i + 2]) ** 2
        m_nums.append(num)
    return m_nums

def gcd_m_nums(mnums):
    m = mnums[0]
    for i in range(12):
        m = gcd(m , mnums[i + 1])
    return m


nonce = [16930430003958815389, 272515578559467103213354728151242537600, 92710202930416477524499261818391708685,210121141778882681558038871817915153336,7574541747552967624437842014314406753,165293508755305657502710531698327716146,4854539309219147013272481239141153014,297286816726706999268095758521493353955,93056668758726819989681317447963502823,28481674078270450591258376911920908273,196696122009223964372735851083284428210,147163801482512299534132116812313991150,199055561282632959896292521353311118693,60126433609107186493720869158907776167,149926822230400595744838196047016324698,72927048368673761644731526896514396856]

r = remote("lab.scist.org", 10021)
r.recv()
r.sendline(b"challenge")
nonce = list(map(int, r.recvline()[:-1].replace(b"Problem: ", b'').decode().split(',')))
# print(nonce)
m = gcd_m_nums(get_m_nums(nonce)) #ans m
a = ((nonce[1] - nonce[2]) * inverse(nonce[0] - nonce[1], m)) % m
c = nonce[1] - a * nonce[0] % m
r.recv()
r.sendline(str((a * nonce[15] + c) % m).encode())
print(r.recv())
# print((a * nonce[15] + c) % m)