"""Certificate L_l (fixed number l of blocks per period).  x = block vector (0-indexed), K = len(x).
Reflection: R(i) = K-1-i if l odd (fixes residue class f=(l-1)/2), R(i) = K-2-i if l even (fixes classes
f = l/2-1 and g = l-1).  D = x - Rx.
Condition C_l(x):  K % l == 0, K >= 2l,
   D_i = [i==f] - [i==R(f)]  for i == f (mod l)          (exact, perturbed class)
   D_i = 0                    for i == g (mod l) (l even)  (exact, other fixed class)
   for every other class A: D is single-signed on A (all >=0 or all <=0)   (finite union over sign patterns)
Claims: C_l-words are primitive (exhaustive check, all words up to NMAX);
        every insertion of one a into u^k (|u|_b = l, k>=2) has a rotation satisfying C_l (random + exhaustive small)."""
import itertools, random
from refute import primitive, blocks

def refl(l, K):
    return (lambda i: K-1-i) if l % 2 else (lambda i: (K-2-i) % K)

def cond(l, x):
    K = len(x)
    if K % l or K < 2*l: return False
    R = refl(l, K)
    D = [x[i] - x[R(i)] for i in range(K)]
    if l % 2: f, g = (l-1)//2, None
    else: f, g = l//2 - 1, l - 1
    for i in range(K):
        r = i % l
        if r == f:
            if D[i] != (i == f) - (i == R(f)): return False
        elif r == g:
            if D[i] != 0: return False
    for A in range(l):
        if A in (f, g): continue
        vals = [D[i] for i in range(A, K, l)]
        if min(vals) < 0 < max(vals): return False
    return True

def check_sound(l, NMAX):
    cnt = 0
    for n in range(1, NMAX+1):
        for t in itertools.product('ab', repeat=n):
            w = ''.join(t); x = blocks(w)
            if x and cond(l, x):
                cnt += 1; assert primitive(w), (l, w)
    return cnt

def covered(l, x):
    K = len(x)
    return any(cond(l, x[r:] + x[:r]) for r in range(K))

if __name__ == '__main__':
    import sys
    for l, N in [(1, 20), (2, 20), (3, 21), (4, 20), (5, 20), (6, 20)]:
        c = check_sound(l, N)
        print(f'l={l}: {c} words of length <= {N} satisfy C_l, all primitive')
    rnd = random.Random(1)
    for l in range(1, 8):
        tot = 0
        for _ in range(3000):
            c = [rnd.randint(0, 6) for _ in range(l)]; k = rnd.randint(2, 5); j = rnd.randrange(l*k)
            x = c * k; x[j] += 1
            assert covered(l, x), (c, k, j); tot += 1
        # exhaustive small
        for c in itertools.product(range(4), repeat=l):
            if l > 5: break
            for k in (2, 3):
                for j in range(l*k):
                    x = list(c) * k; x[j] += 1; assert covered(l, x), (c, k, j); tot += 1
        print(f'l={l}: {tot} single-a insertions into u^k all covered')
    # F_2 and F_3 explicitly
    for p in range(0, 10):
        for q in range(0, 10):
            for r in range(0, 6):
                for k in range(2, 6):
                    x = [p, q, r] * k; x[0] += 1; assert covered(3, x)
    print('F_3 = a(a^p b a^q b a^r b)^k covered for p,q<10, r<6, k<6')
