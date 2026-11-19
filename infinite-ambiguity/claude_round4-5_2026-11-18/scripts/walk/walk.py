# Agent "walk": iterated first-passage certificates T^k(E').
# Words are tuples of +1 (a) / -1 (b).
import sys, itertools, random

def phi(v):
    """Cyclic first-passage map. Returns (Phi, pieces) or None if D==0.
    If D<0 the word is mirrored (a<->b) first.  Phi letter +1 <-> piece 'a',
    -1 <-> piece z a with z nonempty."""
    n = len(v); D = sum(v)
    if D == 0: return None
    if D < 0: v = tuple(-x for x in v)
    # canonical rotation: start at first argmax of S over [0,n)
    s = 0; best = 0; arg = 0
    for t in range(n):
        if s > best: best, arg = s, t
        s += v[t]
    u = v[arg:] + v[:arg]
    out = []; pieces = []
    s = 0; rec = 0; start = 0
    for t, x in enumerate(u):
        s += x
        if s > rec:
            rec = s
            pieces.append(u[start:t+1])
            out.append(1 if t == start else -1)
            start = t + 1
    assert start == n and rec == abs(D)
    return tuple(out), pieces

def certE(v):            # E' : Delta = +-1
    return abs(sum(v)) == 1

def T(cert):
    def c(v):
        r = phi(v)
        return r is not None and cert(r[0])
    return c

def certG(v):            # weighted count g(a)=1, g(ba..)=-2, g(bb..)=0, F=+-1
    r = phi(v)
    if r is None: return False
    F = 0
    for p in r[1]:
        if len(p) == 1: F += 1
        elif p[1] == 1: F -= 2
    return abs(F) == 1

def primitive(v):
    n = len(v)
    for d in range(1, n):
        if n % d == 0 and v[d:] + v[:d] == v: return False
    return True

CERTS = {'E1': certE, 'T1=T(E1)': T(certE), 'T2': T(T(certE)), 'T3': T(T(T(certE))), 'G': certG}

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 18
    for n in range(1, N + 1):
        cnt = {k: 0 for k in CERTS}; bad = {k: 0 for k in CERTS}
        for v in itertools.product((1, -1), repeat=n):
            pr = None
            for k, c in CERTS.items():
                if c(v):
                    cnt[k] += 1
                    if pr is None: pr = primitive(v)
                    if not pr: bad[k] += 1
        print(n, ' '.join(f"{k}:{cnt[k]/2**n:.4f}/bad{bad[k]}" for k in CERTS), flush=True)
