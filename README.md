# Scoring Playground

_Are you sick of seeing those three **P**s on top of the scoreboard?_

_Do you think the challenges scores were dropping too fast, and that
caused stress and frustration in your team members - leading to an
unhealthy consumption of alcoholic beverages?_

_Do you believe that just a tiny change in one of the 
parameters of the scoring algorithm would have been enough to get you and your team
to Vegas, wearing a tuxedo, ready to sign authographs on the Defcon red carpet?_

We hear your complains. 

So, now go ahead and customize the scoring system the way you prefer.

### Howto 

This project includes a `json` file with all successful submissions of 
the Defcon CTF Quals 2019 and a python script to test different scoring
systems.

To compare different outcomes, follow these simple rules:

1. Check the `teams.conf` and `challs.conf` files. They contain,
   respectively, the list of teams and challenges you want to work with.
   By default, the tool simulates the top 30 teams and all challenges
   except the _speedrun_.
2. Run `./scorep.py data_2019.json` to print the final scoreboard obtained by
   the same algorithm and the same parameters we used in the Defcon 2019 quals.
   You can then run `./scorep.py -w dc19 data_2019.json` to save this
   result as a reference file for future comparisons.
3. Time to play. Run the tool without parameters to see all its option.


### Examples (basic use)

The final scoreboard is defined by three algorithms: the
**ranking** algorithm (which decides how to sort the teams and break
ties), the **scoring** algorithm (which assigns a score to each
challenge), and an optional **bonus** algorithm (which assign extra
points to certain teams).

So, let's just see the results according to the OOO algorithms:

```
> ./scorep.py data_2019.json
-------------------------------=[ Config ]=------------------------------------------
Scoring: 100 + ( 500 - 100 ) / (1 + 0.08 * Solved(2880) * Log (1 * Solved(2880)))
Ranking: score,first
Bonus:   None
Teams:   30        Challs:   24
-------------------------------    --------------------------------------------------
 #  Score  Team                     Score Solves 1st   Challenge
-------------------------------    --------------------------------------------------
 1 -  3591 PPP                         500    1   23  LCARS333
 2 -  3371 HITCON⚔BFKinesiS            460    2  751  papatrace
 3 -  3035 Shellphish                  271    8  420  election_coin
 4 -  2877 Sauercloud                  254    9   35  LCARS022
 5 -  2863 Samurai                     240   10  309  chainedrsa
 6 -  2860 A*0*E                       201   14  190  ASRybaB
 7 -  2695 SeoulPlusBadAss             187   16  408  Hotel-California
 8 -  2659 Tea Deliverers              182   17   74  tania
 9 -  2547 CGC                         162   22  105  shitorrent
10 -  2547 hxp                         156   24  193  LCARS000
11 -  2478 r00timentary                143   30  467  RTOoOS
12 -  2405 KaisHack GoN                142   31   26  mamatrace
13 -  2341 TokyoWesterns               139   33  156  VeryAndroidoso
14 -  2277 r3kapig                     137   34  162  ooops
15 -  2223 Tasteless                   135   36  117  gloryhost
16 -  2218 RPISEC                      131   40  171  vitor
17 -  2165 mhackeroni                  127   45   49  Return_to_shellQL
18 -  2164 OpenBlue                    118   61   78  nodb
19 -  2061 binja                       114   76   55  babytrace
20 -  1996 pasten                      112   88   40  babyheap
                                      110  102   45  redacted-puzzle
                                      108  122   39  know_your_mem
                                      102  390    4  cant_even_unplug_it
                                      100 1252    0  welcome_to_the_game
```

The output is divide in three parts. On the top, you have all the deails of the scoring
algorithms you selected. On the bottom left the actual scoreboard. And on the bottom
right the list of challenges with their individual score, the number of teams
who solved them, and the time it took for the first team to do that.

If you now save this ranking by using `-w` option, you can easily print 
what would have changed by using a different scoring algorithm.
For instance, let's compare against the exponential decay used by the CCC CTF:

