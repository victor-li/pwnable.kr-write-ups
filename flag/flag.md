# flag

The binary of this challenge can be found here: <http://pwnable.kr/bin/flag>.

Let's execute the binary to see what it does:

```
root@kali:~# ./flag
I will malloc() and strcpy the flag there. take it.
```


The first obvious step is to use `strings` to see if we find some interesting strings in the binary directly:

```
# Check how many strings can be found in ./flag
root@kali:~# strings ./flag | wc -l
5279

# Check how many strings contains at least 10 characters
root@kali:~# strings ./flag | grep '[^ ]\{10\}' | wc -l
78

root@kali:~# strings ./flag | grep '[^ ]\{10\}'
[truncated]
$Info: This file is packed with the UPX executable packer http://upx.sf.net $
[truncated]
```

It seems that the executable is packed with the UPX executable packer. Let's try to unpack it:

```
root@kali:~# upx -d ./flag
                       Ultimate Packer for eXecutables
                          Copyright (C) 1996 - 2013
UPX 3.91        Markus Oberhumer, Laszlo Molnar & John Reiser   Sep 30th 2013

        File size         Ratio      Format      Name
   --------------------   ------   -----------   -----------
    887219 <-    335288   37.79%  linux/ElfAMD   flag

Unpacked 1 file.
```

It worked! Let's see if we can find the string `I will malloc() and strcpy the flag there. take it.`:

```
root@kali:~# strings ./flag | grep 'I will'
I will malloc() and strcpy the flag there. take it.
```

The string appears to be in the executable without any obfuscation. Let's see the surrounding lines of this string:

```
root@kali:~# strings ./flag | grep -C 5 'I will'
([]A\A]A^A_
[]A\A]A^A_
AUATUSH
[]A\A]
UPX...? sounds like a delivery service :)
I will malloc() and strcpy the flag there. take it.
FATAL: kernel too old
/dev/urandom
FATAL: cannot determine kernel version
/dev/full
/dev/null
```

The flag appears to be unobfuscated as well! Flag: `UPX...? sounds like a delivery service :)`