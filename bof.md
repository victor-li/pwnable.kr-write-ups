# bof

### bof.c
```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
void func(int key){
	char overflowme[32];
	printf("overflow me : ");
	gets(overflowme);	// smash me!
	if(key == 0xcafebabe){
		system("/bin/sh");
	}
	else{
		printf("Nah..\n");
	}
}
int main(int argc, char* argv[]){
	func(0xdeadbeef);
	return 0;
}
```

To obtain the flag, we need to make sure that the parameter `key` is equal to `0xcafebabe` such that we get a root shell. The `key` parameter that is passed from the main function is `0xdeadbeef`, therefore the key does not match. However, it is possible to overflow the `overflowme` buffer, because the content will be set by the method `gets`. Because `gets` does not take the length of the initialized array into account, it just starts writing the input string from the begin of the array until the whole string is written in memory. Therefore it is also possible to write in memory beyond the boundaries of the array and override other data in memory.

## Buffer overflow

The stack in memory grows from the high to low addresses and the heap grows from low to high.

```
|--------------------| High address
|       Stack        |
|--------------------|
|         ||         |
|         \/         |
|                    |
|         /\         |
|         ||         |
|--------------------|
|        Heap        |
|--------------------| Low address
```

This is how the stack look like when the `overflowme` buffer is allocated. The buffer starts at the lower address and ends at the higher address.

```
|--------------------| High address
|       Stack        |
|--------------------|
|      int key       | <- method parameters
|--------------------|
|    return address  | <- return address
|--------------------|
|    overflowme[32]  | <- method locals variables
|--------------------|
|                    |
|                    |
|                    |
|                    |
|     Free space     |
|--------------------|
|        Heap        |
|--------------------| Low address
```

The idea is to overflow the `key` parameter in the stack with the value that we want, which is in this `0xcafebabe`.

```
|--------------------|--------------------| High address
|       Stack        |       Stack        |
|--------------------|--------------------|
|      int key       |     0xcafebabe     |
|--------------------| ////////////////// |
|    return address  | ////////////////// |
|--------------------| //Arbitrary data// |  /\
|    overflowme[32]  | ////////////////// |  ||  Fill buffer
|--------------------|--------------------|
|                    |                    |
|                    |                    |
|                    |                    |
|                    |                    |
|     Free space     |     Free space     |
|--------------------|--------------------|
|        Heap        |        Heap        |
|--------------------|--------------------| Low address
```

## Stack smash detection

C programs compiled with the default configuration will have stack smashing detecting, which detects when a buffer overflow has occurred and that the value of the return address has been changed to an invalid address.

```
victorli@ubuntu:~$ ./bof
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX # 32x
overflow me :
Nah..
victorli@ubuntu:~$ ./bof
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX # 33x
*** stack smashing detected ***: /home/bof/bof terminated
overflow me :
Nah..
```

However, this would not be a problem for this challenge, since the stack smashing detection is done on return of the `func` method. Before that, we should already got a shell.

Because it is not always clear how many bytes will be between the `overflowme` buffer and the `key` int, we can just brute force the length of the padding before our payload until we get a shell. The `key` parameter need to become `0xcafebabe`, but because C uses the little endian format for int's, we need to reverse the byte order to `\xBE\xBA\xFE\xCA`.

The code that I used for this challenge can be found [here](src/bof.py).

If you want to read more about buffer overflowing: <https://www.sans.org/reading-room/whitepapers/threats/buffer-overflows-dummies-481>
