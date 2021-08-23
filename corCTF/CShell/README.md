## Challenge __(CShell)__

- This is a typical ctf challenge with a binary file and the source code.
- From the source code we can see that we can only gain shell when the 
uid is 0.

> ###  structure of the Challenge :cry: 

- To exploit the challenge we have to find a way to become "root". Lets first 
understand the workflow of the challenge and find a way to exploit it.
- We start with what happens from the main function.

1. The binary allocates 2 chunks on the heap of the same sizes. 
	* **root_t**: 0x20 (0x30) -->  FastBinChunk.
	* **user_t**: 0x20 (0x30) -->  FastBinChunk.

2. There are 2 objects that are freed() from the heap and they are of the 
following sizes:
	* `Eric_buff` : 0x80 (0x90) --> **This is a smallbin chunk.**
	* `Charlie_buff` : 0x50 (0x60) --> **This is a fastbin chunk.**
- Both of these chunks fill up the tcache but in different indexes. Since they 
are of different sizes.

3. There is an allocation of the user object that is of the type struct_user and 
then the root allocation of the type struct_user. They are allocated in the following
way.
	* `user = malloc(sizeof(struct users)*4)`
	* `root = user + 1`

4. There follows a couple of str copies. They copy strings into the `user -> name`
and `root -> name` buffers.

5. The setup() function is called that allows us to do the following:
	* Enter the username and password.
	* Specify our own size to `malloc()` and input into this buffer
	is limited to 201 bytes. __Therefore this can be a possible heap 
	overflow when we allocate a chunk of size < 200 bytes :smile:__
	

7. The logout function looks intresting since it does the following.
	* It gets the name of the user 
	* There is a loop that checks for the username and checks if the 
	user exists if not, the program exists; if True the programs asks for 
	the password and updates `uid`
	* Using the user `root` and password `guessme=)` will never work since
	when we enter a password it is hashed first then checks against the password
	that is stored in `ptr -> ptr -> password`. Therefore our hashed `guessme=)` will
	be strcompared against the unhashed `guessme=)` and this will never be true.

## Exploitation

- We need to find a way to chain the freed chunks in the tcache and the possible heap overflow.
- The structure of the heap will be as follows.
 
	```
	+-------------------------------+
	| 	Address of root_t	 |
	+-------------------------------+
	|	Address of user_t        |
	+-------------------------------+
	| 	alex_buff		 |
	+-------------------------------+
	|	charlie_buff 	         |  ----> This is a freed fastbin chunk (Inside the Tcache)
	+-------------------------------+	
	|	johnyy buff		 |
	+-------------------------------+
	|	eric_buff		 |  -----> This is a freed SmallBinChunk (Inside the Tcache)
	+-------------------------------+
	|	user			 |
	+-------------------------------+
	| 	root 			 |
	+-------------------------------+
	```
- Therefore using the power that we have been given. The power to supply the size of
a chunk we want to allocate + 8. We will allocate (120) as the size and `malloc()` will return 
to us a chunk of the same size from the tcache that is `eric_buff` and so 
using our heap overflow vuln we can overflow into `root`and write into the `root->password`
with our desired hashed password.
- When we now `logout()` and provide the username as `root` and password as `our_unhashed_password`
this will bypass the check `strcmp(hash, ptr -> ptr >password)`.
- Checking `whoami` we are now root and can now spawn a shell =).
- The exploit python code is @ [exploit file](asd.py).





