## Challenge *ChainBlock*

- The binary file is an `x64` elf binary file and looking at the protections
only `nx`is enabled.
- The input is taken using `gets()` and therefore this is a basic `bof`.
at the offset `264`

### Exploitation

- The challenge can be exploited using the following technique:
	* Leak libc address to get the `__libc_base` address.
	* Since we are given the libc file, we use the base address to get the 
	actual address of `system()` and `binsh` at runtime. Since they are randomized.
	* return to libc and get a shell :smile:

- The basic exploit is @ [exploitation file](asd.py)
