# Harvester 

*static analysis*

- 64-bit ELF binary that was `not stripped` and that is dynamically linked.
- All the protections enabled in the binary.

```
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled

```

*Dynamic Analysis*

- Running the binary we can see a classic CTF menu where we have options to choose from.
- The following are the diffrent functions in the binary

`fight`: 
       This is a function that enables us to leak address looking at the disassembly of the function it calls `printf` with only the rdi register that
       is the input we passed in via `read` therefore a `format string` vulnerability.

`Inventory`:
        - This is a function that basically enables us control the value of `pie` and prints the value.
        - It prompts us to drop some and we can select the number of values we want to drop
        and they will be subracted from the pie.
        
`Stare`
        - This is a value that prompt us for input that leads to a buffer overflow only if the value
        of pie the variable is `0x16`.

## Exploitation

1. Using fight leak the address of libc from the stack. Leaking the address of `__libc_start_main_ret`.
2. Using fight to leak the address of the `canary` since the canary protection is enabled.
3. Call inventory to control the value of PIE that is pass `-11` when prompted and this will give us `21` as out new pie value
4. Call stare that adds one to `pie` therefore giving us `0x16` and its prompts for input that leads to a buffer overflow.
5. Find the offset to the stack cookie and since only a minium of `0x40` bytes in read in return to a one_gadget address and get a shell

Final exploit [solution.md](asd.py)


