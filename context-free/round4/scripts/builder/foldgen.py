# Generic "fold certificate": predicate R on the sign sequence of mirror pairs (outermost first),
# for every reflection axis (edge type; vertex type when n even).  Tests soundness (n<=SN) and completeness.
import sys, re
from common import *

def signs(w, vertex):
    n = len(w)
    rng = range(1, n // 2) if vertex else range(n // 2)
    out = []
    for i in rng:
        x, y = w[i], w[(n - i) if vertex else (n - 1 - i)]
        out.append('=' if x == y else ('<' if x < y else '>'))
    return ''.join(out)

CANDS = {
  'nogt':      lambda t: '<' in t and '>' not in t,
  'firstlast<': lambda t: (t.replace('=', '')[:1] == '<' and t.replace('=', '')[-1:] == '<'),
  'lt_then_gt': lambda t: re.fullmatch(r'[=<]*<[=<]*[=>]*', t) is not None,
  'gt_then_lt': lambda t: re.fullmatch(r'[=>]*[=<]*<[=<]*', t) is not None and '<' in t,
  'atmost1gt': lambda t: t.count('>') <= 1 and t.count('<') >= 2,
  'first<_no>after2': lambda t: t.replace('=', '')[:2] == '<<' and t.replace('=','').count('>') <= 1,
}

def inC(w, R):
    n = len(w)
    if R(signs(w, False)): return True
    if n % 2 == 0 and R(signs(w, True)): return True
    return False

if __name__ == '__main__':
    SN, N = int(sys.argv[1]), int(sys.argv[2])
    for name, R in CANDS.items():
        unsound = None
        for n in range(2, SN + 1):
            for w in all_words(n):
                if inC(w, R) and not is_primitive(w):
                    unsound = s(w); break
            if unsound: break
        if unsound:
            print(name, 'UNSOUND, e.g.', unsound); continue
        res = []
        for n in range(2, N + 1):
            res.append(sum(1 for w in lyndon(n) if not any(inC(r, R) for r in rotations(w))))
        print(name, 'sound<=%d' % SN, 'misses n=2..%d:' % N, res, flush=True)
