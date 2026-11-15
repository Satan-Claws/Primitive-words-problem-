"""Computer check of the 'rigid case' of Lemma I (reports/closure.md, Lemma I, step f).

Setting: cyclic parametric word W(e) = y_1^{e_1} x_1 ... y_r^{e_r} x_r, y_i primitive,
no cyclically adjacent pair (i,i+1) "merges" (x_i y_{i+1}^c is not a prefix of y_i^omega,
c = 1 + max|y|).  Claim (F1-F3): for all e with every e_i >= T,
    W(e) is NOT primitive  <=>  there is s in {1..r-1} with U'_i(e) = U'_{i+s}(e) for all i,
where U'_i(e) is the factor of the cyclic word between the left ends of the maximal
|y_i|-periodic arcs R_i, R_{i+1} around the blocks.  We compute a_i (left extension of
R_i beyond block i) directly on the word, and compare with brute force primitivity.
"""
import random, itertools, sys

def primitive(w):
    return len(w) > 0 and (w + w).find(w, 1) == len(w)

def is_prim_root(y):
    return primitive(y)

def merges(y, x, z, c):
    # x z^c prefix of y^omega ?
    t = x + z * c
    yo = y * (len(t) // len(y) + 2)
    return yo.startswith(t)

def build(ys, xs, e):
    w = ''
    starts = []
    for y, x, k in zip(ys, xs, e):
        starts.append(len(w))
        w += y * k + x
    return w, starts

def left_ext(w, start, p):
    # how far to the left of 'start' does period p (cyclic word w) extend, given the
    # block starting at start is p-periodic to the right
    n = len(w)
    a = 0
    while a < n:
        j = (start - a - 1) % n
        if w[j] != w[(j + p) % n]:
            break
        a += 1
    return a

def check_instance(ys, xs, T, M, rng):
    r = len(ys)
    c = 1 + max(len(y) for y in ys)
    for i in range(r):
        if merges(ys[i], xs[i], ys[(i + 1) % r], c):
            return None  # not in the rigid case
    bad = 0
    tested = 0
    for _ in range(200):
        e = [rng.randint(T, M) for _ in range(r)]
        # bias: sometimes make e shift-invariant to hit non-primitive cases
        if rng.random() < 0.5 and r >= 2:
            s = rng.randint(1, r - 1)
            for i in range(r):
                e[(i + s) % r] = e[i] if rng.random() < 0.9 else e[(i + s) % r]
        w, starts = build(ys, xs, e)
        n = len(w)
        A = [left_ext(w, starts[i], len(ys[i])) for i in range(r)]
        Rstart = [(starts[i] - A[i]) % n for i in range(r)]
        U = []
        for i in range(r):
            a, b = Rstart[i], Rstart[(i + 1) % r]
            L = (b - a) % n
            U.append((w + w)[a:a + L] if L > 0 else '')
        pred_nonprim = any(all(U[i] == U[(i + s) % r] for i in range(r)) for s in range(1, r))
        truth_nonprim = not primitive(w)
        tested += 1
        if pred_nonprim != truth_nonprim:
            bad += 1
            print('MISMATCH', ys, xs, e, pred_nonprim, truth_nonprim)
            break
    return bad, tested

def randword(rng, lo, hi):
    return ''.join(rng.choice('ab') for _ in range(rng.randint(lo, hi)))

def main():
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    inst = 0; mism = 0; total = 0
    while inst < 3000:
        r = rng.randint(1, 4)
        ys = []
        while len(ys) < r:
            y = randword(rng, 1, 3)
            if is_prim_root(y):
                ys.append(y)
        # make repeated block types likely
        if r >= 2 and rng.random() < 0.6:
            per = rng.choice([d for d in range(1, r) if r % d == 0])
            ys = [ys[i % per] for i in range(r)]
            xs0 = [randword(rng, 0, 3) for _ in range(per)]
            xs = [xs0[i % per] if rng.random() < 0.85 else randword(rng, 0, 3) for i in range(r)]
        else:
            xs = [randword(rng, 0, 3) for _ in range(r)]
        Y = max(len(y) for y in ys); X = max(len(x) for x in xs)
        c = 1 + Y
        Astar = X + c * Y
        T = max(c + 1, 4 * Y + X + 2 * Astar + 2)
        res = check_instance(ys, xs, T, T + 12, rng)
        if res is None:
            continue
        inst += 1
        mism += res[0]; total += res[1]
    print('rigid instances:', inst, 'exponent vectors tested:', total, 'mismatches:', mism)

if __name__ == '__main__':
    main()
