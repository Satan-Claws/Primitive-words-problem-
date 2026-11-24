"""R6 Lemma A check: if the drift-corrected cyclic walk T(i) = n*S(i) - i*A of w has a unique argmax r,
the rotation starting at r lies in G^- = {v : d_k(v) < 0 for all 1 <= k <= n/2} (subset of F_K, subset of Q).
Exhaustive n <= 18: (i) Lemma A never fails; (ii) |Q_n minus Rot(G^-)|, |{#argmax>=2}|; (iii) G^- has no non-primitive word.
Usage: python r6_miss_lemmaA.py [NMAX=18]"""
import sys
import numpy as np
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 18
print('n  |Q_n|  |Q_n \\ Rot(G-)|  #(argmax>=2 in Q_n)  LemmaA-fail  G- nonprimitive')
for n in range(2, NMAX + 1):
    W = np.arange(1 << n)
    X = ((W[:, None] >> np.arange(n)) & 1).astype(np.int64)
    prim = np.ones(len(W), bool)
    for p in range(2, n + 1):
        if n % p == 0 and all(p % q for q in range(2, p)):
            d = n // p; prim &= ~np.all(X == np.roll(X, -d, 1), 1)
    A = X.sum(1, keepdims=True)
    Sp = np.concatenate([np.zeros((len(W), 1), np.int64), np.cumsum(X, 1)], 1)  # S(0..n)
    Tfull = n * Sp[:, :n] - np.arange(n)[None] * A
    amax = Tfull.argmax(1); cnt = (Tfull == Tfull.max(1, keepdims=True)).sum(1)
    # G^- membership of every rotation: d_k^{(r)} = T(r+k)+T(r-k)-2T(r) (cyclic T)
    inG = np.zeros((len(W), n), bool)
    ks = np.arange(1, n // 2 + 1)
    for r in range(n):
        d = Tfull[:, (r + ks) % n] + Tfull[:, (r - ks) % n] - 2 * Tfull[:, [r]]
        inG[:, r] = np.all(d < 0, 1)
    rotG = inG.any(1)
    lemfail = np.sum((cnt == 1) & ~inG[np.arange(len(W)), amax])
    print(n, prim.sum(), np.sum(prim & ~rotG), np.sum(prim & (cnt >= 2)), lemfail, np.sum(inG[:, 0] & ~prim))
