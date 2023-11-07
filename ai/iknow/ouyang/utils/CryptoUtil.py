import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad

key = b'1234567891234567'
iv = b'1234567891234567'
print(len(key))


def _pad(par):
    par = par.encode('utf-8')
    while len(par) % 16 != 0:
        par += b'\x00'
    return par


def encrypt(data: str):
    byte = pad(data.encode("utf-8"), 16, "pkcs7")
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(byte)
    return base64.encodebytes(ciphertext).decode("utf-8").strip("\n")


def decrypt(data: str):
    byte = data.encode("utf-8")
    byte = base64.decodebytes(byte)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = unpad(cipher.decrypt(byte), 16, "pkcs7")
    return ciphertext.decode("utf-8")


content = b"3L/VB8EtV3eTocZh55wIFZfTp2x+C/Qn+EQ3wesnwgKUsEO/dQnlIYsaOimR7hsY8+qSgKATvR9W6izam+qm0Q=="
encode = b'P2VBelySWQogHdAnc6jlZzDdxCW7RdnXE5MKMiqLlZu/WL108mduU+OIioX6c0Io'
# byte = base64.decodebytes(content)
# print(byte)
byte = encrypt("好好学习天天向上")
print(byte)
string = decrypt(byte)
print(string)
