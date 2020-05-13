#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import json
import math
import scorings
import getopt
import inspect
import pickle
from collections import namedtuple

# ----------------------------------------------------------------------------
#                                FUNCTIONS
# ----------------------------------------------------------------------------

def dict_to_sorted_list(d, f):
    result = list(d.values())
    result.sort(key=f, reverse=True)
    return result

class Chall:
    def __init__(self, name, open_time):
        self.name      = name
        self.open_time = open_time
        self.solved_by = []
        self.points    = 0
        
    def add_solution(self, team, time):
        t = int((time - self.open_time)/60); assert t >= 0
        for oldsolve in self.solved_by: assert t >= oldsolve[1]  # solved_by must be ordered
        self.solved_by.append((team, t))
        if isinstance(team, Team):
            team.solve(self, t, len(self.solved_by))
    
    def get_solve_count(self, max_time=0):
        if max_time:
            return len([x for x in self.solved_by if x[1]<max_time])
        return len(self.solved_by)

    def first_blood(self, n=1):
        if len(self.solved_by)<n:
            return None
        return self.solved_by[n-1]
        

class Team:
    def __init__(self, name):
        self.name = name
        self.solved = []
        self.bonus  = 0

    def solve(self, chall, time, fb=False):
        self.solved.append((chall, time, fb))

    def get_final_score(self):
        return self.bonus + sum([x[0].points for x in self.solved])

    def get_score_at(self, time):
        return sum([x[0].points for x in x[1]+x[0].open_time<time])

    def get_cumulative_solve_time(self):
        return sum([x[1] for x in self.solved])

    def last_solved(self):
        try:
            return self.solved[-1][1] + self.solved[-1][0].open_time
        except:
            error("%s <---- %s"%(self.name, self.solved))

    def __str__(self):
        return self.name


def save_reference(filename, cmdline, final_ranking, challenges_info):
    with open(filename, 'wb') as f:
        pickle.dump((cmdline, final_ranking, challenges_info), f, pickle.HIGHEST_PROTOCOL)

def load_reference(filename):
    # try:
        with open(filename,'rb') as f:
            return pickle.load(f)
    # except:
        # error("could not load reference score from %s"%filename)

def load_config():
    config = namedtuple('Config', 'teams challs')(teams=[], challs=[])
    lineno = 1
    try:
        for line in open('teams.conf'):
            line = line.strip()
            if line.startswith('#'):
                continue
            if line.startswith('"'):
                if not line.endswith('"'):
                    error("Line %d in teams.conf not properly quoted"%lineno)
                line = line[1:-1]
            config.teams.append(line)
            lineno +=1
    except:
        error("unable to load teams.conf")
    lineno = 1
    try:
        for line in open('challs.conf'):
            line = line.strip()
            if line.startswith('#'):
                continue
            if line.startswith('"'):
                if not line.endswith('"'):
                    error("Line %d in challs.conf not properly quoted"%lineno)
                line = line[1:-1]
            config.challs.append(line)
            lineno +=1
    except:
        error("unable to load challs.conf")
    return config

def load_json(filename, config):
    challs = {}
    teams  = {}

    with open(filename) as f:
        data   = json.load(f)
    solves = data['message']['solves']
    tmp    = data['message']['open']

    for name, _a, _b, _c, t in tmp:
        if name not in config.challs:
            continue
        challs[name] = Chall(name, t)

    for t in config.teams:
        teams[t] = Team(t)

    for chall, team, tstamp in solves:
        c = challs.get(chall)
        if not c:
            continue
        t = teams.get(team, team)
        c.add_solution(t, tstamp)

    return challs, teams

