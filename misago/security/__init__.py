from django.utils import crypto
    
def get_random_string(length):
    return crypto.get_random_string(length, "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")