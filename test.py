import random
import string

# generates a random password of length N cosisting of numbers and letters
def gen_password(N):
    word = ''
    for _ in range(N):
        word+= random.SystemRandom().choice(string.ascii_letters + string.digits)
    return word

print(gen_password(10))
