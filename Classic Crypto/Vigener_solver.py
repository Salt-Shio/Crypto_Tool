from collections import Counter
from string import ascii_uppercase as Upper
from math import ceil, floor

def I_cacu(cipher: str):
    counter = Counter()
    for char in Upper:
        counter[char] = cipher.count(char)
    return sum([counter[char] * (counter[char] - 1) for char in Upper])         \
            / (len(cipher) * (len(cipher) - 1))

def key_length_cacu(I, cipher_length):
    return (0.0265 * cipher_length) /        \
           ((0.065 - I) + cipher_length * (I - 0.0385))

def cipher_grouper(cipher, key_length):
    sub_cipher = dict()
    for key_len in key_length:
        sub_cipher[key_len] = []
        for i in range(key_len):
            sub_cipher[key_len].append("".join([cipher[i + j * key_len] for j in range(0, len(cipher)//key_len, 1)]))
    return sub_cipher

def find_key(sub_ciphers: list):
    key = ""
    for sub_cipher in sub_ciphers:
        ctr = Counter()
        for char in Upper:
            ctr[char] = sub_cipher.count(char)
        P = [ctr[char]/len(sub_cipher) for char in Upper]
        Mg = []
        for offset in range(26):
            mg = 0
            for i in range(26):
                mg += P[(i + offset) % 26] * letter_frequence[i]
            Mg.append(abs(0.065 - mg))
        key += Upper[Mg.index(min(Mg))]
    return key

letter_frequence = [0.08166999999999999, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06326999999999999, 0.09055999999999999, 0.02758, 0.00978, 0.0236, 0.0015, 0.01974, 0.00074]
table = """A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
B C D E F G H I J K L M N O P Q R S T U V W X Y Z A
C D E F G H I J K L M N O P Q R S T U V W X Y Z A B
D E F G H I J K L M N O P Q R S T U V W X Y Z A B C
E F G H I J K L M N O P Q R S T U V W X Y Z A B C D
F G H I J K L M N O P Q R S T U V W X Y Z A B C D E
G H I J K L M N O P Q R S T U V W X Y Z A B C D E F
H I J K L M N O P Q R S T U V W X Y Z A B C D E F G
I J K L M N O P Q R S T U V W X Y Z A B C D E F G H
J K L M N O P Q R S T U V W X Y Z A B C D E F G H I
K L M N O P Q R S T U V W X Y Z A B C D E F G H I J
L M N O P Q R S T U V W X Y Z A B C D E F G H I J K
M N O P Q R S T U V W X Y Z A B C D E F G H I J K L
N O P Q R S T U V W X Y Z A B C D E F G H I J K L M
O P Q R S T U V W X Y Z A B C D E F G H I J K L M N
P Q R S T U V W X Y Z A B C D E F G H I J K L M N O
Q R S T U V W X Y Z A B C D E F G H I J K L M N O P
R S T U V W X Y Z A B C D E F G H I J K L M N O P Q
S T U V W X Y Z A B C D E F G H I J K L M N O P Q R
T U V W X Y Z A B C D E F G H I J K L M N O P Q R S
U V W X Y Z A B C D E F G H I J K L M N O P Q R S T
V W X Y Z A B C D E F G H I J K L M N O P Q R S T U
W X Y Z A B C D E F G H I J K L M N O P Q R S T U V
X Y Z A B C D E F G H I J K L M N O P Q R S T U V W
Y Z A B C D E F G H I J K L M N O P Q R S T U V W X
Z A B C D E F G H I J K L M N O P Q R S T U V W X Y"""


cipher = input("Input Cipher:")
table = [line.split(' ') for line in table.split('\n')]

I = I_cacu(cipher) # 密文中隨意選擇2個字母，相同的機率
K = key_length_cacu(I, len(cipher))
key_length = list(set([floor(K), round(K), ceil(K)]))
cipher_groups = cipher_grouper(cipher, key_length)

keys = []

for key_len in key_length:
    keys.append(find_key(cipher_groups[key_len]))

# print(keys)
for key in keys:
    print("===================================================")
    print("Key:", key)
    key = ceil(len(cipher)/len(key)) * key
    plain = ""
    base = ord('A')
    for i in range(len(cipher)):
        k = ord(key[i]) - base
        idx = table[k].index(cipher[i])
        plain += Upper[idx]

    print("Plain:", plain)

