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

This appliction allows you to test different scoring
systems and in the `data` directory you find several `json` files (with all successful 
flag submissions of the Defcon CTF Quals from 2019 to 2021) to play with.

To compare different outcomes, follow these simple rules:

1. Check the `teams.conf` and `challs.conf` files. They contain,
   respectively, the list of teams and challenges you want to work with.
   By default, the tool simulates the top 30 teams and all challenges
   except the _speedrun_.
2. Run `./scorep.py data/dcquals_2019.json` to print the final scoreboard obtained by
   the same algorithm and the same parameters we used in the Defcon 2019 quals.
   You can then run `./scorep.py -w dc19 data/dcquals_2019.json` to save this
   result as a reference file for future comparisons.
3. Time to play. Run the tool without parameters to see all its options.


### Examples (basic use)

The final scoreboard is defined by three algorithms: the
**ranking** algorithm (which decides how to sort the teams and break
ties), the **scoring** algorithm (which assigns a score to each
challenge), and an optional **bonus** algorithm (which assign extra
points to certain teams).

So, let's just see the results according to the OOO algorithms:

```
> ./scorep.py data/dcquals_2019.json
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

The output is divide in three parts. On the top, you have all the details of the scoring
algorithms you selected. On the bottom left the actual scoreboard. And on the bottom
right the list of challenges with their individual score, the number of teams
who solved them, and the time it took for the first team to do that.

If you now save this ranking by using the `-w` option, you can easily print 
the changes with respect to using a different scoring algorithm.
For instance, let's compare against the exponential decay approach used by the CCC CTF:

```
> ./scorep.py -c dc19 -s ccc  data/dcquals_2019.json
-------------------------------=[ Config ]=------------------------------------------
Scoring: 30 + ( 500 - 30 ) / (1 + (max(0, Solved(2880)-1)/ 11.92201) ** 1.206069)
Ranking: score,first
Bonus:   None
Teams:   30        Challs:   24
Reference: dc19 (-w dc19 data/dcquals_2019.json)
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

Not much difference, eh?

Basically, only two adjacent teams switched place in the Top10.

Let's say you now want to find something to change the winning team. 
That won't be easy.. as PPP wins in almost any reasonable setup. But after few tries I found 
one possible solution. Ranking teams not based on their score, but based only on the number of 
challenges they solved and break ties not by who score first, but by total cumulative solving time.
Here it is:

```
> ./scorep.py -c dc19 -r solved,ctime data/dcquals_2019.json
-------------------------------=[ Config ]=------------------------------------------
Scoring: 100 + ( 500 - 100 ) / (1 + 0.08 * Solved(2880) * Log (1 * Solved(2880)))
Ranking: solved,ctime
Bonus:   None
Teams:   30        Challs:   24
Reference: dc19 (-w dc19 data/dcquals_2019.json)
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

What's interesting is that even with this weird approach, few teams move up and
down a bit, but the teams in the top ten remain largely the same!

It is easy to overestimate the impact of the scoring algorithm on the final
result (I know because I certainly spent too much time thinking about it). 
But in reality, it seems like the impact is mostly psychological and 
the top teams will score equally well no matter how you configure your 
scoring.

### Examples (fine grained)

Let's say you want to make some fine-grained adjustment to one of the algorithms. 
For instance, you want to test CTFd parabolic function, but by tweeking the decay parameter.

First, run the tool without options to see the full help. Here is the snippet we are
interested in:

```
  - ctfd  Parabolic function available in ctfd.
          Format: ctfd:base,top,decay,time
          Points: max(base, (((base - top)/(decay**2)) * (Solved(@time)**2)) + top)
          Default value: ctfd:100,500,20,2880
```

So, we can configure the parameters of each algorithm by passing them after the colon sign.
In our case, the default is `ctfd:100,500,20,2880` and the decay value is in third position.

You want to see what happens if you set it to 50 instead of 20?
Just run:

```
./scorep.py -c dc19 -s ctfd:100,500,50,2880 data/dcquals_2019.json
```

The last parameter `@time` let you configure how the score of each challenge is updated.
Basically, it sets an upper limit and only the number of solves in that window are counted.
So, if you want to see what happens if you decrease the score of a challenge only based to
the solutions submitted in the first 5 hours (to account for very difficult challenges
open early in the game), you can run:

```
./scorep.py -c dc19 -s  ooo:100,500,0.08,1,300 data/dcquals_2019.json
-------------------------------=[ Config ]=------------------------------------------
Scoring: 100 + ( 500 - 100 ) / (1 + 0.08 * Solved(300) * Log (1 * Solved(300)))
Ranking: score,first
Bonus:   None
Teams:   30        Challs:   24
Reference: dc19 (-w dc19 data/dcquals_2019.json)
-------------------------------------------------------------------------------------

 #  Score  Diff  Team                        Score    Solves 1st   Challenge
