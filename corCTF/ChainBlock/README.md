## Challenge *ChainBlock*

- The binary file is an elf binary file and looking at the protections
only `nx`is enabled.
- The input is taken using `gets()` and therefore this is a basic `bof`.
at the offset `264`

### Exploitation

- The challenge can be exploited using the following tech:
	* Leak libc address to get the base address.
	* Since we are given the libc file, we get the address 
	of system and binsh and get the actual address.
	* return to libc and get a shell :smile:
- The basic exploit is @ [exploitation file](asd.py)
