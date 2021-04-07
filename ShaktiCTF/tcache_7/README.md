## CACHE_7

- This is a heap challenge where we are given a filename and the libc file.
- Since the libc version is 2.27 that means we are dealing with the tcache that was introduced in libc version 2.26.

*static Analysis*

- Using the commands `file chall && checksec chall && rabin2 -i chall rabin2 -z chall`. Therefore we can definately see 
the type of file and the different file protections there is.
- The file has all protections enabled and it is a 64-elf binary that is `not stripped` and `dynamically linked`.

*Dyamic Analysis*

- There are various functions in the binary and they are `add, view, delete and quit`. The function of focus here are the 
`delete`, `view` and `add` functions.

- These functions do the following

1. Add:

        - This is a function that is used to malloc a chunk based on the input that we give. That is the size and the data.
        - The chunk refrence is stored in the bss section.
        - When another chunk is allocated the refrence chunk is replaced with the address of the new chunk.
         
3. Delete:

        - This is used to free the chunk and therefore the chunk is placed in a tcache bin based on the given libc version.
        - The chunk refrence at the bss section at ptr is not replaced with a null value

5. View
        
        -  This is used to print the value at ptr in the bss section.
       
# Exploitation

- For a heap exploitation challenge I do look for the following common bugs that will therefore lead to some more complicated bugs

        1. Heap Overflow 
        2. Use After Free
        3. Double Free

- Since the pointer that was `freed` is not replaced by null therefore this leads to a `UAF` bug.
- The `UAF` bug leads to `Double Free` bug and this is where we can free out chunk more than 2 times.
- Therefore we can use these bugs to leak libc address and gain shell =)

*Leak Address*

- Using the `Double Free Bug` we can tcache dup into bss at `ptr`.
- When a chunk is deleted 2 times therefore the tcache will be a follows [chunk1---->chunk1]
- Therefore this means that we can control the fd pointer to point to the address of `ptr` in memory.
- When we then allocate a chunk we will therefore end up with `ptr` as a chunk and write into it the value of `elf.got.setbuf`
- We will then leak the address at libc by calling `view` that will print the value at `ptr` which is out got address.

*pop shell*

- tcache dup into `__free_hook` and that address with the address of system or the address of `one_gadget` and gain a shell.
- Therefore the final [exploit](exploit.py)
