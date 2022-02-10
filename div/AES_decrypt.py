from random import randint
from Crypto.Cipher import *
import socket
import json

ip = "138.68.129.154"
port = 31713

flag = b'HTB{dummyflag}'

def gen_key(option=0):
    alphabet = b'0123456789abcdef'
    const = b'cyb3rXm45!@#'
    key = b''
    for i in range(16-len(const)):
        key += bytes([alphabet[randint(0,15)]])

    if option:
        return key + const
    else:
        return const + key

def encrypt(data, key1, key2):
    cipher = AES.new(key1, mode=AES.MODE_ECB)
    ct = cipher.encrypt(pad(data, 16))
    cipher = AES.new(key2, mode=AES.MODE_ECB)
    ct = cipher.encrypt(ct)
    return ct.hex()

def decrypt(ct, key1, key2):
    encobj = AES.new(key1,mode=AES.MODE_ECB)
    pt = encobj.decrypt(ct)
    encobj = AES.new(key2,mode=AES.MODE_ECB)
    pt = encobj.decrypt(pt)
    return(encobj.decrypt(pt))

def challenge():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    ct = s.recv(1024)[95:287]

    print(ct)

    while 1:

        key1 = gen_key()
        key2 = gen_key(1)
        
        pt = decrypt(ct, key1, key2)
        #print(pt)
        #print(key1, key2)

        if b"HTB{" in pt:
            print(key1, key2)
            print(pt)

    #ct = encrypt(flag, k1, k2)
    
    #print('Super strong encryption service approved by the elves X-MAS spirit.\n'+\
    #                'Message for all the elves:\n' + ct + '\nEncrypt your text:\n> ')
    #try:
            
        #dt = json.loads(input().strip())
        #pt = bytes.fromhex(dt['pt'])
        #res = encrypt(pt, k1, k2)
        #print(res + '\n')
        #exit(1)
    #except Exception as e:
        #print(e)
        #print('Invalid payload.\n')
        #exit(1)
    
if __name__ == "__main__":
    challenge()