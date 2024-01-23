MASK = (2 ** 32 - 1)

def inverse_left(extract_randnum, shift, and_num = -1):
    mask = MASK >> (32 - shift)
    inverse_num = 0
    for _ in range(0, 32, shift):
        tmp = (inverse_num << shift) & and_num
        new_extract = (extract_randnum ^ tmp) & mask
        inverse_num = new_extract | inverse_num
        mask <<= shift
    return inverse_num

def inverse_right(extract_randnum, shift, and_num = -1):
    mask = MASK << (32 - shift)
    inverse_num = 0
    for _ in range(0, 32, shift):
        tmp = (inverse_num >> shift) & and_num
        new_extract = (extract_randnum ^ tmp) & mask
        inverse_num = new_extract | inverse_num
        mask >>= shift
    return inverse_num


def inverse_randnum(extract_randnum): 
    inv_randnum = extract_randnum
    inv_randnum = inverse_right(inv_randnum, 18)
    inv_randnum = inverse_left(inv_randnum, 15, 0xefc60000)
    inv_randnum = inverse_left(inv_randnum, 7, 0x9d2c5680)
    inv_randnum = inverse_right(inv_randnum, 11)
    return inv_randnum

def reverse_twist(twist):
    
    reverse_twist=[0] * 624
    
    for i in range(623,-1,-1):
        tmp = twist[i] ^ twist[(i + 397) % 624] 
        if (tmp & 0x80000000) >> 31 == 1:
            tmp = tmp ^ 0x9908b0df
            low_bit = 1
            high_bit = (tmp & 0x40000000) >> 30
            reverse_twist[i] = high_bit << 31
            reverse_twist[(i + 1) % 624] = reverse_twist[(i + 1) % 624] + ((tmp & 0x3fffffff) << 1) + low_bit
            if i != 623:
                twist[(i + 1) % 624] = reverse_twist[(i + 1) % 624]

        elif (tmp & 0x80000000) >> 31 == 0:
            low_bit = 0
            high_bit = (tmp & 0x40000000) >> 30
            reverse_twist[i] = high_bit << 31
            reverse_twist[(i + 1) % 624] = reverse_twist[(i + 1) % 624]+((tmp & 0x3fffffff) << 1) + low_bit
            if i != 623:
                twist[(i + 1) % 624] = reverse_twist[(i + 1) % 624]
    return reverse_twist