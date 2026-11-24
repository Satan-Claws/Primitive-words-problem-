"""r5_generic: the 'unique longest b-run' box cover (Prop B in R2/r5_generic.md).

UMR = {w : w[0] = a, w contains b, and the longest maximal b-run of w is unique}.
(a) exhaustive soundness: UMR ⊆ Q for all n <= 18;
(b) Monte Carlo density of UMR among uniform words, and among words with p | gcd(#a,#b)
    (sampled as a uniform word with prescribed #a, #a ≡ 0 mod p, n ≡ 0 mod p; #a drawn from the
    binomial law conditioned on p | #a).
"""
import itertools, random, math, sys

def primitive(w):
    n = len(w)
    return all(w != w[:d] * (n // d) for d in range(1, n) if n % d == 0)

def umr(w):
    if not w or w[0] != 'a' or 'b' not in w:
        return False
    runs = [len(r) for r in w.split('a') if r]
    m = max(runs)
    return runs.count(m) == 1

def exhaustive(N):
    bad = 0; tot = 0
    for n in range(1, N + 1):
        for t in itertools.product('ab', repeat=n):
            w = ''.join(t)
            if umr(w):
                tot += 1
                if not primitive(w):
                    bad += 1
    return tot, bad

def mc(n, trials, rng, p=None):
    hit = 0
    for _ in range(trials):
        if p is None:
            w = ''.join(rng.choice('ab') for _ in range(n))
        else:
            # sample #a from Binomial(n,1/2) conditioned on p | #a
            ks = list(range(0, n + 1, p))
            lg = [math.lgamma(n+1)-math.lgamma(k+1)-math.lgamma(n-k+1) for k in ks]
            M = max(lg); wts = [math.exp(x - M) for x in lg]
            k = rng.choices(ks, weights=wts)[0]
            l = ['a'] * k + ['b'] * (n - k)
            rng.shuffle(l); w = ''.join(l)
        hit += umr(w)
    return hit / trials

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 18
    tot, bad = exhaustive(N)
    print(f"(a) exhaustive n<={N}: |UMR| = {tot}, non-primitive members = {bad}")
    rng = random.Random(5)
    print("(b) n, P(UMR) uniform, P(UMR | p|g) (p = prime near sqrt n)")
    for n, p in [(253, 11), (1023, 31), (4087, 61), (16129, 127)]:
        t = 2000 if n < 10000 else 600
        print(n, p, round(mc(n, t, rng), 3), round(mc(n, t, rng, p), 3))
