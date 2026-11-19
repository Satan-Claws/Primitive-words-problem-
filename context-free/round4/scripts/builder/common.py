# Common harness: enumerate primitive necklaces (Lyndon words) over {0,1} (a=0,b=1).
def lyndon(n):
    """Generate Lyndon words of length exactly n over {0,1} (FKM / Duval)."""
    w = [-1]
    while w:
        w[-1] += 1
        m = len(w)
        if m == n:
            yield tuple(w)
        while len(w) < n:
            w.append(w[len(w) - m])
        while w and w[-1] == 1:
            w.pop()

def rotations(w):
    n = len(w)
    for s in range(n):
        yield w[s:] + w[:s]

def is_primitive(w):
    n = len(w)
    for d in range(1, n):
        if n % d == 0 and all(w[i] == w[i % d] for i in range(n)):
            return False
    return n > 0

def s(w):
    return ''.join('ab'[x] for x in w)

def all_words(n):
    for x in range(1 << n):
        yield tuple((x >> (n - 1 - i)) & 1 for i in range(n))
