import random
import string

def gen_password(N):
    '''
    Generates a random password of length N cosisting of numbers and letters.
    '''
    word = ''
    for _ in range(N):
        word+= random.SystemRandom().choice(string.ascii_letters + string.digits)
    return word
