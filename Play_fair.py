from string import ascii_uppercase

class Play_Fair:

    def __init__(self, secret_key: str) -> None:
        self.secret_key = secret_key
        self.init_array() 

    def init_secret_key(self, secret_key: str):
        ret_set = set()
        ret = ""
        for key in secret_key:
            if key not in ret_set:
                ret += key
                ret_set.add(key)
        return list(ret)

    def init_array(self):
        # replace 'J' to 'I'
        tmp_secret_key = self.secret_key.upper().replace('J', 'I')
        tmp_ascii_letter = ascii_uppercase.replace('J', 'I')

        # tmp_ascii_letter - tmp_secret_key 
        Uppercase_Letter = sorted(list(set(tmp_ascii_letter).difference(set(tmp_secret_key)))) 

        # final
        Letter_Array = self.init_secret_key(tmp_secret_key) + Uppercase_Letter
        self.Letter_Array = [Letter_Array[i : i+5] for i in range(0, 25, 5)]
        
        self.Letter_Array_Pos = dict()

        for i in range(5):
            for j in range(5):
                self.Letter_Array_Pos[self.Letter_Array[i][j]] = (i, j)

    def init_plain(self, plain_text: str):
        plain_text = plain_text.upper().replace('J', 'I')
        bogus1 = 'X'
        bogus2 = 'Q'

        final_plain = plain_text[0]

        for next_char in plain_text[1:]:
            
            if final_plain[-1] == next_char:
                final_plain += bogus2 if next_char == bogus1 else bogus1
                
            final_plain += next_char
        
        if len(final_plain) & 1:
            final_plain += bogus2 if next_char == bogus1 else bogus1
        
        final_plain = tuple(final_plain)
        return [(final_plain[i : i+2]) for i in range(0, len(final_plain), 2)]

    def Encrypt(self, plain_text: str):
        plain_twins = self.init_plain(plain_text)
        cipher = ""       
        for plain_twin in plain_twins:
            # (y, x)
            first_x = self.Letter_Array_Pos[plain_twin[0]][1]
            first_y = self.Letter_Array_Pos[plain_twin[0]][0]
            second_x = self.Letter_Array_Pos[plain_twin[1]][1]
            second_y = self.Letter_Array_Pos[plain_twin[1]][0]

            if first_x == second_x:
                first_cipher = self.Letter_Array[(first_y + 1) % 5][first_x]
                second_cipher = self.Letter_Array[(second_y + 1) % 5][second_x]
                cipher += first_cipher + second_cipher
            elif first_y == second_y:
                first_cipher = self.Letter_Array[first_y][(first_x + 1) % 5]
                second_cipher = self.Letter_Array[second_y][(second_x + 1) % 5]
                cipher += first_cipher + second_cipher
            else:
                first_cipher = self.Letter_Array[first_y][second_x]
                second_cipher = self.Letter_Array[second_y][first_x]
                cipher += first_cipher + second_cipher
        
        return cipher
    
    def init_cipher(self, cipher_text: str):
        cipher_text = tuple(cipher_text)
        return [cipher_text[i : i+2] for i in range(0, len(cipher_text), 2)]
        
    def Dercypt(self, cipher_text: str):
        
        cipher_twins = self.init_cipher(cipher_text)
        plain = ""

        for cipher_twin in cipher_twins:
            first_x = self.Letter_Array_Pos[cipher_twin[0]][1]
            first_y = self.Letter_Array_Pos[cipher_twin[0]][0]
            second_x = self.Letter_Array_Pos[cipher_twin[1]][1]
            second_y = self.Letter_Array_Pos[cipher_twin[1]][0]

            if first_x == second_x:
                first_cipher = self.Letter_Array[(first_y - 1) % 5][first_x]
                second_cipher = self.Letter_Array[(second_y - 1) % 5][second_x]
                plain += first_cipher + second_cipher
            elif first_y == second_y:
                first_cipher = self.Letter_Array[first_y][(first_x - 1) % 5]
                second_cipher = self.Letter_Array[second_y][(second_x - 1) % 5]
                plain += first_cipher + second_cipher
            else:
                first_cipher = self.Letter_Array[first_y][second_x]
                second_cipher = self.Letter_Array[second_y][first_x]
                plain += first_cipher + second_cipher
        
        return plain

pf = Play_Fair("monarchy")

for line in pf.Letter_Array:
    print(line)
    
plain = pf.Dercypt("RB")

# print(cipher)
print(plain)
