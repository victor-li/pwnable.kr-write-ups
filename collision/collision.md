# collision

The home folder of this challenge contains the following:

```
col@ubuntu:~$ ls -l
total 16
-r-sr-x--- 1 col_pwn col     7341 Jun 11  2014 col
-rw-r--r-- 1 root    root     555 Jun 12  2014 col.c
-r--r----- 1 col_pwn col_pwn   52 Jun 11  2014 flag
```

### col.c
```c
#include <stdio.h>
#include <string.h>
unsigned long hashcode = 0x21DD09EC;
unsigned long check_password(const char* p){
    int* ip = (int*)p;
    int i;
    int res=0;
    for(i=0; i<5; i++){
        res += ip[i];
    }
    return res;
}

int main(int argc, char* argv[]){
    if(argc<2){
        printf("usage : %s [passcode]\n", argv[0]);
        return 0;
    }
    if(strlen(argv[1]) != 20){
        printf("passcode length should be 20 bytes\n");
        return 0;
    }

    if(hashcode == check_password( argv[1] )){
        system("/bin/cat flag");
        return 0;
    }
    else
        printf("wrong passcode.\n");
    return 0;
}
```

As you can see from the code, the password length needs to be 20 bytes, which is equal to 5 integers (1 int = 4 bytes). The sum of the 5 integers from the input needs to be equal to `0x21DD09EC` to obtain the flag. Let's find 5 integers that are in total equal to `0x21DD09EC`:

```
Python 2.7.10
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.34)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> 0x21DD09EC
568134124
>>> 568134124 / 5
113626824
>>> 568134124 - 4 * 113626824
113626828
>>> 4 * 113626824 + 113626828
568134124
```

We found that `4 * 113626824 + 113626828` equals `0x21DD09EC`. The next step is to convert the integers to bytes. The tricky part here is that in C, integers are stored in little-endian format. Therefore the byte order of the integers is reversed.

I use `struct.pack` to directly convert integers into the little endian byte representation. The first argument of `struct.pack` (the format of the conversion) consists of two parts: `<` means that the bytes need to be in little-endian order, and `i` means that it needs to be converted to the size of an int.

```
>>> import struct
>>> 4 * struct.pack('<i', 113626824) + struct.pack('<i', 113626828)
'\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xcc\xce\xc5\x06'
```

Now that we have our byte string, we can use it to solve the challenge:

```
col@ubuntu:~$ ./col `echo -n -e "\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xc8\xce\xc5\x06\xcc\xce\xc5\x06"`
daddy! I just managed to create a hash collision :)
```