--------------------------------------    ------------------------------------------
 1 -  7192   ---  PPP                         500 +373    45   49  Return_to_shellQL
 2 -  7192   ---  HITCON⚔BFKinesiS            500 +260    10  309  chainedrsa
 3 -  6232   1 ▲  Sauercloud                  500 +313    16  408  Hotel-California
 4 -  6192   2 ▲  A*0*E                       500 +299    14  190  ASRybaB
 5 -  5972   ---  Samurai                     500 +357    30  467  RTOoOS
 6 -  5917   1 ▲  SeoulPlusBadAss             500 + 40     2  751  papatrace
 7 -  5849   4 ▼  Shellphish                  500 +229     8  420  election_coin
 8 -  5692   ---  Tea Deliverers              500  ---     1   23  LCARS333
 9 -  5417   ---  CGC                         460 +325    36  117  gloryhost
10 -  5272   ---  hxp                         460 +304    24  193  LCARS000
11 -  5232   1 ▲  KaisHack GoN                460 +206     9   35  LCARS022
12 -  5209   1 ▼  r00timentary                377 +246    40  171  vitor
13 -  5001   ---  TokyoWesterns               343 +206    34  162  ooops
14 -  4961   ---  r3kapig                     315 +133    17   74  tania
15 -  4917   ---  Tasteless                   291 +152    33  156  VeryAndroidoso
16 -  4732   ---  RPISEC                      271 +129    31   26  mamatrace
17 -  4646   2 ▲  binja                       271 +109    22  105  shitorrent
18 -  4646   1 ▼  mhackeroni                  182 + 64    61   78  nodb
19 -  4457   1 ▼  OpenBlue                    149 + 37    88   40  babyheap
20 -  3756   1 ▲  NASA_Rejects                147 + 37   102   45  redacted-puzzle
                                              139 + 25    76   55  babytrace
                                              122 + 14   122   39  know_your_mem
                                              104 +  2   390    4  cant_even_unplug_it
                                              101 +  1  1252    0  welcome_to_the_game
```


### Examples (just tell me how to win!)

Ok ok. You just want to know how to adjust the parameters to maximize the ranking of your team,
and yes - there is an experimental feature (well, everything is
experimental, but this is even more untested) to help you with that.

The option you are looking for is `-t max:<team_number>`
For instance, if you want to bruteforce the OOO algorithm's parameters to maximize the position
of Shellphish, you can do:

```
> ./scorep.py -c dc19 -t max:3 data/dcquals_2019.json
-------------------------------=[ Config ]=------------------------------------------
Scoring: 100 + ( 500 - 100 ) / (1 + 0.08 * Solved(2880) * Log (1 * Solved(2880)))
Ranking: score,first
Bonus:   None
Teams:   30        Challs:   24
Reference: dc19 (-w dc19 data/dcquals_2019.json)
-------------------------------------------------------------------------------------

Looking for parameters that maximize the final ranking of team: Shellphish
Initial ranking: 3
 Param 1 =  -16.00 --> rank 2
 Param 3 =   -0.12 --> rank 1
```

The tool tries to bruteforce each parameter in isolation, and reports the best outcome (if any).
In this case, if in the formula we change the third parameter from 0.08 to -0.12 Shellphish would
have won. But as you can imagine, changing the sign does have a large impact on the results.
The other option is to score each challenge in the range -16-to-500 (instead of 100-500) which
basically penalizes teams that solve very easy challenges :D

### Extending the tool

If you want to add a new algorithm, check `scorings.py`.
The task is actually quite simple: just add a new function and if it starts with `score_` it
will be automatically added to the list of available scoring algorithms (same if you start
with `rank_` or `bonus_`).

If you add support for other major CTF formulas, send me a PR.














