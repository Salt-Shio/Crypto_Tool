from Crypto.Util.number import bytes_to_long, long_to_bytes
from pwn import *

r = remote("lab.scist.org", 10057)
public = r.recvline().decode().replace("public key: (","").replace(")\n","").split(", ")
e, n = int(public[0]), int(public[1])

cipher = r.recvline().decode()
cipher = bytes_to_long(bytes.fromhex(cipher.replace("encrypted: ","")[:-1]))
r.recv()

B = bytes_to_long(b"\x01" + 30 * b"\x00")

def ceil_int(a, b):
    return - (a // -b)

def floor_int(a, b):
    return a // b

def vaild(c): # 主要修改部分
    r.sendline(b"decrypt")
    r.recv()
    r.sendline(c.encode())
    ans = r.recv().decode()
    return not "Bad" in ans

def Find_Next_S_opt(s, interval_old: set):
    first = interval_old.pop()
    interval_old.add(first)
    a = first[0]
    b = first[1]
    r = ceil_int((2 * (b * s - 2 * B)) , n)
    while True:
        bottom = ceil_int((2 * B + r * n) , b)
        top = ceil_int((3 * B + r * n) , a)
        # print(bottom, top)
        for s in range(bottom, top):
            new_cipher = (pow(s, e, n) * cipher) % n
            new_cipher = long_to_bytes(new_cipher).hex()
            if vaild(new_cipher):
                return int(s)
        r += 1

def Find_Next_S(s):
    while True:
        s += 1
        new_cipher = (pow(s, e, n) * cipher) % n
        new_cipher = long_to_bytes(new_cipher).hex()
        if vaild(new_cipher):
            print("Find s")
            return s 

def Find_Next_Interval(interval_old, s):
    interval_new = set([])
    for (a, b) in interval_old:
        bottom = ceil_int((-3 * B + s * a) , n)
        top = floor_int((-2 * B + s * b) , n)
        # print(bottom, top)
        for k in range(bottom, top + 1):
            new_a = max(a, ceil_int((2 * B + k * n) , s))
            new_b = min(b, floor_int((3 * B - 1 + k * n) , s))
            # print(new_a, new_b)
            if new_a <= new_b:
                interval_new |= set([(new_a, new_b)])
    return interval_new

request = 1

def attack():
    global request
    interval = set([(2 * B, 3 * B - 1)])
    s = ceil_int(n , (3 * B))
    while True:
        if len(interval) > 1 or request == 1:
            s = Find_Next_S(s)
        else:
            ans = interval.pop()
            interval.add(ans)

            if ans[0] == ans[1]:
                print("Find answer!!!")
                return ans
            
            s = Find_Next_S_opt(s, interval)
        interval = Find_Next_Interval(interval, s)
        request += 1

flag = attack()
print(flag)
print(long_to_bytes(flag))

