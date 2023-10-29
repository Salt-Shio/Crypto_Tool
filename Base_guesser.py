from base64 import *
from base58 import b58encode, b58decode

use_encode = False if input("Encoding: [Y/n]") == 'n' else True
use_decode = False if input("Decoding: [Y/n]") == 'n' else True

input_text = input().encode()
if use_decode:
    print("<------------ Decoding ------------>\n")

    decoder = [b16decode, b32decode, b64decode, b58decode, b85decode]
    Base_name = ["Base16", "Base32", "Base64", "Base58", "Base85"]

    for i in range(len(decoder)):
        try:
            decode_text = decoder[i](input_text)
            print(f"<======{Base_name[i]}======>")
            print(decode_text)
            print()
        except:
            pass

if use_encode:
    print("<------------ encoding ------------>\n")
    encoder = [b16encode, b32encode, b64encode, b58encode, b85encode]

    for i in range(len(encoder)):
        try:
            encode_text = encoder[i](input_text)
            print(f"<======{Base_name[i]}======>")
            print(encode_text)
            print()
        except:
            pass