def display(sb, cb, reference, limit):
    if reference:
        ref_scores = [t.name for t in reference[1]]
        ref_challs = {c.name: c.points for c in reference[2]}
        empty = "                                            "
        print ("\033[32m #  Score  Diff  Team                        Score    Solves 1st   Challenge" )
    else:
        empty = "                                            "
        # print ("\033[32m #  Score  Team                     Score Solves 1st   Challenge" )
        print ("\033[32m #  Score Solv  Time  Team                  Score Solves 1st   Challenge" )

    print ("--------------------------------------    ------------------------------------------\033[0m")

    pos = 0
    for i in range(max(len(cb), min(limit,len(sb)))):
        col1 = empty
        if i < len(sb) and i < limit:
            t = sb[i]
            try:
                quals = ref_scores.index(t.name)
                if pos == quals:
                    delta = '  --- '
                elif pos > quals:
                    delta = u' \033[31m%2d ▼\033[0m '%(pos-quals)
                else:
                    delta = u' \033[32m%2d ▲\033[0m '%(quals-pos)
            except:
                delta = '   ?  '
            if reference:
                col1 = "%2d - \033[35m%5s\033[0m %s %s"%(pos+1, t.get_final_score(), delta, t.name+" "*(26-len(t.name)))
            else:
                # col1 = "%2d - \033[35m%5s\033[0m %s"%(pos+1, t.get_final_score(), t.name+" "*(26-len(t.name)))
                col1 = "%2d - \033[35m%5s\033[0m %d    %d  %s"%(pos+1, t.get_final_score(), len(t.solved), t.get_cumulative_solve_time()/60, t.name+" "*(22-len(t.name)))

        col2 = ""
        if i < len(cb):
            delta = ' ---'
            score = cb[i].points
            name  = cb[i].name
            try:
                diff  = score - ref_challs[name]
                if diff > 0:
                    delta = '\033[32m+%3d\033[0m'%diff
                elif diff < 0:
                    delta = '\033[31m-%3d\033[0m'%abs(diff)
            except:
                delta = ' ?  '

            if reference:
                col2 = "%4d %s  %4d %4d  %s"%(score, delta, cb[i].get_solve_count(), cb[i].first_blood()[1], name)
            else:
                col2 = "%4d %4d %4d  %s"%(score, cb[i].get_solve_count(), cb[i].first_blood()[1], name)

        print ("%s %s"%(col1, col2))
        pos += 1


def usage():
    print ("\033[32mUse:\033[0m \n   python3 %s [options] filename.json"%sys.argv[0])
    print ("")
    print ("\033[32mOptions:\033[0m")
    # print ("  -h [rank|score|bunus]    \033[32m # Provide help on individual options \033[0m ")
    print ("  -r a1,a2,...,an      \033[33m # Select the ordered list of *Ranking* algorithms \033[0m ")
    print ("  -s name:p1,p2..,pn   \033[33m # Select and configure the *Scoring* algorithm  \033[0m ")
    print ("  -b ???               \033[33m # Select and configure the *Bonus* algorithm  \033[0m ")  
    print ("  -w <filename>        \033[33m # Save the result to a file for later comparison\033[0m ")  
    print ("  -c <filename>        \033[33m # Compare ranking against previous result\033[0m ")  
    print ("  -l <n>               \033[33m # Limit the scoreboard to the top <n> places\033[0m ")  
    print ("  -t [max|change|new]:n\033[33m # Automatically test different values for the scoring parameters\033[0m ")  
    print ("\n\033[32mRanking Algorithms:\033[0m")
    print (" Comma-separated list of algorithms. First ranking algorithm is applied first, in case of ties,")
    print (" the second algorithm is used, and so forth.")
    for name, help_str in [(s[5:], scorings.__dict__[s].__doc__) for s in scorings.__dict__ if s.startswith('rank')]:
        print ("  - \033[32m{0:s}\033[0m {1:s}".format(name,help_str))
    print (" Default is: score,first")
    print ("\n\033[32mScoring Algorithms:\033[0m")
    print (" Only one scoring algorithm can be applied at a time.")
    print (" Default is: ooo")
    for name, help_str in [(s[6:], scorings.__dict__[s].__doc__) for s in scorings.__dict__ if s.startswith('score')]:
        print ("  - \033[32m{0:5s}\033[0m {1:s}".format(name,help_str.replace('\n','\n        ')))
    print ("\n\033[32mBonus Algorithms:\033[0m")
    for name, help_str in [(s[6:], scorings.__dict__[s].__doc__) for s in scorings.__dict__ if s.startswith('bonus')]:
        print ("  - \033[32m{0:5s}\033[0m {1:s}".format(name,help_str.replace('\n','\n        ')))

def error(msg):
    print("\033[31m ERROR:\033[0m %s"%msg)
    sys.exit(2)

def get_default_params(f):
    spec = inspect.getfullargspec(f)
    return list(spec.defaults)

# ----------------------------------------------------------------------------
#                                MAIN
# ----------------------------------------------------------------------------


try:
    optlist, args = getopt.getopt(sys.argv[1:], 'hvw:c:r:s:b:l:t:', ['help', 'verbose', 'write=', 'compare=', 'rank=','score=','bonus=', 'limit=', 'test='])
except:
    usage()
    sys.exit(1)

if len(args) != 1:
    usage()
    sys.exit(2)

