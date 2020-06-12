import random 
import string

def gen_id(size: int):
    return ''.join(random.choice(string.ascii_uppercase+string.digits) for _ in range(size))