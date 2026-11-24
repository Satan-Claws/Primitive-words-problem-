"""r15_onesided_models.py -- exact n<=NMAX test of one-sided candidate pair models (r15_onesided.md §5).
Model: tokens (u,v) iid, W = p u1..ur w vr..v1 q.  G-: P(k) < P(n)-P(n-k) for 1<=k<=n/2 (a=+1/2, b=-1/2).
For each candidate token family and every (p,w,q) with |p|,|w|,|q| <= 2, report the first length at which some
word leaves G- (or a collision of the sequence->word map).  Thm PR1s predicts no (p,w,q) survives (if injective)."""
import itertools, sys
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 22
def inG(W):
    n = len(W); P = [0]
    for c in W: P.append(P[-1] + (1 if c == 'a' else -1))
    return all(P[k] < P[n]-P[n-k] for k in range(1, n//2 + 1))
def fam(name):
    L = NMAX
    if name == "a*b|{a,b}":   # U-level block a* (prefix profile >= 0), V side single letters; sum pi = 1
        return [("a"*i+"b", v) for i in range(L) for v in "ab"]
    if name == "a*|{b,ab}":   # U block a^i (i>=0), V in {b, ab}: weights sum_i 2^-i*(1/2+1/4)... use i>=1: 2^-i*(3/4)*... 
        return [("a"*i, v) for i in range(1, L) for v in ("b", "ab", "ba")]  # sum = 1*(1/2+1/4+1/4)=1
    if name == "D-|{a,b}":    # U block = flat words (ab)^i i>=1 (U-level, not V-steep); V letters; sum=1/3*... supercritical ok for test
        return [("ab"*i, v) for i in range(1, L) for v in ("a", "b", "")]
def seqs(tokens, budget):
    out = [((), "", "")]
    stack = [((), "", "")]
    while stack:
        s, U, V = stack.pop()
        for t in tokens:
            nu, nv = U + t[0], t[1] + V
            if len(nu) + len(nv) <= budget and len(t[0]) + len(t[1]) > 0:
                x = (s + (t,), nu, nv); out.append(x); stack.append(x)
    return out
words = ["".join(w) for l in range(3) for w in itertools.product("ab", repeat=l)]
for name in ("a*b|{a,b}", "a*|{b,ab}", "D-|{a,b}"):
    toks = fam(name); S = seqs(toks, NMAX)
    best = (0, None)
    for p in words:
        for w in words:
            for q in words:
                fixed = len(p)+len(w)+len(q); seen = {}; fail = None
                for s, U, V in sorted(S, key=lambda x: len(x[1])+len(x[2])):
                    W = p+U+w+V+q
                    if len(W) > NMAX: continue
                    if W in seen and seen[W] != s: fail = (len(W), "collision", W); break
                    seen[W] = s
                    if not inG(W): fail = (len(W), "not in G-", W); break
                f = fail[0] if fail else NMAX + 1
                if f > best[0]: best = (f, (p, w, q, fail))
    print(f"{name:12s} tokens={len(toks)} seqs={len(S)} best (p,w,q) survives to length {best[0]-1}: {best[1]}", flush=True)
