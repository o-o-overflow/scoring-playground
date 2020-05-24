#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys
import json
import os.path

if len(sys.argv) < 2:
    print ("Use: %s <datafile.json>"%sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]
if filename.endswith(".json"):
    basename = filename[:-5]
else:
    basename = filename

if os.path.exists(basename+".teams"):
    print ("File %s.teams already exist"%basename)
    sys.exit(2)
if os.path.exists(basename+".challs"):
    print ("File %s.challs already exist"%basename)
    sys.exit(2)

with open(filename) as f:
    data   = json.load(f)
solves = data['message']['solves']
tmp    = data['message']['open']

challs_names = [t[0] for t in tmp]
teams_names  = set([s[1] for s in solves])
teams_names  = sorted(list(teams_names))

f = open(basename+".teams","w")
for tname in teams_names:
    f.write('# "%s"\n'%tname)
f.close()

f = open(basename+".challs","w")
for cname in challs_names:
    f.write('"%s"\n'%cname)
f.close()

print ("Configuration file created successfully") 
print ("  %d teams"%len(teams_names)) 
print ("  %d challenges"%len(challs_names)) 
print ("\n  (now edit the %s.teams file to uncomment the ones you want to work with)"%basename)


