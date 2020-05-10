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

The final scoreboard is defined by three algorithms: the
**ranking** algorithm (which decides how to sort the teams and break
ties), the **scoring** algorithm (which assigns a score to each
challenge), and an optional **bonus** algorithm (which assign extra
points to certain teams).

For instance, if you want to see what would have changed with the scoring
algorithm used by the CCC, just run:
`./scorep.py -c dc19 -s ccc  data_2019.json`



