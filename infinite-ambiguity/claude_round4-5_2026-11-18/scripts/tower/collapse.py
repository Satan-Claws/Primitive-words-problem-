# Deterministic streaming tower machines (b opens at every level, no swap).
# record = [d, active, received]. Input enters top record. A record completing a piece
# (closing letter 'a' at d==0) emits type ('b' if active else 'a') to the record below it.
# ABS: completed records are replaced by fresh records (absolute levels; j fresh after a j-cascade).
# COL: after a j-cascade only ONE fresh record is put back (levels collapse; mixed depth).
# accept(u): at end, some record has received exactly 1 letter and all records above it are fresh.
import sys, itertools
sys.path.insert(0, '../walk'); from walk import primitive
def run(u, mode):
    st = [[0, False, 0]]           # st[-1] = top (level 1)
    for x in u:
        i = len(st) - 1; popped = 0
        while True:
            if i < 0:
                if len(st) > len(u): break
                st.insert(0, [0, False, 0]); i = 0
            r = st[i]; r[2] += 1
            if x == 1 and False: pass
            if x == -1:            # b opens
                r[0] += 1; r[1] = True; break
            if r[0] > 0:
                r[0] -= 1; break
            t = -1 if r[1] else 1  # complete piece
            r[0], r[1] = 0, False
            popped += 1; x = t; i -= 1
        if mode == 'COL' and popped >= 2:
            # remove the popped fresh records except one
            top = len(st) - 1
            del st[top - popped + 2: top + 1]
    return st
def accept(u, mode):
    st = run(u, mode)
    for k in range(len(st)):       # st[k], records above it are st[k+1:]
        if st[k][2] == 1 and all(r[0] == 0 and not r[1] for r in st[k+1:]):
            return True
    return False
N = int(sys.argv[1])
for mode in ('ABS', 'COL'):
    for n in range(1, N+1):
        c = bad = 0; ex = None
        for v in itertools.product((1, -1), repeat=n):
            if any(accept(v[r:]+v[:r], mode) for r in range(n)):
                c += 1
                if not primitive(v):
                    bad += 1; ex = ex or ''.join('a' if t == 1 else 'b' for t in v)
        print(mode, n, c, round(c/2**n, 4), 'nonprim', bad, ex, flush=True)
