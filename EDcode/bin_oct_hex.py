from Crypto.Util.number import long_to_bytes, bytes_to_long
from string import printable

printable_set = set(printable)
# printable_set = [chr(i) for i in range(256)]

def prefix_decoder(enc: str):
    if enc.startswith('0x') or enc.startswith('x'):
        return long_to_bytes(int(enc.split('x')[1], 16))
    
    if enc.startswith('0d') or enc.startswith('d'):
        return long_to_bytes(int(enc.split('d')[1]))

    if enc.startswith('0o') or enc.startswith('o'):
        return long_to_bytes(int(enc.split('o')[1], 8))
    
    return long_to_bytes(int(enc.split('b')[1], 2))

def printable_check(enc):
    for e in enc:
        if not chr(e) in printable_set:
            return False
    return True

def brute_force_decoder(enc, possible_decode):
    max_base = max(enc)
    ret = []

    add = long_to_bytes(int(enc, 16))
    if printable_check(add):
        ret += [now + add for now in possible_decode]
    if max_base >= '8':
        if not printable_check(add):
            return [now + b'[none]' for now in possible_decode]
        return ret

    add = long_to_bytes(int(enc, 8))
    if printable_check(add):
        ret += [now + add for now in possible_decode]
    if max_base >= '2':
        return ret
    
    add = long_to_bytes(int(enc, 2))
    if printable_check(add):
        ret += [now + add for now in possible_decode]
    return ret

def most_possible(enc):
    max_base = max(enc)

    if max_base <= '1':
        add = long_to_bytes(int(enc, 2))
        if printable_check(add):
            return add

    if max_base <= '7':
        add = long_to_bytes(int(enc, 8))
        if printable_check(add):
            return add

    add = long_to_bytes(int(enc, 16))
    if not printable_check(add):
        return '?'
    return add 


func = input("1. decode with prefix(0b, 0o, 0x)\n\
2. decode the most possible (input long text for futher analysis)\n\
3. decode with brute force (for short string)\n\
4. decode bin oct hex\n\
5. encode text to bin oct hex\n\
Choose: ")

encode_text = input("Input text: ").strip()


if func == '1':
    print(b" ".join([prefix_decoder(enc) for enc in encode_text.split()]))

elif func == '2':
    print(b" ".join([most_possible(enc) for enc in encode_text.split()]))

elif func == '3':
    possible_decode = [b""]
    for enc in encode_text.split():
        possible_decode = brute_force_decoder(enc, possible_decode)
    for pos in possible_decode:
        print(pos)

elif func == '4':
    try:
        text = long_to_bytes(int(encode_text ,2))
        if printable_check(text):
            print("Bin:", text)
    except:
        pass
    try:
        text = long_to_bytes(int(encode_text ,8))
        if printable_check(text):
            print("Oct:", text)
    except:
        pass
    try:
        text = long_to_bytes(int(encode_text ,16))
        if printable_check(text):
            print("Hex:", text)
    except:
        pass

elif func == '5':
    base = int(input("Input base (input 0 show all): "))
    num = bytes_to_long(encode_text.encode())
    if base == 2 or base == 0:
        print("Bin:", bin(num))
    if base == 8 or base == 0:
        print("Oct:", oct(num))
    if base == 16 or base == 0:
        print("Hex:", hex(num))


# Bin: 0b1101000011001010110110001101100011011110010000001110111011011110111001001101100011001000010000001110111011010000110000101110100001000000111010001101000011001010010000001100110011101010110001101101011
# Oct: 0o1503126615433620167336711543102016732060564100721503122014635261553
# Hex: 0x68656c6c6f20776f726c64207768617420746865206675636b

# 101 
