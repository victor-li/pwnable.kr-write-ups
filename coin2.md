# coin2

The summary of the challenge:

```
	---------------------------------------------------
	-              Shall we play a game?              -
	---------------------------------------------------

	You have given some gold coins in your hand.
	however, there is one counterfeit coin among them
	counterfeit coin looks exactly same as real coin
	luckily, its weight is different from real one
	real coin weighs 10, counterfeit coin weighes 9
	help me to find the counterfeit coin with a scale.
	if you find 100 counterfeit coins, you will get reward :)
	FYI, you have 30 seconds.

	- How to play -
	1. you get a number of coins (N) and number of chances (C) to use scale
	2. then you specify C set of index numbers of coins to be weighed
	3. you get the weight information of each C set
	4. you give the answer

	- Example -
	[Server] N=4 C=2 	# find counterfeit among 4 coins with 2 trial
	[Client] 0 1-1 2	# weigh two set of coins (first and second), (second and third)
	[Server] 20-20		# scale result : 20 for first set, 20 for second set
	[Client] 3 		# counterfeit coin is fourth!
	[Server] Correct!

	- Note -
	dash(-) is used as a seperator for each set

	- Ready? starting in 3 sec ... -
```

This challenge differs from the first problem, because in this case we need to give all the sets we want to check as input at once, instead of excluding subsets based on the previous response.

My approach is to make different groups of integers, where the integers in binary representation has its bit set on the i'th position starting from the back.

Groups will be for example:

| Group | Integers               | Binary                                                 |
|-------|------------------------|--------------------------------------------------------|
| 0     | 1, 3, 5, 7, 9, ....    | 000**1**, 001**1**, 010**1**, 011**1**, 100**1**, .... |
| 1     | 2, 3, 6, 7, 10, ....   | 00**1**0, 00**1**1, 01**1**0, 01**1**1, 10**1**1, .... |
| 2     | 4, 5, 6, 7, 12, ....   | 0**1**00, 0**1**01, 0**1**10, 0**1**11, 1**1**00, .... |
| 3     | 8, 9, 10, 11, 12, .... | **1**000, **1**001, **1**010, **1**011, **1**100, .... |

Based on the response of the server, we are able to calculate which coin is counterfeit. If the i'th group contains the counterfeit coin (`total weight % 10 != 0`), then we know that the i'th bit of the counterfeit coin is set. If not, then the bit of the counterfeit coin is not set on the i'th position.

As long as `N < 2^C`, it is possible to find the counterfeit coin by using this method.

In my case, the Python code needs to be executed on the `pwnable.kr` server, because the response from the server is too slow when I execute it from my computer and then the challenge times out. Do not forget to change the host address to `localhost` when the code in executed from the `pwnable.kr` server.

The code that I used for this challenge can be found [here](src/coin2.py).

```
someserver@ubuntu:/tmp/test$ python client.py
.
.
.
Correct! (99)
Congratz! get your flag
NoN_aDaptiv3_b1narY_S3arcHing_is_4ls0_3asY
```