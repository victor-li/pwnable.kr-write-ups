# crypto1

In this challenge, we need to find the password of the admin to obtain the flag, which is `hashlib.sha256('admin'+cookie).hexdigest()`.
The client encrypts the string `username-password-cookie`, and sends it to the server.
As a user, we have control over the content and the length of the username and password.

When the username and password are empty, the length of the encrypted packet is 64 bytes (128 bytes hex encoded).
This is also true when the username is `12 * 'a'`.
When the username is `13 * 'a'`, the encrypted packet is 80 bytes (160 bytes hex encoded).
This allows us to calculate the length of the cookie.

```
13 * 'a' + '-' + '-' + cookie + 16 * '/00' = 80 bytes
80 - 13 - 2 - 16 = 49
```

The idea is to brute-force the cookie byte for byte.
First, we encrypt the first block, without knowing what the last character is.
This will be done by sending `13 * '-'` as username.
The first 16 characters in the packet will then be `15 * '-' + the first character of the cookie`.
Next, we will send `15 * '--' + a brute-force character` as username.
We can find the first character of the cookie by matching the ciphertexts of the first encryption and the brute-force attempts. When the ciphertext matches, we have found a character of the cookie.
This can be repeated until the whole cookie is found.

```
[---------------?][????????????????] -> Calculate the ciphertext of the first block
[---------------a][????????????????]
[---------------b][????????????????]
...
[---------------y][????????????????] -> Ciphertext matches with the original ciphertext!

[--------------??][????????????????] -> Calculate the ciphertext of the first block
[--------------ya][????????????????]
[--------------yb][????????????????]
...
[--------------yo][????????????????] -> Match!
```

The code that I used for this challenge can be found [here](src/crypto1.py).

```
victorli@ubuntu:~$ python crypto1.py
...
Connecting to pwnable.kr port 9006
---------------------------------------------------
-       PWNABLE.KR secure RPC login system        -
---------------------------------------------------

Input your ID
---------------you_will_never_guess_this_sugar_honey_salt_cookie
Input your PW

sending encrypted data (c178376374b28c26c62943a8257db334e296ebacce7a3be88147f4d5fd99194e42c428906e15dba8732c4c067841541888ed5180a8bc43e5afe1fca1a981dee26d5812c4f300cbab5313f91cb761d59e333bf1c182ae937d1f15339d775465ba3300952c28529b7468c72becb33245354c4b4b5b3b32972696549e1ef6138a2d)
Found char 48: e
Cookie: you_will_never_guess_this_sugar_honey_salt_cookie
```

Now we have found the cookie, we are able to calculate the password.

```
Python 2.7.10
[GCC 4.2.1 Compatible Apple LLVM 8.0.0 (clang-800.0.34)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> import hashlib
>>> cookie = 'you_will_never_guess_this_sugar_honey_salt_cookie'
>>> id = 'admin'
>>> hashlib.sha256(id+cookie).hexdigest()
'fcf00f6fc7f66ffcfec02eaf69d30398b773fa9b2bc398f960784d60048cc503'
```

Finally, submit the correct credentials to obtain the flag!

```
victorli@ubuntu:~$ nc pwnable.kr 9006
---------------------------------------------------
-       PWNABLE.KR secure RPC login system        -
---------------------------------------------------

Input your ID
admin
Input your PW
fcf00f6fc7f66ffcfec02eaf69d30398b773fa9b2bc398f960784d60048cc503
sending encrypted data (05c4ccfd4880c92339b995c7754ec2e6567f2ed91d955cb7144c1b6037855db1b3a8525e74d30fd4505bb38c975b86f23d0e5aa23eed44b9beaa7e2195da93ba53cb08758a261ada5612245f49d25b81aa5a297aa5d555886073b17e2ed719b3607da6fbfe40b260a45485910404d69c818a2faedac7bb3a727cfbb53eab8406)
hi admin, here is your flag
byte to byte leaking against block cipher plaintext is fun!!
```