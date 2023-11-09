from hashlib import sha256
from string import ascii_lowercase
from itertools import product

with open("下載.png", "rb") as f:
    print(sha256(f.read()).hexdigest())

