## Easy-Rop

> **Description**: Welcome to the world of pwn!!This should be a good entry level warmup challenge!!
> Enjoy getting the shell
>
> **Points**: 441 points
>
>**Connection**: nc 65.1.92.179 49153


### Solution

*Static Analysis*

- Using the `file` command in linux we can see the file is a `64-bit` elf binary that 
is statically linked therefore no `got's` and `not stripped` therefore we can easily get the 
address of symbols in the binary.
- Using `rabin2 -i` to check the imports there is no information this is because the binary 
is statically linked.
- `checksec` all protections were enabled apart from `pie` therefore this me

*Dynamic Analysis*

- Running the binary, we get a message `welcome to darkcon` and the next line prompts use
for our name and the program exits.
- Fuzzing the binary and providing a long string, gives us a segmentation fault therefore 
this means we have a buffer overflow vulnerability. This is because out input was passed in 
via `get()` function.

### Exploitation

- We have a `buffer` overflow vulnerability based on out reconissance therefore we 
have to find the offset to the return address on the stack.
- The offset was `72` and therefore we can use this information to get a shell.
- Since `no nx` is enabled therefore I used `mprotect` to change the protections of
a memory region that was not affected by `aslr` e.g `bss` wrote a shell there and 
returned to the region to get a shell.
- The full exploit is [exploit](exploit.py)

