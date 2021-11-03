import string
import random


def generate_random_key(length: int = 8) -> str:
    """ Generates a random key using uppercase, lowercase ascii letters and digits """
    random_characters = (random.choice(string.ascii_letters + string.digits) for i in range(length))
    return ''.join(random_characters)