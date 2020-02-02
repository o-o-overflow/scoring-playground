import math

# ----------------------------------------------------------------------------
#                             SCORING  FUNCTIONS
# ----------------------------------------------------------------------------

def score_ooo(base=100, top=500, k=0.08, j=1, time=2880):
    '''Log-based Decay formula used for the Defcon Quals in 2018 and 2019
  Format: ooo:base,top,k,j,time
  Points: @base + ( @top - @base ) / (1 + @k * Solved(@time) * Log (@j * Solved(@time)))
  Default value: ooo:100,500,0.08,1,2880'''
    def f(chall):
        n = chall.get_solve_count(int(time))
        if n==0:
            chall.points = int(top)
        else:
            chall.points = int(int(base) + float(int(top)-int(base))/(1 + float(k)*n * math.log(float(j)*n)))
    return f

def score_ctfd(base=100, top=500, decay=20, time=2880):
    '''Parabolic function available in ctfd.
  Format: ctfd:base,top,decay,time
  Points: max(base, (((base - top)/(decay**2)) * (Solved(@time)**2)) + top)
  Default value: ctfd:100,500,20,2880'''
    def f(chall):
        n = chall.get_solve_count(int(time))
        chall.points = max(int(base), int(math.ceil(  (((int(base)- int(top))/(int(decay)**2)) * (n**2)) + int(top) )))
    return f

def score_ccc(base=30, top=500, k=11.92201, j=1.206069, time=2880):
    '''Exponential decay formula used by the CCC CTF.
  Format: ccc:base,top,k,j,time
  Points: @base + ( @top - @base ) / (1 + (max(0, Solved(@time)-1)/ @k) ** @j)
  Default value: ooo:30,500,11.92291,1.206069,2880'''
    def f(chall):
        n = chall.get_solve_count(int(time))
        chall.points = int(round(int(base) + float(int(top)-int(base)) / (1 + (max(0, n - 1) / float(k)) ** float(j))))
    return f

def score_time(base=30, top=500, i=0.75, n=1):
    '''Incremental model in which the number of points increase with time
  Format: time:base,top,i,n
  Points: @base + 1 point every @i minutes until @top or until @n-th team solve it
  Default value: time:20,500,0.75,1'''
    def f(chall):
        min_time = chall.first_blood(int(n))
        if min_time:
            chall.points = int(round(min(int(top), int(base)+float(min_time[1])/float(i))))
        else:
            chall.points = int(top)
    return f

def score_five(v1=10, v2=15, v3=20, v4=40, t=2880):
    '''Classic five levels (500,400,300,200,100) challenges. 
  Format: five:v1,v2,v3,v4,t
  Points: 500 if Solved(@t) < @v1; 400 if Solved(@t) < @v2; 300 if Solved(@t) < @v3; 200 if Solved(@t) < @v4; 100 otherwise
  Default: five:10,15,20,40,0'''
    def f(chall):
        n = chall.get_solve_count(int(t))
        if   n < int(v1): chall.points=500
        elif n < int(v2): chall.points=400
        elif n < int(v3): chall.points=300
        elif n < int(v4): chall.points=200
        else:
            chall.points = 100
    return f

# ----------------------------------------------------------------------------
#                              TIE BREAKERS
# ----------------------------------------------------------------------------

def rank_score(team):
    '''rank teams based on their final score''' 
    return team.get_final_score()

def rank_solved(team):
    '''rank teams based on how many challenges they solved''' 
    return len(team.solved)

def rank_first(team):
    '''rank teams based on who reached its final score first''' 
    return 1./team.last_solved()

def rank_fb(team):
    '''rank teams based on number of first blood''' 
    return len([s for s in team.solved if s[2]==1])

def rank_ctime(team):
    '''rank teams based on the cumulative time they spent solving challenges''' 
    return 1./team.get_cumulative_solve_time()

# ----------------------------------------------------------------------------
#                                 BONUS
# ----------------------------------------------------------------------------

def bonus_firstblood(team, *params, **kwargs):
    '''Add a bonus to the first n teams who solved a challenge
       Format: firstblood:x1,x2,..,xn
       Where x can be an absolute value (e.g., 30) or a percentage of the challenge points (e.g., 2.5%)'''
    for chall, time, order in team.solved:
        if order <= len(params):
            if params[order-1].endswith('%'):
                team.bonus += int(round(float(params[order-1][:-1])*0.01*chall.points))
            else:
                team.bonus += int(params[order-1])


