"""Check Prop D (half-dimension of forced non-primitive sets) empirically.
For random merge-free slices B = x0 y1^e1 x1 ... yr^er xr (x0 absorbed cyclically),
count Nb(R) = #{e in [0,R)^r : W(e) not primitive} for R, 2R and report the
growth exponent log2(Nb(2R)/Nb(R)); Prop D predicts exponent <= floor(r/2) asymptotically.
Also records max over e of Nb restricted to sub-boxes is not needed.
usage: python3 halfdim_check.py seed ninst r R
"""
import sys, random, math, itertools

def primitive(w):
    n = len(w)
    if n == 0: return False
    return (w + w).find(w, 1) == n

def is_prim_word(y):
    return primitive(y)

def merges(x, y, ynext, c):
    # x y_next^c prefix of y^omega ?
    s = x + ynext * c
    yw = y * (len(s) // len(y) + 2)
    return yw.startswith(s)

def rand_word(L, rng):
    return ''.join(rng.choice('ab') for _ in range(L))

def main():
    seed, ninst, r, R = map(int, sys.argv[1:5])
    rng = random.Random(seed)
    done = 0
    worst = 0.0
    while done < ninst:
        ys = []
        while len(ys) < r:
            y = rand_word(rng.randint(1, 2), rng)
            if is_prim_word(y): ys.append(y)
        xs = [rand_word(rng.randint(0, 2), rng) for _ in range(r)]
        Y = max(map(len, ys)); c = Y + 1
        if any(merges(xs[i], ys[i], ys[(i + 1) % r], c) for i in range(r)):
            continue
        done += 1
        def count(Rr):
            cnt = 0
            for e in itertools.product(range(Rr), repeat=r):
                w = ''.join(ys[i] * e[i] + xs[i] for i in range(r))
                if not primitive(w): cnt += 1
            return cnt
        n1, n2 = count(R), count(2 * R)
        ex = math.log2(n2 / n1) if n1 > 0 else 0.0
        worst = max(worst, ex)
        print(ys, xs, n1, n2, round(ex, 3))
    print('r =', r, 'max growth exponent', round(worst, 3), 'bound floor(r/2) =', r // 2)

main()
