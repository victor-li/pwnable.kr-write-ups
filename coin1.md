# coin1

The summary of the challenge:

```
	---------------------------------------------------
	-              Shall we play a game?              -
	---------------------------------------------------

	You have given some gold coins in your hand
	however, there is one counterfeit coin among them
	counterfeit coin looks exactly same as real coin
	however, its weight is different from real one
	real coin weighs 10, counterfeit coin weighes 9
	help me to find the counterfeit coin with a scale
	if you find 100 counterfeit coins, you will get reward :)
	FYI, you have 30 seconds.

	- How to play -
	1. you get a number of coins (N) and number of chances (C)
	2. then you specify a set of index numbers of coins to be weighed
	3. you get the weight information
	4. 2~3 repeats C time, then you give the answer

	- Example -
	[Server] N=4 C=2 	# find counterfeit among 4 coins with 2 trial
	[Client] 0 1 		# weigh first and second coin
	[Server] 20			# scale result : 20
	[Client] 3			# weigh fourth coin
	[Server] 10			# scale result : 10
	[Client] 2 			# counterfeit coin is third!
	[Server] Correct!

	- Ready? starting in 3 sec... -
```

As long as `N <= 2^C`, it is possible to find the counterfeit coin by using binary search. By splitting subsets of coins in half, we are able to determine exactly which coin is a counterfeit.

For every subset, the first half of the coins will be submitted to the server. If the `total weight % 10 == 0`, then we know that the counterfeit coin is in the second half of the coins, else, the counterfeit coin is in the first half. The half with the counterfeit coin will be the subset for the next iteration.

In my case, the Python code needs to be executed on the `pwnable.kr` server, because the response from the server is too slow when I execute it from my computer and then the challenge times out. Do not forget to change the host address to `localhost` when the code in executed from the `pwnable.kr` server.

The code that I used for this challenge can be found [here](src/coin1.py).

```
someserver@ubuntu:/tmp/test$ python client.py
.
.
.
Correct! (99)
Congrats! get your flag
b1NaRy_S34rch1nG_1s_3asy_p3asy
```