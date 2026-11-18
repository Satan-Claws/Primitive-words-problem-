# Theorem 2 check: class-restricted near-palindrome certificate with marker classes.
# Vector x in N^{l k}; class r = positions j (0-indexed) with j % l == r. Defect class 0.
# Condition: y_i = x[l*i]; y_0 - y_{k-1} = 1; y_i = y_{k-1-i} (1<=i<=k-2); x[j] = 1 for j%l in M.
# Claim: if for every prime r | l the coset 0 + (l/r)Z_l meets M, then x is not shift-invariant.
import itertools, sys
def periodic(x):
    K = len(x)
    return any(all(x[j] == x[(j+d) % K] for j in range(K)) for d in range(1, K))
def primes(n): return [p for p in range(2, n+1) if n % p == 0 and all(p % q for q in range(2, p))]
def check(l, M, k, V):
    K = l*k; free = [j for j in range(K) if j % l not in M]
    bad = 0; tot = 0
    for vals in itertools.product(range(V), repeat=len(free)):
        x = [1]*K
        for j, v in zip(free, vals): x[j] = v
        y = [x[l*i] for i in range(k)]
        if y[0] - y[k-1] != 1: continue
        if any(y[i] != y[k-1-i] for i in range(1, k-1)): continue
        tot += 1
        if periodic(x):
            bad += 1
            if bad == 1: ex = x
    return tot, bad, (ex if bad else None)
for l, M in [(2, set()), (2, {1}), (3, set()), (3, {2}), (3, {1}), (4, {2}), (4, {1}), (4, {3}), (6, {3, 2}), (6, {1})]:
    good = all(any((m - 0) % (l//r) == 0 for m in M) for r in primes(l))
    for k in range(2, 6):
        free = sum(1 for j in range(l*k) if j % l not in M)
        V = 3 if free <= 11 else 2
        if V**free > 3*10**5: continue
        tot, bad, ex = check(l, M, k, V)
        print(f"l={l} M={sorted(M)} hyp={good} k={k} V={V} tested={tot} periodic={bad} ex={ex}")
