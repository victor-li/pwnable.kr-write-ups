# mistake

The home folder of this challenge contains the following:

```
mistake@ubuntu:~$ ls -l
total 24
-r-------- 1 mistake_pwn root      51 Jul 29  2014 flag
-r-sr-x--- 1 mistake_pwn mistake 8934 Aug  1  2014 mistake
-rw-r--r-- 1 root        root     792 Aug  1  2014 mistake.c
-r-------- 1 mistake_pwn root      10 Jul 29  2014 password

```

### mistake.c
```c
#include <stdio.h>
#include <fcntl.h>

#define PW_LEN 10
#define XORKEY 1

void xor(char* s, int len){
	int i;
	for(i=0; i<len; i++){
		s[i] ^= XORKEY;
	}
}

int main(int argc, char* argv[]){

	int fd;
	if(fd=open("/home/mistake/password",O_RDONLY,0400) < 0){
		printf("can't open password %d\n", fd);
		return 0;
	}

	printf("do not bruteforce...\n");
	sleep(time(0)%20);

	char pw_buf[PW_LEN+1];
	int len;
	if(!(len=read(fd,pw_buf,PW_LEN) > 0)){
		printf("read error\n");
		close(fd);
		return 0;		
	}

	char pw_buf2[PW_LEN+1];
	printf("input password : ");
	scanf("%10s", pw_buf2);

	// xor your input
	xor(pw_buf2, 10);

	if(!strncmp(pw_buf, pw_buf2, PW_LEN)){
		printf("Password OK\n");
		system("/bin/cat flag\n");
	}
	else{
		printf("Wrong Password\n");
	}

	close(fd);
	return 0;
}

```

The mistakes that are made on this line:

```
if(fd=open("/home/mistake/password",O_RDONLY,0400) < 0){
```

and on this line:

```
if(!(len=read(fd,pw_buf,PW_LEN) > 0)){
```

Because the `<` and `>` operator have a higher precedence than the `=` operator, the expression on the right side of the `=` operator is evaluated first.

`open("/home/mistake/password",O_RDONLY,0400) < 0` will return 0 (false) is the file is correctly loaded, therefore `fd` will always be `0`.

In `C`, the file descriptor `0` indicates the `stdin` file stream. Because `fd` is always 0, `read()` will copy the content of the `stdin` stream to `pw_buf`!

The password will be checked on this line:
```
if(!strncmp(pw_buf, pw_buf2, PW_LEN)){
```

`pw_buf` and `pw_buf2` will be read from the `stdin` stream, therefore we have full control over this control statement.

Every character in `pw_buf2` will be first xor'ed with `1` before it will be compared with `pw_buf`. Therefore we need to find two characters where `c1 ^ 1 = c2`. This means that only the last bit flips in the xor operation.

There are many combinations possible, but I picked `0` and `1`. In ascii their hex value is `60` and `61` respectively. You can use python to verify that you have the correct values:

```
Python 2.7.10
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.34)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 60 ^ 1
61
>>> 61 ^ 1
60
```

Use these characters to solve the challenge:

```
mistake@ubuntu:~$ ./mistake
do not bruteforce...
0000000000
input password : 1111111111
Password OK
Mommy, the operator priority always confuses me :(
```
