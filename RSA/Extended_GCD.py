def Extended_GCD(a, b):
    if b == 0:
        return 1, 0 
    r1, r2 = a, b
    s1, s2 = 1, 0
    t1, t2 = 0, 1
    while not r2 == 0: # if r2 == 0 , r1 = gcd(a, b)
        q = r1 // r2
        r1, r2 = r2, r1 - q * r2
        s1, s2 = s2, s1 - q * s2
        t1, t2 = t2, t1 - q * t2
    # a * s1 + b * t1 = gcd(a, b)
    return s1, t1
