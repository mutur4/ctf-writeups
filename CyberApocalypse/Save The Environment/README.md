# Save The Environment

*Static Analysis*

- This is was a 64-bit elf binary file that was dynamically linked and not stripped.
- The file had every other protection enabled apart from `pie`.
- Looking at the string something intresting was the `./flag.txt` strings. Therefore this meant that the binary has a function that reads the flag.
- Therefore a `ret2win` binary challenge

*Dynamic Analysis*

- Running the binary, there are 2 options

* `Plant`
        - This was a function that enabled us to write were we wanted.
* `Recyle`
      - This was a function that enabled us to leak address if only the value
      of `rec_count` was `0xa(10)`.
       
 ## Exploitation
 
 - My very first idea was to write into the `fini_array` so that the `hidden_resrouces`
 function is called as a destructor function when main returns. But the region was not writable =(
 and writing there the program crashed.
 - We can not write into `got` because we have `full relro` enabled.
 - Finally an idea came in `environ` this is a pointer that points to environment variables
 on the stack. This is the third pointer that is passed to main `int main(int argc, char **argv, char **environ)`
 - Therefore leaking the address of `libc` to find `libc_base` that will be used to find the address of environ.
 - Finally leaking the address of `environ` and getting a stack address. The return address of main is `environ + 0xf` in ctf challenges
 but on your system it might be diffrent.
 - The return address of `main - 48` will give us the return address of `plant` function and therefore we can overwrite this 
 region using the `write anywhere` leverage given to us in the `plant` function.
 - The final exploit is @ [solution](asd.py)


 `
