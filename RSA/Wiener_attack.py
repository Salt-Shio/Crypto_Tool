from Crypto.Util.number import long_to_bytes

def continue_fraction(a, b):
    ret = []
    while b != 0:
        ret.append(a // b)
        a, b = b, a % b
    return ret

def continue_fraction_reverse(continue_fraction):
    p0, p1 = 1, continue_fraction[0]
    q0, q1 = 0, 1

    ret = [(p1, q1)]
    for CF in continue_fraction[1:]:
        p0, p1 = p1, p1 * CF + p0
        q0, q1 = q1, q1 * CF + q0
        ret.append((p1, q1))

    return ret # 算出來的會約分

def wiener_attack(e, N, c):
    cf = continue_fraction(e, N)
    possible_k_d = continue_fraction_reverse(cf)
    for k_d in possible_k_d:
        k,d = k_d
        plain = long_to_bytes(pow(c, d, N)).decode(errors="ignore")
        if "pico" in plain:
            return plain