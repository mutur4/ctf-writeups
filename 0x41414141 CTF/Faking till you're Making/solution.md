## Faking till you're Making


### Challenge Overview

There was yet another `PoW` file that required a 4 letter lowercase word whose hash was in sha256.
There was a `vuln` file that was a 64-bit elf executable, dynamically linked and not stripped. There is no `canary` enabled.

### Exploit Overview

I bypassed the `proof of concept` with python `string`, `hashlib` and `itertools permutations`.

The `vuln` file had a description that mentioned `maleficarum`. If you are familiar with heap exploitation, this meant that the 
challenges was based on exploiting the heap. Running the binary with some random input some address was leaked 
and it triggered a `free(): invalid pointer` error.

Checking the address that is leaked this is the address of a function `sh` that calls system and binsh giving us a shell.We 
need to find a way to control rip and call this function.

The `invalid pointer` error is thrown when we try to `free` a chunk of memory that was not previously allocated by malloc. Analysing the binary 
using `gdb` we can see that the memory that is being passed to `free` is a memory address from the stack. 

This is a block of memory that we control.The first call to `read` gets our input from the command line to this `address+16` on the stack.
Using this information we need to find a way to overwrite the `ret` address with the leaked address of `sh`.

> To control `rip` we need to do the following

1. Create our fake fastbin chunk (make sure it is the same size as the second request 
by malloc) and `free` will therefore add the fastchunk in the fastbin.
2. The second call to `malloc` requests `0x30` which is a fastchunk and this will be pulled out from the fastbin now the fake chunk we 
created.
3. `fgets` into the new allocated chunk leads to a `heap overflow` since the chunk is a memory block from the stack we can overflow 
and overwrite the saved return pointer with the adddress of `sh()` and get a shell :)

The final exploit is @ [exploit.py](exploit.py)

## flag

flag{seems_h0us3_0f_sp1r1ts_w0rks_0n_2.32_then_58493}



