# blackjack

The source code of the challenge can be found [here](https://cboard.cprogramming.com/c-programming/114023-simple-blackjack-program.html).

This challenge is based on a very simple mistake that the programmer made.

```c
721 int betting() //Asks user amount to bet
722 {
723  printf("\n\nEnter Bet: $");
724  scanf("%d", &bet);
725  
726  if (bet > cash) //If player tries to bet more money than player has
727  {
728         printf("\nYou cannot bet more money than you have.");
729         printf("\nEnter Bet: ");
730         scanf("%d", &bet);
731         return bet;
732  }
733  else return bet;
734 } // End Function
```

This function asks the player how much he/she wants to bet this round and then checks if the betting amount is not exceeding the amount of cash that the player currently have (line 726). However, the function does not check if the betting amount is not a negative number.

After the betting function, the game starts. Based on the outcome of the cards, the logic will decide if the player or the dealer wins. Line 689 is an example of the logic that adds or subtracts cash from the balance of the player.

```c
671 void stay() //Function for when user selects 'Stay'
672 {
673      dealer(); //If stay selected, dealer continues going
674      if(dealer_total>=17)
675      {
676       if(player_total>=dealer_total) //If player's total is more than dealer's total, win
677       {
             ...
684       }
685       if(player_total<dealer_total) //If player's total is less than dealer's total, loss
686       {
687          printf("\nDealer Has the Better Hand. You Lose.\n");
688          loss = loss+1;
689          cash = cash - bet;
690          printf("\nYou have %d Wins and %d Losses. Awesome!\n", won, loss);
691          dealer_total=0;
692          askover();
693       }
694       if(dealer_total>21) //If dealer's total is more than 21, win
695       {
             ...
702       }
703      }
704      else
705      {
706          stay();
707      }
708       
709 } // End Function
```

Because negative betting amounts are possible, we are able to exploit this. To pass this challenge, we just need to make sure that we lose and that our betting amount is negative. Because we need a million to get the flag, we will set the betting amount to `-1000000`. This will result in `500 - -1000000 = 1000500` if we lose. Losing is very easy, just choose to stay on the first turn.

```
Cash: $500
-------
|C    |
|  A  |
|    C|
-------

Your Total is 11

The Dealer Has a Total of 6

Enter Bet: $-1000000


Would You Like to Hit or Stay?
Please Enter H to Hit or S to Stay.
S

You Have Chosen to Stay at 11. Wise Decision!

The Dealer Has a Total of 7
The Dealer Has a Total of 8
The Dealer Has a Total of 9
The Dealer Has a Total of 10
The Dealer Has a Total of 11
The Dealer Has a Total of 12
The Dealer Has a Total of 13
The Dealer Has a Total of 14
The Dealer Has a Total of 15
The Dealer Has a Total of 16
The Dealer Has a Total of 17
Dealer Has the Better Hand. You Lose.

You have 0 Wins and 1 Losses. Awesome!

Would You Like To Play Again?
Please Enter Y for Yes or N for No
Y

YaY_I_AM_A_MILLIONARE_LOL
```
