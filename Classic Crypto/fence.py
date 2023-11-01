
class Fence:
    def __init__(self, High) -> None:
        self.High = High
        self.chunk_size = High * 2 - 1

    def offset_counter(self, high_idx):
        first = self.chunk_size - 1 - 2 * high_idx
        second = self.chunk_size - 1 - first

        if first == 0:
            return second, second
        if second == 0:
            return first, first

        return first, second


    def Encrypt(self, plain_text: str):
        cipher = ""
        
        plain_list = list(plain_text) + [''] * self.chunk_size

        for i in range(self.High):
            step_idx = 0
            step = self.offset_counter(i)
            index = i

            while index < len(plain_text):
                cipher += plain_list[index]
                index += step[step_idx]
                step_idx = (step_idx + 1) % 2

        return cipher

    def Decrypt(self, cipher_text: str):
        plain = [' '] * len(cipher_text)
        cipher_list = list(cipher_text) + [' '] * self.chunk_size
        cipher_index = 0

        for i in range(self.High):
            step_idx = 0
            step = self.offset_counter(i)
            index = i
            while index < len(cipher_text):
                plain[index] = cipher_list[cipher_index]
                index += step[step_idx]
                step_idx = (step_idx + 1) % 2
                cipher_index += 1
        return "".join(plain)


cipher = "Ta _7N6D49hlg:W3D_H3C31N__A97ef sHR053F38N43D7B i33___N6"

for high in range(2, 10, 1):
    fence = Fence(high)
    print(fence.Decrypt(cipher))


# 演算法
# 根據高度 High 跑 i = 0, 1, 2, ... High - 1
# 透過 i 計算每一行的間隔，必定是兩個一組
# 如果計算出來有 0 ，說明 間格是 固定一種

# casear + affine cipher(1格) => 屁
