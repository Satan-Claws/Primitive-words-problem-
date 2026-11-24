"""Task G (walk.md): ambiguity of explicit grammars for T^k(E'), k=1,2,3, two variants:
  lit : E' grammar exactly as printed in walk.md §1 (S -> KXK|KYK, K -> eps|XKYK|YKXK)
  fix : same language, K replaced by the unambiguous first-return grammar (EFIX in testgram_cfg.py)
G_k = T^k(E') built literally: sigma-substitution -> CNF -> cyclic closure (PA/poly_S4C) -> union with swap.
Part A: literal CYK on the built CNF grammars, all words |w| <= NA, cross-checked against the reduction formula
  amb_{T1}(w) = sum_{t<D} amb_{E'}(rot_t Phi(w)),  amb_{T_k}(w) = D * amb_{T_{k-1}}(Phi(w))   (k >= 2),
  (Phi = first-passage type word after swapping to Delta>0; D = |Delta(w)|; testgram.md §1.3).
Part B: A_G(N) = max over |w| <= N via the formula, enumerating type words v with #a(v)+3#b(v) <= N
  (the shortest w with Phi(w)=v is v[a->a, b->baa], of that length)."""
import sys, itertools, time
from functools import lru_cache
from testgram_cfg import EPRIME, EFIX, T, cyk, size

def phi(w):
    v = [1 if c == 'a' else -1 for c in w]; n = len(v); D = sum(v)
    if D == 0: return None
    if D < 0: v = [-x for x in v]
    s = best = arg = 0
    for t in range(n):
        if s > best: best, arg = s, t
        s += v[t]
    u = v[arg:] + v[:arg]
    out = []; s = rec = 0; start = 0
    for t, x in enumerate(u):
        s += x
        if s > rec:
            rec = s; out.append('a' if t == start else 'b'); start = t + 1
    return ''.join(out)

@lru_cache(maxsize=None)
def Klit(u):
    """# trees of K -> eps | aKbK | bKaK on u."""
    if u == '': return 1
    tot = 0; first = u[0]; h = 0
    for i, c in enumerate(u):
        h += 1 if c == 'a' else -1
        if i > 0 and c != first:
            inner = u[1:i]
            if inner.count('a') == inner.count('b'):
                tot += Klit(inner) * Klit(u[i + 1:])
    return tot if u.count('a') == u.count('b') else 0

def amb0(v, var):
    D = v.count('a') - v.count('b')
    if abs(D) != 1: return 0
    maj = 'a' if D == 1 else 'b'
    if var == 'fix':
        h = 0; cnt = 0
        for c in v:
            if h == 0 and c == maj: cnt += 1
            h += 1 if c == 'a' else -1
        return cnt
    return sum(Klit(v[:i]) * Klit(v[i + 1:]) for i in range(len(v)) if v[i] == maj)

@lru_cache(maxsize=None)
def amb(w, k, var):
    if k == 0: return amb0(w, var)
    f = phi(w)
    if f is None: return 0
    return m(f, k, var)

def m(v, k, var):
    """amb_{T_k}(w) for any w with Phi(w) = v."""
    if k == 1: return sum(amb0(v[t:] + v[:t], var) for t in range(len(v)))
    return len(v) * amb(v, k - 1, var)

def primitive(w):
    n = len(w); return all(w[d:] + w[:d] != w for d in range(1, n) if n % d == 0)

def type_words(N):
    """all v over {a,b} with #a + 3#b <= N, v nonempty."""
    out = []
    def rec(v, L):
        if v: out.append(v)
        if L + 1 <= N: rec(v + 'a', L + 1)
        if L + 3 <= N: rec(v + 'b', L + 3)
    rec('', 0); return out

if __name__ == '__main__':
    NA = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    NB = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    for var, E in (('lit', EPRIME), ('fix', EFIX)):
        g = E; G = {}
        for k in (1, 2, 3):
            g = T(g, f'L{k}'); G[k] = g
        print(f"[{var}] CNF sizes (nonterminals, rules):", {k: size(G[k]) for k in G})
        for k in (1, 2, 3):
            na = NA - 2 * (k - 1); t0 = time.time(); first_miss = None; mism = bad = 0; A = 0; row = []
            for n in range(1, na + 1):
                for x in itertools.product('ab', repeat=n):
                    w = ''.join(x); c = cyk(G[k], w); f = amb(w, k, var)
                    if c != f: mism += 1
                    if c and not primitive(w): bad += 1
                    if not c and primitive(w) and first_miss is None: first_miss = w
                    A = max(A, c)
                row.append(A)
            print(f"[{var}] k={k} literal CYK all |w|<={na}: formula mismatches={mism}, non-primitive accepted={bad}, "
                  f"first primitive word missed={first_miss}; A(1..{na})={row} ({time.time()-t0:.0f}s)", flush=True)
    for var in ('lit', 'fix'):
        for k in (1, 2, 3):
            best = {}
            for v in type_words(NB):
                L = v.count('a') + 3 * v.count('b')
                val = m(v, k, var)
                if val and (L not in best or val > best[L][0]): best[L] = (val, v)
            A = 0; arg = None; row = []
            for n in range(1, NB + 1):
                if n in best and best[n][0] > A: A, arg = best[n][0], best[n][1].replace('b', 'B').replace('B', 'baa')
                row.append((n, A, arg))
            print(f"[{var}] k={k} A_G(n), n=1..{NB}:")
            for n, A, arg in row: print(f"   {n:3d} {A} {arg} ratio={(A/row[n-2][1]) if n>1 and row[n-2][1] else 0:.3f}")
            sys.stdout.flush()
