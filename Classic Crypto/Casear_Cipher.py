class Casear:
    def __init__(self, cipher: str):
        self.cipher = cipher
    
    def Brute_force_letter(self):
        ret = []

        for offset in range(1, 26):
            plain = ""
            lower_base = ord('a')
            upper_base = ord('A')
            for char in self.cipher:
                if 'a' <= char <= 'z':
                    index = ord(char) - lower_base
                    plain += chr(lower_base + (index + offset) % 26)
                elif 'A' <= char <= 'Z':
                    index = ord(char) - upper_base
                    plain += chr(upper_base + (index + offset) % 26)
                else:
                    plain += char

            ret.append(plain)
        
        return ret

cipher = input()
casear = Casear(cipher)

for i, plain in enumerate(casear.Brute_force_letter()):
    print("<-------- " + f"key{i + 1}" + " -------->\n")
    print(plain)
    print()
