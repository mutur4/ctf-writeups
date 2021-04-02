## CHALLENGE DESCRIPTION

*Static Analysis*

* Using the commands `file chall && checksec chall && rabin2 -z chall && rabin2 -i chall`. The binary file has no protections and it is a 64-bit binary file.
* There are various imports in the binary including `gets` and therefore this definately leads to a buffer overflow.
* Since there is no `nx` therefore we can store shellcode in memory and execute the shellcode getting a shell.

*Dynamic Anaylsis*
- Using a debugger the binary is a small binary and uses gets to get input therefore definately a buffer overflow. The offset to the saved `rip` registers is @ 24
- Therefore we will store the shellcode @ `elf.sym.bomb` this is where out first input goes and return there to execute our shellcode


*Seccomp*

* There are some seccomp-filters in the binary that only allow the use of `open, read && write`. Therefore our shellcode should only contain the read and write 
and open syscall.
* Therefore this means we:
  * open("flag.txt", 0, 0)
  * read(rax, rsp, 0x100) : The value of rax this is the  value returned by open that is the `fd` of the opened file.
                          : The value of `rsp` that will be our buffer and this is the region where we copy the contents of the file.
  * write(1, rsp, rax): The value of `rax` this is returned by `read` and this is the number of bytes read from the opened file.

* These filters can be seen using the command `seccomp-tools dump ./chall`

```
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x09 0xc000003e  if (A != ARCH_X86_64) goto 0011
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x00 0x01 0x40000000  if (A < 0x40000000) goto 0005
 0004: 0x15 0x00 0x06 0xffffffff  if (A != 0xffffffff) goto 0011
 0005: 0x15 0x04 0x00 0x00000000  if (A == read) goto 0010
 0006: 0x15 0x03 0x00 0x00000001  if (A == write) goto 0010
 0007: 0x15 0x02 0x00 0x00000002  if (A == open) goto 0010
 0008: 0x15 0x01 0x00 0x0000003c  if (A == exit) goto 0010
 0009: 0x15 0x00 0x01 0x000000e7  if (A != exit_group) goto 0011
 0010: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0011: 0x06 0x00 0x00 0x00000000  return KILL
```
- There using pwntools shellcraft we can generate our shellcode and that can be used to read the flag.
- Therefore the final exploit code [exploit.py](exploit.py)
