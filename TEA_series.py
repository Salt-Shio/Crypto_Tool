import struct

class TEA:
    def __init__(self, key) -> None:
        self.key = struct.unpack("4I", key)
    
    def pkcs5(self, plain: bytes):
        pad = 8 - len(plain) % 8
        return plain + pad * bytes([pad])
    
    def unpkcs5(self, plain: bytes):
        pad = plain[-1]
        return plain[:-pad]

    def encrypt(self, plain: bytes):
        plain = self.pkcs5(plain)
        cipher = b""
        mask = 0xffffffff
        delta = 0x9e3779b9

        for i in range(0, len(plain), 8):
            left, right = struct.unpack("2I", plain[i: i+8])
            _sum = 0
            for j in range(32):
                _sum = (_sum + delta) & mask

                left += (((right << 4) + self.key[0]) \
                        ^ (right + _sum) \
                        ^ ((right >> 5) + self.key[1]))
                left &= mask

                right += (((left << 4) + self.key[2]) \
                        ^ (left + _sum) \
                        ^ ((left >> 5) + self.key[3]))
                right &= mask

            cipher += struct.pack("2I", left, right)
        
        return cipher
    
    def decrypt(self, cipher: bytes):
        plain = b""
        mask = 0xffffffff
        delta = 0x9e3779b9

        for i in range(0, len(cipher), 8):
            left, right = struct.unpack("2I", cipher[i: i+8])
            _sum = (delta * 32) & mask
            for j in range(32):
                
                right -= ((left << 4) + self.key[2]) \
                        ^ (left + _sum) \
                        ^ ((left >> 5) + self.key[3])
                right &= mask

                left -= (((right << 4) + self.key[0]) \
                        ^ (right + _sum) \
                        ^ ((right >> 5) + self.key[1])) & mask
                left &= mask
                _sum = (_sum - delta) & mask

            plain += struct.pack("2I", left, right)
        
        return self.unpkcs5(plain)

class XTEA:
    def __init__(self, key, rounds) -> None:
        self.key = struct.unpack("4I", key)
        self.rounds = rounds
    
    def pkcs5(self, plain: bytes):
        pad = 8 - len(plain) % 8
        return plain + pad * bytes([pad])
    
    def unpkcs5(self, plain: bytes):
        pad = plain[-1]
        return plain[:-pad]

    def encrypt(self, plain: bytes):
        plain = self.pkcs5(plain)
        cipher = b""
        mask = 0xffffffff
        delta = 0x9e3779b9

        for i in range(0, len(plain), 8):
            left, right = struct.unpack("2I", plain[i: i+8])
            _sum = 0
            for j in range(self.rounds):
                left += (((right << 4) ^ (right >> 5)) + right) \
                        ^ (_sum + self.key[_sum & 3])
                left &= mask

                _sum = (_sum + delta) & mask
                
                right += (((left << 4) ^ (left >> 5)) + left) \
                        ^ (_sum + self.key[(_sum >> 11) & 3])
                right &= mask

            cipher += struct.pack("2I", left, right)
        
        return cipher
    
    def decrypt(self, cipher: bytes):
        plain = b""
        mask = 0xffffffff
        delta = 0x9e3779b9

        for i in range(0, len(cipher), 8):
            left, right = struct.unpack("2I", cipher[i: i+8])
            _sum = (delta * self.rounds) & mask
            for j in range(self.rounds):
                right -= (((left << 4) ^ (left >> 5)) + left) \
                        ^ (_sum + self.key[(_sum >> 11) & 3])
                right &= mask

                _sum = (_sum - delta) & mask

                left -= (((right << 4) ^ (right >> 5)) + right) \
                        ^ (_sum + self.key[_sum & 3])
                left &= mask

            plain += struct.pack("2I", left, right)
        
        return self.unpkcs5(plain)

class XXTEA:
    def __init__(self, key) -> None:
        self.key = struct.unpack("4I", key)
    
    def pkcs5(self, plain: bytes):
        pad = 8 - len(plain) % 8
        return plain + pad * bytes([pad])
    
    def unpkcs5(self, plain: bytes):
        pad = plain[-1]
        return plain[:-pad]

    def data_pack(self, data: list):
        return struct.pack(str(len(data)) + "I", *data)

    def data_unpack(self, data: bytes):
        return [struct.unpack("I", data[i: i + 4])[0] for i in range(0, len(data), 4)]

    def encrypt(self, plain):
        data = self.data_unpack(self.pkcs5(plain))
        data_length = len(data)
        rounds = 6 + 52 // data_length
        mask = 0xffffffff
        delta = 0x9e3779b9
        _sum = 0

        for round in range(rounds):
            _sum = (_sum + delta) & mask
            e = _sum >> 2 & 3
            for i in range(data_length):
                left = data[i - 1]
                right = data[(i + 1) % data_length]
                data[i] += ((left >> 5 ^ right << 2) \
                            + (right >> 3 ^ left << 4) \
                            ^ (_sum ^ right) \
                            + (self.key[i & 3 ^ e] ^ left))
                data[i] &= mask
        
        return self.data_pack(data)

    def decrypt(self, cipher):
        data = self.data_unpack(cipher)
        data_length = len(data)
        rounds = 6 + 52 // data_length
        mask = 0xffffffff
        delta = 0x9e3779b9
        _sum = (delta * rounds) & mask

        for round in range(rounds):
            e = _sum >> 2 & 3
            for i in range(data_length - 1, -1, -1):
                left = data[i - 1]
                right = data[(i + 1) % data_length]
                data[i] -= ((left >> 5 ^ right << 2) \
                            + (right >> 3 ^ left << 4) \
                            ^ (_sum ^ right) \
                            + (self.key[i & 3 ^ e] ^ left))
                data[i] &= mask
            _sum = (_sum - delta) & mask
        
        return self.unpkcs5(self.data_pack(data))


import os 
key = b"1234567890abcdef"

tea = TEA(key)
tea_cipher = tea.encrypt(b"Hello TEA!")
de_tea_cipher = tea.decrypt(tea_cipher)
print(de_tea_cipher)

xtea = XTEA(key, 40)
xtea_cipher = xtea.encrypt(b"Hello XTEA!")
de_xtea_cipher = xtea.decrypt(xtea_cipher)
print(de_xtea_cipher)

xxtea = XXTEA(key)
xxtea_cipher = xxtea.encrypt(b"Hello XXTEA!")
de_xxtea_cipher = xxtea.decrypt(xxtea_cipher)
print(de_xxtea_cipher)