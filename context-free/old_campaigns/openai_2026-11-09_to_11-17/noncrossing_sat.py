"""CEGIS search for a primitive word without noncrossing witnesses.

Each learned clause rules out exactly a valid noncrossing edge certificate.
UNSAT is a finite-length result only. No global claim follows.
"""
import sys
import time
import z3
from noncrossing_witnesses import primes,witness

def run(n,timeout=60):
    bits=[z3.Bool('b'+str(i)) for i in range(n)]
    solver=z3.Solver()
    solver.set(timeout=10000)
    solver.add(z3.Not(bits[0]))
    for p in primes(n):
        d=n//p
        solver.add(z3.Or([bits[i]!=bits[i+d] for i in range(n-d)]))
    start=time.monotonic()
    rounds=0
    while time.monotonic()-start<timeout:
        result=solver.check()
        if result!=z3.sat:
            print(n,result,'rounds',rounds,flush=True)
            return
        model=solver.model()
        w=[z3.is_true(model.eval(b,model_completion=True)) for b in bits]
        edges=witness(w)
        if edges is None:
            print(n,'COUNTEREXAMPLE',''.join('1' if b else '0' for b in w),flush=True)
            return
        solver.add(z3.Or([bits[i]==bits[j] for p,(i,j) in edges]))
        rounds+=1
    print(n,'TIMEOUT','rounds',rounds,flush=True)

if __name__=='__main__':
    for n in map(int,sys.argv[1:] or [6,30,42,60,210]):
        run(n)
