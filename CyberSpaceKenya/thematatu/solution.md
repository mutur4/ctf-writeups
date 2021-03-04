## The Matatu Vault

> **Tags**: RE,Reverse Engineering
>
> **Description**: A simple checker for input, constraint solve is a good thing
>
> **author**: jimm

## Solution
*Static Analysis*
* `file` command gives details about the file and it is an `elf` executable `64-bit` binary, statically linked and not stripped.
* `radare` comes with a handy tool `rabin2` that can be used to get more info about the binary including the backend language it was written in 
therefore `rabin2 -I matatu` gives the following output.
```
arch     x86
baddr    0x400000
binsz    2147017
bintype  elf
bits     64
canary   false
class    ELF64
crypto   false
endian   little
havecode true
laddr    0x0
lang     go
linenum  true
lsyms    true
machine  AMD x86-64 architecture
maxopsz  16

```
- From the above output we can see `lang go` therefore the binary is a binary written in `go` language. 
- Looking at the strings in the binary too much information because it is a `statically` linked binary but it is worth checking.

*Dynamic Analysis*

- Fire up your favorite debugger and load the binary. I used `gdb` `r2`. Since this is a binary written in `go` and is not stripped lets check the 
entry point that is `main.main()` function.
- We can see the binary takes out input at the address `0x0048e869` and this is where `Scan` is called to get out input. The pointer to out input is then loaded into the register `rcx` and a check is done to first check is the len of our input is less that or equal to `0x2`
- If the len is greater that `0x2` the execution continues else a function is called that throws an error and loops back to get our input.
- It then checks our input for various lengths and on conclusion we see that the input we provide should not be less that or equal to`0x16` bytes
that is 22 in decimal.
- Since our input is loaded in `rcx` resgister therefore the binary checks if each byte in `rcx` meets some certain conditions an exmaple is 
`mov ebx, BYTE PTR [rcx+0x2];cmp bl, 0x74`. This is a check used to check that the 3rd letter of our input should be equal to 0x74 that is `t`
in ascii.
- If we have everything right based on the checks, a function `main.win()` is called.
- Reversing all this by hand is possible and requires you to do some complex math therefore we will write a simple python script that will do 
the math for us.

*Solution*

- Using all the details above we can now write a simple script to do the math. We will be using python and `angr` framework more can be read [here](https://angr.io) this is an amazing tool that is used in reversing. 
- The final exploit [exploit.py](asd.py)