# Configurations
# ----------------------------------------------------------------------------
rank_dict  = {s[5:]: scorings.__dict__[s] for s in scorings.__dict__ if s.startswith('rank')}
score_dict = {s[6:]: scorings.__dict__[s] for s in scorings.__dict__ if s.startswith('score')}
bonus_dict = {s[6:]: scorings.__dict__[s] for s in scorings.__dict__ if s.startswith('bonus')}

filename = args[0]
verbose  = False
limit = 20
fuzz = False
reference_w = None
reference_r = None
reference   = None
test_condition = None
ranking_algorithms = [rank_dict['score'], rank_dict['first']]
score_gen_f =  score_dict['ooo']
score_params = get_default_params(score_gen_f)
bonus_f = lambda x,*y,**z: 1
bonus_params = []

# Parse options
# ----------------------------------------------------------------------------
for o, a in optlist:
    if o in ("-h", "--help"):
        usage()
        sys.exit(0)
    elif o in ("-t", "--test"):
        if not a:
            error ("Please specify a test condition")
        try:
            cond_type, cond_value = a.split(":")
            if cond_type not in ['change', 'max', 'new']:
                error("Test condition type invalid. Valid values are 'change', 'max', or 'new'")
            test_condition = [cond_type, int(cond_value)]
        except:
            error("Invalid test condition. Must be 'condition_type:condition_value")
    elif o in ("-v", "--verbose"):
        verbose = True
    elif o in ("-l", "--limit"):
        if not a:
            error ("Limit to what?")
        try:
            limit = int(a)
        except:
            error("\"%s\" is not a valid number"%a)
    elif o in ("-c", "--compare"):
        if not a:
            error("-c requires a file name")
        reference_r = a
    elif o in ("-w", "--write"):
        if not a:
            error("-w requires a file name to store the reference model")
        reference_w = a
    elif o in ("-b", "--bonus"):
        if not a:
            error("No bonus algorithm specified")
        if ':' in a:
            name, params = a.split(":")
            bonus_params = params.split(",")
        else:
            name = a
            bonus_params = []

        if name in bonus_dict:
            bonus_f = bonus_dict[name]
        else:
            error("\"%s\" bonus algorithm not found!"%name)
        
    elif o in ("-r", "--rank"):
        if not a:
            error("No ranking algorithm specified")
        ranking_algorithms = []
        for name in a.split(','):
            if name not in rank_dict:
                error("\"%s\" ranking algorithm not found!"%name)
            ranking_algorithms.append(rank_dict[name])
    elif o in ("-s", "--score"):
        if not a:
            error("No scoring algorithm specified")
        if ':' in a:
            name, params = a.split(":")
            params = params.split(",")
        else:
            name = a
            params = []

        if name in score_dict:
            score_gen_f = score_dict[name]
        else:
            error("\"%s\" scoring algorithm not found!"%name)
        
        score_params = get_default_params(score_gen_f)
        if len(params) > len(score_params):
            error("Too many parameters for model \"%s\""%name)
        i = 0
        for i in range(len(params)):
            if params[i]:
                score_params[i] = params[i]

if reference_r:
    reference = load_reference(reference_r)


ranking_f = lambda team: [s(team) for s in ranking_algorithms]

formula = [x[10:] for x in score_gen_f.__doc__.split('\n') if x.strip().startswith("Points:")][0]
spec = inspect.getfullargspec(score_gen_f)

config = load_config()

for i in range(len(spec.args)):
    formula = formula.replace("@%s"%spec.args[i], "%s"%score_params[i])
print ("\033[32m-------------------------------=[ Config ]=------------------------------------------\033[0m")
print ("\033[32mScoring:\033[0m %s"%formula)
print ("\033[32mRanking:\033[0m %s"%",".join([r.__name__[5:] for r in ranking_algorithms]))
if bonus_f.__name__.startswith('<lambda>'):
    print ("\033[32mBonus:\033[0m   None")
else:
    print ("\033[32mBonus:\033[0m   %s:%s"%(bonus_f.__name__[6:], bonus_params))
print ("\033[32mTeams:\033[0m   %d        \033[32mChalls:\033[0m   %d"%(len(config.teams), len(config.challs)))
if reference:
    print ("\033[32mReference:\033[0m %s (%s)"%(reference_r," ".join(reference[0])))
print ("\033[32m-------------------------------------------------------------------------------------\033[0m\n")
   
try:
    challs, teams = load_json(filename, config)
except:
    error("Error reading file \"%s\""%filename)

if reference_w and test_condition:
    error("You can't use both -w and -t")

