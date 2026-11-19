"""Cross-check full_escape against brute-force enumeration of sigma in M up to length 14."""
import random
from common import *
random.seed(1)
agree = disagree = und = 0
for trial in range(3000):
    r = ''.join(random.choice('ab') for _ in range(random.randint(2, 9)))
    loops = [''.join(random.choice('ab') for _ in range(random.randint(1, 3))) for _ in range(3)]
    fe = full_escape(r, loops)
    # brute force
    found = False; frontier = {''}
    for _ in range(14):
        nf = set()
        for s in frontier:
            if not primitive(s + r): found = True
            for v in loops:
                if len(s + v) <= 14: nf.add(s + v)
        frontier = nf
        if found: break
    if fe is None: und += 1
    elif fe == (not found): agree += 1
    else:
        # full_escape False but brute none: possibly needs longer sigma; True but brute found: BUG
        disagree += 1
        if fe: print('BUG', r, loops)
print('agree', agree, 'disagree', disagree, 'undecided(r in Fact M)', und)
