
## System DROP

*static Analysis*
- This was a 64-bit elf binary that was not stripped and that was dynamically linked.
- There was no `canary` and `pie` enabled in the binary. `Partial Relro` was also enabled.

*Dynamic Analysis*
- The binary did not do much that it got our input using `read` and exited.
- There were 2 functions `_syscall` that gave us a `syscall` gadget and `main` function
that was used to get our input.

### Exploitation

- There is a buffer overflow at offset `40` we can control our return pointer.
- This was not the intended way of exploitation but the exploitation was as follows

      * Leak the address of libc using `write syscall` since we can control the value of 
        `rax` using read.

      * Look up the address of libc leaked and using `rop` return to libc that is call system
        and the address of `binsh`


- The final exploit is [exploit.py](exploit.py)