if test_condition:
    score_f = score_gen_f(*score_params)
    for chall in challs.values():
        score_f(chall)
    for team in teams.values():
        bonus_f(team, *bonus_params, all_teams=teams, all_challs=challs)

    baseline = dict_to_sorted_list(teams, ranking_f)
    baseline = [b.name for b in baseline]
    
    if test_condition[0]=='max':
        test_max   = True
        base_pos   = int(test_condition[1]) - 1
        test_value = baseline[base_pos]
        print ("Looking for parameters that maximize the final ranking of team: %s"%test_value)
        print ("Initial ranking: \033[32m%d\033[0m"%(base_pos+1))
        for i in range(len(score_params)):
            new_params = [float(x) for x in score_params]
            best_pos = base_pos
            best_param = 0
            step = max(0.1, 0.01*new_params[i])
            for j in range(1000):
                new_params[i]-=step
                score_f = score_gen_f(*new_params)
                for chall in challs.values():
                    try:
                        score_f(chall)
                    except:
                        continue
                for team in teams.values():
                    team.bonus = 0
                    bonus_f(team, *bonus_params, all_teams=teams, all_challs=challs)
                
                res = dict_to_sorted_list(teams, ranking_f)
                res = [r.name for r in res]
                if res.index(test_value) < best_pos:
                    best_pos = res.index(test_value)
                    best_param = new_params[i]
                    if best_pos == 0:
                        break
            if best_pos !=  base_pos:
                print (" Param {0:d} = \033[32m{1:7.2f}\033[0m --> rank {2:d}".format(i+1, best_param, best_pos+1))
            
            new_params = [float(x) for x in score_params]
            best_pos = base_pos
            best_param = 0
            for j in range(1000):
                new_params[i]+=step
                score_f = score_gen_f(*new_params)
                for chall in challs.values():
                    try:
                        score_f(chall)
                    except:
                        continue
                for team in teams.values():
                    team.bonus = 0
                    bonus_f(team, *bonus_params, all_teams=teams, all_challs=challs)
                res = dict_to_sorted_list(teams, ranking_f)
                res = [r.name for r in res]
                if res.index(test_value) < best_pos:
                    best_pos = res.index(test_value)
                    best_param = new_params[i]
                    if best_pos == 0:
                        break
            if best_pos !=  base_pos:
                print (" Param {0:d} = \033[32m{1:7.2f}\033[0m --> rank {2:d}".format(i+1, best_param, best_pos+1))
    else:    
        test_value = test_condition[1]
        print ("Testing effects of parameter variations on the top %d positions"%test_value)
        for i in range(len(score_params)):
            new_params = [float(x) for x in score_params]
            abs_step = max(0.1, 0.01*new_params[i])
            min_change = False
            print (" Param {0} (step +-{1:4.1f}): ".format(i+1, abs_step), end="")
            eol = False
            for step in [-1*abs_step, abs_step]:
                for j in range(500):
                    new_params[i]-=step
                    score_f = score_gen_f(*new_params)
                    for chall in challs.values():
                        try:
                            score_f(chall)
                        except:
                            print ("Warning")
                            continue
                    for team in teams.values():
                        team.bonus = 0
                        bonus_f(team, *bonus_params, all_teams=teams, all_challs=challs)
                    res = dict_to_sorted_list(teams, ranking_f)
                    res = [r.name for r in res]
                    if (test_condition[0]=='new' and set(res[:test_value]) != set(baseline[:test_value])) or (test_condition[0]=="change" and res[:test_value] != baseline[:test_value]):
                        if step < 0:
                            print ("{1:8.2f} <-- {0:8.2f}".format(float(score_params[i]), new_params[i]), end="")
                            min_change = True
                            break
                        else:
                            if min_change:
                                print ("  --> {0:8.2f}".format(new_params[i]))
                            else:
                                print ("{0:8.2f} --> {1:8.2f}".format(float(score_params[i]), new_params[i]))
                            eol = True
                            break
            if not eol:
                print ("")

else:
    score_f = score_gen_f(*score_params)

    for chall in challs.values():
        score_f(chall)
    for team in teams.values():
        team.bonus = 0
        bonus_f(team, *bonus_params, all_teams=teams, all_challs=challs)

    cboard = dict_to_sorted_list(challs, lambda chall: chall.points)
    sboard = dict_to_sorted_list(teams, ranking_f)

    if reference_w:
        save_reference(reference_w, sys.argv[1:], sboard, cboard)
        print("Results saved to %s"%reference_w)
        print("You can now compare with those results by using \033[32m-c %s\033[0m"%reference_w)
    else:
        display(sboard, cboard, reference, limit)


