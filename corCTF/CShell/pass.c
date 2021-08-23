#include <stdio.h>
#include <stdlib.h>
#include <crypt.h>

int main(int argc, char **argv){
	char *hash;
	char salt[5] = "1337\0";
	hash = crypt("password", salt);
	printf("%s\n", hash);
	return 0;
}
