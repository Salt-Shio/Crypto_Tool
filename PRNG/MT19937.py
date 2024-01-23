def int32(num: int):
    return 0xffffffff & num 

class MT19937:
    def __init__(self, seed) -> None:
        self.seed = seed
        self.mt = [0] * 624
        self.mt_index = 0
        self.mt[0] = seed

        for i in range(1, 624):
            self.mt[i] = int32(1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)
        
        # print(self.mt)
        
    def twist(self):
        for i in range(624):
            tmp = int32((self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = (tmp >> 1) ^ self.mt[(i + 397) % 624]
            self.mt[i] = self.mt[i] ^ 0x9908b0df if (not tmp % 2 == 0) else self.mt[i]
    
    def extract_randnum(self):
        if self.mt_index == 0:
            self.twist()
        
        ret = self.mt[self.mt_index]
        ret = ret ^ (ret >> 11)
        ret = ret ^ (ret << 7) & 0x9d2c5680
        ret = ret ^ (ret << 15) & 0xefc60000
        ret = ret ^ (ret >> 18)

        self.mt_index = (self.mt_index  + 1) % 624

        return int32(ret)

