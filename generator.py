import string
import random

class Generator:
    def generate_random_string(self,length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string