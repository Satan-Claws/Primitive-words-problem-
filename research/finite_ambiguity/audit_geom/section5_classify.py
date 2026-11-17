# Test of the case analysis of section 5 for M=2 on random laminar simple linear sets L = c + N v_1 + ... + N v_r.
# For each set: classify (case 1/2/3/4) exactly as the proof does, then compare the proof's prediction with direct
# membership of the points P(t,delta) = (t w, t w + Lm*delta), |delta|_inf <= R, t a large multiple of Lm.
# Prediction (valid when L avoids the diagonal): cases 1,2,3 -> no points; case 4 -> pattern is either empty or
# exactly {delta : psi(delta) > 0}.  On a mismatch we search for an explicit diagonal point of L.
import random, itertools, sys
from fractions import Fraction as Fr
from math import lcm
from common import crossing, rank
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
M = 2; n = 4; R = 3
Lm = int(sys.argv[2]) if len(sys.argv) > 2 else lcm(*range(1, 41))
omega = (7, 11)
W = [[1, 0, 1, 0], [0, 1, 0, 1]]

def rand_laminar(r):
    for _ in range(1000):
        V = []; sup = []
        while len(V) < r:
            if random.random() < 0.35: s = (random.randrange(n),)
            else: s = tuple(sorted(random.sample(range(n), 2)))
            if any(crossing(s, t) for t in sup): continue
            v = [0]*n
            for i in s: v[i] = random.randint(1, 3)
            if rank(V + [v]) == len(V) + 1: V.append(v); sup.append(s)
            elif random.random() < 0.05: break
        if len(V) == r: return V
    return None

def coords(V, P):
    """Return coordinate vector a with sum a_j V_j = P, or None if P not in span V."""
    k = len(V)
    A = [[Fr(V[j][i]) for j in range(k)] + [Fr(P[i])] for i in range(n)]
    row = 0; piv = []
    for col in range(k):
        p = next((i for i in range(row, n) if A[i][col] != 0), None)
        if p is None: continue
        A[row], A[p] = A[p], A[row]; q = A[row][col]; A[row] = [x/q for x in A[row]]
        for i in range(n):
            if i != row and A[i][col] != 0:
                f = A[i][col]; A[i] = [x - f*y for x, y in zip(A[i], A[row])]
        piv.append(col); row += 1
    if any(A[i][k] != 0 for i in range(row, n)): return None
    a = [Fr(0)]*k
    for i, col in enumerate(piv): a[col] = A[i][k]
    return a

def member(c, V, P):
    a = coords(V, [p - q for p, q in zip(P, c)])
    return a is not None and all(x.denominator == 1 and x >= 0 for x in a)

def classify(V):
    r = len(V)
    Wspan = rank(V + W) == r
    oo = [omega[0], omega[1], omega[0], omega[1]]
    a = coords(V, oo)
    in_C = a is not None and all(x >= 0 for x in a)
    if not Wspan:
        return ('1', None) if not in_C else ('nongeneric', None)
    # functionals l_v(u) = n_v(u,u)
    l1 = coords(V, [1, 0, 1, 0]); l2 = coords(V, [0, 1, 0, 1])
    lv = [(l1[j], l2[j]) for j in range(r)]
    vals = [l[0]*omega[0] + l[1]*omega[1] for l in lv]
    if any(v == 0 and l != (0, 0) for v, l in zip(vals, lv)): return ('nongeneric', None)
    if any(v < 0 for v in vals): return ('1', None)
    V1 = [j for j in range(r) if lv[j] == (0, 0)]
    if r == 3:
        if V1: return ('dim3_with_V1(Lemma X fails: non-laminar)', (coords(V,[0,0,1,0]), coords(V,[0,0,0,1]), V1))
        return ('2', None)
    if r < 3: return ('LEMMA_X_VIOLATION', None)
    if not V1: return ('3', None)
    if len(V1) > 1: return ('POSITIVITY_FACT_VIOLATION', None)
    j = V1[0]
    e3 = coords(V, [0, 0, 1, 0]); e4 = coords(V, [0, 0, 0, 1])
    return ('4', (e3[j], e4[j]))

deltas = [d for d in itertools.product(range(-R, R+1), repeat=2) if d != (0, 0)]
def main():
  stats = {}; mism = 0; checked = 0
  for trial in range(4000):
      r = random.choice([1, 2, 3, 4, 4, 4])
      V = rand_laminar(r)
      if V is None: continue
      c = [random.randint(0, 4) for _ in range(n)]
      cls, psi = classify(V)
      if cls in ('nongeneric',): continue
      T = 10**6
      t = Lm * T
      pat = {d for d in deltas if member(c, V, [t*omega[0], t*omega[1], t*omega[0] + Lm*d[0], t*omega[1] + Lm*d[1]])}
      if cls in ('1', '2', '3'): ok = not pat
      elif cls == '4':
          half = {d for d in deltas if psi[0]*d[0] + psi[1]*d[1] > 0}
          ok = (not pat) or pat == half
      else: ok = False
      key = cls + ('' if cls != '4' else ('-empty' if not pat else '-halfplane'))
      if ok: stats[key] = stats.get(key, 0) + 1; checked += 1; continue
      # mismatch: look for a diagonal point of L (then the hypothesis L cap Delta = empty fails, no contradiction)
      found = None
      for a in itertools.product(range(0, 25), repeat=r):
          P = [c[i] + sum(a[j]*V[j][i] for j in range(r)) for i in range(n)]
          if P[0] == P[2] and P[1] == P[3]: found = P; break
      if found: stats[key + '-meetsDiag'] = stats.get(key + '-meetsDiag', 0) + 1
      else:
          mism += 1; print('MISMATCH (no diagonal point found)', cls, V, c, psi, sorted(pat))
  print('Lm =', Lm if Lm < 10**6 else 'lcm(1..40)', 'omega =', omega, 'R =', R)
  print('consistent sets by case:', dict(sorted(stats.items())))
  print('unexplained mismatches:', mism)

if __name__ == '__main__': main()