```
> ./scorep.py -c dc19 -s ccc  data_2019.json
-------------------------------=[ Config ]=------------------------------------------
Scoring: 30 + ( 500 - 30 ) / (1 + (max(0, Solved(2880)-1)/ 11.92201) ** 1.206069)
Ranking: score,first
Bonus:   None
Teams:   30        Challs:   24
Reference: dc19 (-w dc19 data_2019.json)
-------------------------------    --------------------------------------------------
 #  Score  Diff  Team                        Score    Solves 1st   Challenge
-------------------------------    --------------------------------------------------
 1 -  3567   ---  PPP                         500  ---     1   23  LCARS333
 2 -  3394   ---  HITCON⚔BFKinesiS            477 + 17     2  751  papatrace
 3 -  2911   ---  Shellphish                  338 + 67     8  420  election_coin
 4 -  2833   1 ▲  Samurai                     320 + 66     9   35  LCARS022
 5 -  2770   1 ▼  Sauercloud                  304 + 64    10  309  chainedrsa
 6 -  2752   ---  A*0*E                       253 + 52    14  190  ASRybaB
 7 -  2546   ---  SeoulPlusBadAss             233 + 46    16  408  Hotel-California
 8 -  2499   ---  Tea Deliverers              224 + 42    17   74  tania
 9 -  2410   1 ▲  hxp                         188 + 26    22  105  shitorrent
10 -  2364   1 ▼  CGC                         176 + 20    24  193  LCARS000
11 -  2352   ---  r00timentary                150 +  7    30  467  RTOoOS
12 -  2179   ---  KaisHack GoN                146 +  4    31   26  mamatrace
13 -  2139   ---  TokyoWesterns               140 +  1    33  156  VeryAndroidoso
14 -  2053   ---  r3kapig                     136 -  1    34  162  ooops
15 -  1955   ---  Tasteless                   131 -  4    36  117  gloryhost
16 -  1946   ---  RPISEC                      121 - 10    40  171  vitor
17 -  1933   1 ▲  OpenBlue                    111 - 16    45   49  Return_to_shellQL
18 -  1914   1 ▼  mhackeroni                   89 - 29    61   78  nodb
19 -  1783   1 ▲  pasten                       76 - 38    76   55  babytrace
20 -  1767   1 ▼  binja                        69 - 43    88   40  babyheap
                                               63 - 47   102   45  redacted-puzzle
                                               57 - 51   122   39  know_your_mem
                                               37 - 65   390    4  cant_even_unplug_it
                                               32 - 68  1252    0  welcome_to_the_game
```

Not much eh?

Basically, only two adjacent teams switched place in the top10.

Let's say you now wants to change the first place. That won't be easy.. but after few tries I found 
one possible solution. Ranking teams not based on their score, but based only on the number of 
challenges they solved and break ties not by who score first, but by total cumulative solving time.
Here it is:

```
> ./scorep.py -c dc19 -r solved,ctime data_2019.json
-------------------------------=[ Config ]=------------------------------------------
Scoring: 100 + ( 500 - 100 ) / (1 + 0.08 * Solved(2880) * Log (1 * Solved(2880)))
Ranking: solved,ctime
Bonus:   None
Teams:   30        Challs:   24
Reference: dc19 (-w dc19 data_2019.json)
-------------------------------------------------------------------------------------

 #  Score  Diff  Team                        Score    Solves 1st   Challenge
--------------------------------------    ------------------------------------------
 1 -  3371   1 ▲  HITCON⚔BFKinesiS            500  ---     1   23  LCARS333
 2 -  3591   1 ▼  PPP                         460  ---     2  751  papatrace
 3 -  2860   3 ▲  A*0*E                       271  ---     8  420  election_coin
 4 -  2877   ---  Sauercloud                  254  ---     9   35  LCARS022
 5 -  2695   2 ▲  SeoulPlusBadAss             240  ---    10  309  chainedrsa
 6 -  2863   1 ▼  Samurai                     201  ---    14  190  ASRybaB
 7 -  2659   1 ▲  Tea Deliverers              187  ---    16  408  Hotel-California
 8 -  3035   5 ▼  Shellphish                  182  ---    17   74  tania
 9 -  2547   ---  CGC                         162  ---    22  105  shitorrent
10 -  2405   2 ▲  KaisHack GoN                156  ---    24  193  LCARS000
11 -  2547   1 ▼  hxp                         143  ---    30  467  RTOoOS
12 -  2478   1 ▼  r00timentary                142  ---    31   26  mamatrace
13 -  2341   ---  TokyoWesterns               139  ---    33  156  VeryAndroidoso
14 -  2277   ---  r3kapig                     137  ---    34  162  ooops
15 -  2218   1 ▲  RPISEC                      135  ---    36  117  gloryhost
16 -  2223   1 ▼  Tasteless                   131  ---    40  171  vitor
17 -  2165   ---  mhackeroni                  127  ---    45   49  Return_to_shellQL
18 -  2061   1 ▲  binja                       118  ---    61   78  nodb
19 -  2164   1 ▼  OpenBlue                    114  ---    76   55  babytrace
20 -  1718   3 ▲  $TLDR$                      112  ---    88   40  babyheap
                                              110  ---   102   45  redacted-puzzle
                                              108  ---   122   39  know_your_mem
                                              102  ---   390    4  cant_even_unplug_it
                                              100  ---  1252    0  welcome_to_the_game
```

Even with weird approach results in few times moving up and down a bit, but the top ten teams remain largely unmodified!

### Examples (fine grained)

Let's say you want to make some fine-grained adjustment to a 







