def bin_to_gray(bin_code):
    return bin(bin_code ^ bin_code >> 1)

def gray_to_bin(gray_code):
    now = gray_code[0]
    ret_bin = [now]
    for g in gray_code[1:]:
        now = int(g) ^ int(now)
        ret_bin.append(str(now))

    return ''.join(ret_bin)

input_num = int(input())
gray_code = bin_to_gray(input_num)[2:]
print("Bin:", bin(input_num)[2:], "Gray:", gray_code)
print("Verify:", gray_to_bin(gray_code) == bin(input_num)[2:])