from RC4_challenge import send_cmd
from collections import Counter

def get_S(key, state):
    s_box = [i for i in range(256)]
    j = 0
    for i in range(state): # key len = 0, 1, 2
        j = (j + s_box[i] + key[i]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]
    return s_box, j

keys = []

for A in range(24 - 3):
    counter = Counter()
    for iv2 in range(256):
        iv = [A + 3, 255, iv2]
        key_tmp = iv + keys
        s_box, j = get_S(key_tmp, A + 3)
        if not (s_box[0] == A + 3 and s_box[1] == 0):
            continue
        
        cipher = "00"
        print(iv)
        print(''.join([":02x".format(i) for i in iv]))
        KS = send_cmd(cipher, ''.join(["{:02x}".format(i) for i in iv]))
        K = (s_box.index(int(KS, 16)) - j - s_box[A + 3]) % 256
        counter[K] += 1
    keys.append(counter.most_common()[0][0])

for key in keys:
    print(chr(key), end="")