""" creates passwords """
import string, random

def new(length):
    if length is None:
        length = 16
    chars = string.letters + string.digits + string.punctuation
    password = ''.join((random.SystemRandom().choice(chars)) for i in range(length))
    return password
