# random

The home folder of this challenge contains the following:

```
random@ubuntu:~$ ls -l
total 20
-r--r----- 1 random_pwn root     49 Jun 30  2014 flag
-r-sr-x--- 1 random_pwn random 8538 Jun 30  2014 random
-rw-r--r-- 1 root       root    301 Jun 30  2014 random.c

```

### random.c
```c
#include <stdio.h>

int main(){
	unsigned int random;
	random = rand();	// random value!

	unsigned int key=0;
	scanf("%d", &key);

	if( (key ^ random) == 0xdeadbeef ){
		printf("Good!\n");
		system("/bin/cat flag");
		return 0;
	}

	printf("Wrong, maybe you should try 2^32 cases.\n");
	return 0;
}
```

In this challenge we need to make sure that `key ^ random` is equal to `0xdeadbeef` to obtain the flag. It is known that the `rand()` method is insecure for random number generation. The numbers that this method generates are predictable and are just a numerical state of a predetermined formula. When the seed is not given for the `rand` method, the seed will always be starting on `1`. Therefore `rand` will always give the same answer when the method in only called once in the program.

Not every OS/system has the same implementation of the `rand` function. Therefore we need to determine which random value will be generated on the server.

### /tmp/test/rand.c
```c
#include <stdio.h>

int main(){
        unsigned int random;
        random = rand();

        printf("%d\n", random);
        return 0;
}
```

```
random@ubuntu:/tmp/test$ gcc rand.c -o rand
random@ubuntu:/tmp/test$ ./rand
1804289383
```

Now we have determined the "random" value, we can calculate the key we need to input to obtain the flag. `key ^ random = 0xdeadbeef` => `random ^ 0xdeadbeef = key`.

```
Python 2.7.10
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.34)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 1804289383 ^ 0xdeadbeef
3039230856
```
We found the key! Now we can use it to obtain the flag.

```
random@ubuntu:~$ ./random
3039230856
Good!
Mommy, I thought libc random is unpredictable...
```
