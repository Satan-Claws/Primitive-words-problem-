"""r18_sh6_sp: exact Sardinas-Patterson-type test of C_exp (= non-freeness of the interface monoid) for a
single linear SCC X -> u X v | w with sides literal or a prime-Dyck block B (a=+1,b=-1).

C_exp <=> two distinct token sequences with the same (U, V), U = u1..uk, V = vk..v1
      <=> the generator set {(u, v^R)} is NOT a code in S* x S*.
Blocks are emitted lazily: a pending block is Blk(h) (h = current height, 0 = not yet started; on the R tape the
reversed block B^R has b=+1). Two aligned pending blocks are resolved jointly (the lower one closes first; any common
continuation is allowed), so the state is finite-describable: per tape, the leader's surplus queue.
BFS over states; success = both tapes balanced. If the reachable state set is finite and has no success state, the
generator set is a code, i.e. NO C_exp (an exact proof for this grammar, modulo correctness of this code).
Usage: r18_sh6_sp.py NAME [maxstates]
"""
import sys
from collections import deque
sys.path.insert(0, __import__('os').path.dirname(__file__))
EX = {
 'SH3': [('ab','ab'),('bb','a'),('','ba'),('a','B'),('B','aa'),('a','bb'),('ab','bb')],
 'SH6': [('ab','ab'),('bb','a'),('','ba'),('a','B'),('B','bb'),('a','bb'),('ab','aa')],
 'SH1': [('ab','ab'),('bb','a'),('','ba'),('a','B'),('B','aa'),('','bbb'),('a','baa')],
 'SH4': [('ab','ab'),('bb','a'),('','ba'),('a','B'),('B','aa'),('a','bbb'),('b','bb')],
}
PLUS = {'L': 'a', 'R': 'b'}  # opening letter of the block on each tape

def gens(tok):
    out = []
    for u, v in tok:
        L = ('B',) if u == 'B' else tuple(u)
        R = ('B',) if v == 'B' else tuple(v[::-1])
        out.append((L, R))
    return out

def items(seq):
    return tuple(('K', 0) if c == 'B' else c for c in seq)   # ('K',h) = pending block of height h

def step(tape, q1, q2):
    """cancel common heads of two queues on one tape; return (q1,q2) with one empty, or None if dead."""
    p = PLUS[tape]
    q1 = list(q1); q2 = list(q2)
    while q1 and q2:
        x, y = q1[0], q2[0]
        if isinstance(x, str) and isinstance(y, str):
            if x != y: return None
            q1.pop(0); q2.pop(0); continue
        if isinstance(x, tuple) and isinstance(y, tuple):
            hx, hy = x[1], y[1]
            # both blocks aligned: lower closes first (fresh = height 0 started jointly)
            if hx == hy:
                q1.pop(0); q2.pop(0)
            elif hx < hy:
                q1.pop(0); q2[0] = ('K', hy - hx)
            else:
                q2.pop(0); q1[0] = ('K', hx - hy)
            continue
        # block vs letter
        if isinstance(y, tuple):
            q1, q2 = q2, q1; x, y = y, x; swapped = True
        else:
            swapped = False
        h = x[1]; c = y
        d = 1 if c == p else -1
        if h == 0 and d < 0: return None
        h += d
        q2.pop(0)
        if h == 0: q1.pop(0)
        else: q1[0] = ('K', h)
        if swapped: q1, q2 = q2, q1
    return tuple(q1), tuple(q2)

def norm(state):
    (l1, l2), (r1, r2), path = state
    return (l1, l2, r1, r2)

def run(name, maxstates=10**6, maxq=60):
    G = gens(EX[name]); n = len(G)
    seen = {}; dq = deque()
    for i in range(n):
        for j in range(n):
            if i == j: continue
            L = step('L', items(G[i][0]), items(G[j][0])); R = step('R', items(G[i][1]), items(G[j][1]))
            if L is None or R is None: continue
            key = (L, R)
            if key not in seen:
                seen[key] = ((i,), (j,)); dq.append(key)
    capped = 0
    while dq:
        key = dq.popleft(); (l1, l2), (r1, r2) = key; s1, s2 = seen[key]
        if not l1 and not l2 and not r1 and not r2:
            return 'WITNESS', s1, s2, len(seen)
        # parse behind on some tape: queue empty while the other's is nonempty
        if (not l1 and l2) or (not r1 and r2): p = 1
        else: p = 2
        for g in range(n):
            gl, gr = items(G[g][0]), items(G[g][1])
            if p == 1:
                L = step('L', l1 + gl, l2); R = step('R', r1 + gr, r2); ns = (s1 + (g,), s2)
            else:
                L = step('L', l1, l2 + gl); R = step('R', r1, r2 + gr); ns = (s1, s2 + (g,))
            if L is None or R is None: continue
            nk = (L, R)
            if max(len(x) for x in L + R) > maxq: capped += 1; continue
            if nk not in seen:
                seen[nk] = ns; dq.append(nk)
                if len(seen) > maxstates: return 'UNDECIDED (state cap)', None, None, len(seen)
    return ('CODE: no C_exp' if not capped else 'UNDECIDED (queue cap hit %d times)' % capped), None, None, len(seen)

if __name__ == '__main__':
    name = sys.argv[1]; ms = int(sys.argv[2]) if len(sys.argv) > 2 else 10**6
    mq = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    res, s1, s2, ns = run(name, ms, mq)
    print(name, res, 'states=%d' % ns)
    if s1:
        T = EX[name]
        print(' seq1:', ' '.join('(%s,%s)' % T[g] for g in s1))
        print(' seq2:', ' '.join('(%s,%s)' % T[g] for g in s2))
