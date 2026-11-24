"""r17_oh_search_margin.py -- required-pad statistic for the deep survivors.

For a word x, b^j x a^j is in G- iff M(x) := max_{1<=k<=|x|/2} d_k(x) < j   (d'_k = d_{k-j}(x) - j, exact identity).
So a family S -> b^j X a^j can only be a counterexample if sup_x M(x) < infinity.  We compute
  - exact max_{x in X_n} M(x) for n <= NEX (enumeration),
  - M on exactly-uniform random words of X_n (sampling by exact parse counts; X unambiguous on the checked range)
    for n up to 600, and report the largest M found plus an explicit witness.
Also for asymmetric pads (b^i, a^j), i,j <= 8, check witnesses directly."""
import sys, random, pickle
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from r17_oh_search_engine import parses, words, in_Gminus

def M(x):
    n = len(x); d = 0; best = -10**9
    for k in range(1, n // 2 + 1):
        d += (x[k - 1] == 'a') - (x[n - k] == 'a')
        best = max(best, d)
    return best

def build_sampler(G, N):
    P = parses(G, N)
    # suffix products: for rule r with NT list nts, S[j][m] = #ways nts[j:] produce total length m
    R = {}
    for X, rules in G.items():
        lst = []
        for r in rules:
            nts = [s for s in r if s not in ('a', 'b')]
            t = len(r) - len(nts)
            S = [None] * (len(nts) + 1)
            S[len(nts)] = [1] + [0] * N
            for j in range(len(nts) - 1, -1, -1):
                A = P[nts[j]]; B = S[j + 1]
                S[j] = [sum(A[l] * B[m - l] for l in range(m + 1)) for m in range(N + 1)]
            lst.append((r, nts, t, S))
        R[X] = lst
    def sample(X, n, rng):
        opts = [(S[0][n - t] if n - t >= 0 else 0, r, nts, t, S) for (r, nts, t, S) in R[X]]
        tot = sum(o[0] for o in opts)
        u = rng.randrange(tot)
        for (c, r, nts, t, S) in opts:
            if u < c:
                break
            u -= c
        m = n - t; lens = []
        for j, s in enumerate(nts):
            tot = S[j][m]; u = rng.randrange(tot)
            for l in range(m + 1):
                c = P[s][l] * S[j + 1][m - l]
                if u < c:
                    break
                u -= c
            lens.append(l); m -= l
        out = []; it = iter(lens); k = 0
        for s in r:
            if s in ('a', 'b'):
                out.append(s)
            else:
                out.append(sample(s, lens[k], rng)); k += 1
        return ''.join(out)
    return P, sample

if __name__ == '__main__':
    sys.setrecursionlimit(100000)
    src = sys.argv[1]
    NMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    surv = pickle.load(open(src, 'rb'))
    rng = random.Random(17)
    for o in surv:
        G = o[6]
        print('=== X:', G['X'], ' Y:', G['Y'])
        P, sample = build_sampler(G, NMAX)
        W = words(G, 21)
        ex = [max([M(x) for x in W['X'][n]], default=None) for n in range(22)]
        print('   exact max_{x in X_n} M(x), n=0..21:', ex)
        for n in sorted(set(m for m in (40, 80, 160, 320) if m < NMAX) | {NMAX}):
            if P['X'][n] == 0:
                n -= 1
            Ms = [];
            for _ in range(300):
                x = sample('X', n, rng); Ms.append((M(x), x))
            Ms.sort(key=lambda z: z[0])
            med = Ms[len(Ms) // 2][0]; top = Ms[-1]
            print(f'   n={n}: uniform sample of 300: median M = {med}, max M = {top[0]}, frac(M>=4) = {sum(m>=4 for m,_ in Ms)/300:.2f}')
            if n == NMAX:
                wit = top[1]
        j = M(wit) + 0
        for (i, jj) in [(j, j), (j + 2, j - 2 if j >= 2 else 0), (max(j - 2, 0), j + 2)]:
            print(f'   witness |x|={len(wit)}, M={M(wit)}: b^{i} x a^{jj} in G-? {in_Gminus("b"*i + wit + "a"*jj)}')
        print('   witness x =', wit[:120] + ('...' if len(wit) > 120 else ''))
