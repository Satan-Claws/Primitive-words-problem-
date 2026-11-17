"""Experiments: Parikh images of rational transductions of Q (primitive words over {a,b}).

A transducer is a list of edges (p, inword, outletter, q) with inword in {a,b}^{<=2}
and outletter in an output alphabet (every edge outputs exactly one letter, so input
length <= 2 * output length and the computation below is EXACT for outputs of
length <= OUTMAX).  For every output Parikh vector v with |v| <= OUTMAX we decide
  in_image(v)  : some input x (any) has an accepting run with output Parikh v
  in_Qimage(v) : some PRIMITIVE input x has such a run.
N = in_image \\ in_Qimage are the "forced non-primitive" vectors.  Theorem B of
reports/closure.md says N is always semilinear; here we print N for random and for
hand-made adversarial transducers.
"""
import itertools, random, sys
from functools import lru_cache

def primitive(w):
    return len(w) > 0 and (w + w).find(w, 1) == len(w)

def image_sets(edges, start, finals, outalpha, OUTMAX):
    # DP over (state, consumed input prefix as string) is exponential; instead enumerate
    # input words x of length <= 2*OUTMAX and compute set of (output Parikh) reachable.
    # For efficiency: forward DP on positions of x.
    k = len(outalpha)
    idx = {c: i for i, c in enumerate(outalpha)}
    res_any = set(); res_q = set()
    byp = {}
    for (p, iw, o, q) in edges:
        byp.setdefault(p, []).append((iw, idx[o], q))
    maxin = 2 * OUTMAX
    for L in range(0, maxin + 1):
        for t in itertools.product('ab', repeat=L):
            x = ''.join(t)
            # configurations: (pos, state) -> set of parikh tuples
            confs = {(0, start): {tuple([0] * k)}}
            # process in order of pos then BFS for epsilon-input edges
            frontier = [(0, start)]
            outs = set()
            seen = {}
            stack = [(0, start, tuple([0] * k))]
            visited = set()
            while stack:
                pos, st, v = stack.pop()
                if (pos, st, v) in visited:
                    continue
                visited.add((pos, st, v))
                if sum(v) > OUTMAX:
                    continue
                if pos == L and st in finals:
                    outs.add(v)
                for (iw, oi, q) in byp.get(st, []):
                    if x.startswith(iw, pos):
                        nv = list(v); nv[oi] += 1
                        stack.append((pos + len(iw), q, tuple(nv)))
            if outs:
                res_any |= outs
                if primitive(x):
                    res_q |= outs
    return res_any, res_q

def show(name, edges, start, finals, outalpha, OUTMAX):
    A, Qs = image_sets(edges, start, finals, outalpha, OUTMAX)
    N = sorted(A - Qs)
    print(f'== {name}: |image|={len(A)}  |Q-image|={len(Qs)}  N (forced non-primitive) =')
    print('   ', N if len(N) < 60 else (N[:60], '...'))

def random_transducer(rng, nstates, nedges, outalpha):
    edges = []
    for _ in range(nedges):
        p = rng.randrange(nstates); q = rng.randrange(nstates)
        iw = ''.join(rng.choice('ab') for _ in range(rng.choice([0, 1, 1, 2, 2])))
        edges.append((p, iw, rng.choice(outalpha), q))
    finals = {rng.randrange(nstates)}
    return edges, 0, finals

if __name__ == '__main__':
    OUT = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    # Adversarial 1: x in (a^+ b)^3, output c^i d^j e^k with i,j,k the block lengths.
    E1 = [(0, 'a', 'c', 1), (1, 'a', 'c', 1), (1, 'b', 'z', 2), (2, 'a', 'd', 3), (3, 'a', 'd', 3),
          (3, 'b', 'z', 4), (4, 'a', 'e', 5), (5, 'a', 'e', 5), (5, 'b', 'z', 6)]
    show('(a^i b a^j b a^k b) -> c^i d^j e^k z^3  [N should be i=j=k]', E1, 0, {6}, 'cdez', OUT)
    # Adversarial 2: only length is output, input in (ab*)^*  -> unary
    E2 = [(0, 'a', 'c', 1), (1, 'b', 'c', 1), (1, 'a', 'c', 1)]
    show('x in a(a+b)^* -> c^|x|', E2, 0, {1}, 'c', OUT)
    # Adversarial 3: input (ab)^n (ab)^m with output c^n d^m: always non-primitive unless n+m=1
    E3 = [(0, 'ab', 'c', 0), (0, '', 'z', 1), (1, 'ab', 'd', 1)]
    show('(ab)^n z (ab)^m -> c^n z d^m', E3, 0, {1}, 'cdz', OUT)
    # Adversarial 4: input a^n b a^m b, output only n+m (unary) -> N = {0}? (bb), and n=m forced? no
    E4 = [(0, 'a', 'c', 0), (0, 'b', 'z', 1), (1, 'a', 'c', 1), (1, 'b', 'z', 2)]
    show('a^n b a^m b -> c^{n+m} z^2', E4, 0, {2}, 'cz', OUT)
    rng = random.Random(7)
    for t in range(6):
        edges, s, F = random_transducer(rng, 3, 7, 'cd')
        show(f'random #{t} {edges} F={F}', edges, s, F, 'cd', OUT)
