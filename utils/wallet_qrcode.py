import re
import sys
import base64

import qrcode
from PIL import Image
from oasis2018.settings_config.keyconfig import SECRET_KEY
from cryptography.fernet import Fernet

KEY = base64.urlsafe_b64encode(SECRET_KEY[0:32].encode("utf-8"))

def genString(_id, email, key=KEY):
    """
        inputs: str or int _id, str email, str key
        aim: take the participant id, participant email address, the word "OASIS18"
             (will be kept in plaintext), and the project encryption key and generate
             a QRCode string using AES-128 bit CBC mode encryption.
        note: the key should be generated by Fernet.generate_key and stored in an env file
        output: str (for the QRCode which will be in ciphertext)
    """
    # first do some basic input checking
    try:
        _id = int(_id)
    except:
        raise ValueError("id must be a number, {} was inputted.".format(_id))
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        raise ValueError("email must be of a valid format, {} was inputted.".format(email))

    # now generate the key using the python Cryptography library
    cipher = Fernet(key)
    plaintext = "{}_/_{}".format(_id, email).encode("utf-8")
    return (cipher.encrypt(plaintext).decode("utf-8")+"OASIS18")


def genImage(_id, email, key=KEY, **kwargs):
    """
        inputs: str _id, str email, str key, (optional kwarg) str save_location
        aim: use genString then create a qrcode
        output: PIL Image instance
    """
    qrcode_str = genString(_id, email, key)
    image = qrcode.make(qrcode_str)
    if "save_location" in kwargs.keys():
        image.save(kwargs["save_location"])
    return image


def decString(value, key=KEY):
    """
        inputs: str value, str key
        aim: take the qrcode str (value) and the key and decrypt the QRCode
             then return a tuple of the data values
        output: (id, email) if valid else bool False
    """
    # decrypt using the python Cryptography library
    cipher = Fernet(key)
    ciphertext = value[:-7].encode("utf-8") # remove the OASIS_18 part
    decoded_string = cipher.decrypt(ciphertext).decode("utf-8")
    result = decoded_string.split("_/_")[:2]

    # check to see if the decrypted values are legitimate else return False
    try:
         result[0] = int(result[0])
    except:
        return False
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", result[1]):
        return False

    return tuple(result)
