r"""
Explicit CFG for coPow_k = {a,b}^* \ { u^k : u in {a,b}^* }, checked by an Earley parser
against brute force for all words up to length LMAX.

Grammar (k >= 2):
  S   -> N | M
  N   -> R_1 | ... | R_{k-1}            (length not divisible by k)
  R_r -> X^r T ;  T -> eps | X^k T ;  X -> a | b
  M   -> A[r,c] B[k-2-r,d]   for 0<=r<=k-2, (c,d) in {(a,b),(b,a)}
  A[r,c] -> X^{k-1} A[r,c] X | X^r c        ( = { x c y : |x| = (k-1)|y| + r } )
  B[s,d] -> X B[s,d] X^{k-1} | d X^s        ( = { y d z : |z| = (k-1)|y| + s } )
Usage: python3 copow_grammar.py k LMAX
"""
import sys, itertools

def grammar(k):
    G = {}
    G['X'] = [('a',), ('b',)]
    G['T'] = [(), ('X',) * k + ('T',)]
    G['N'] = [(f'R{r}',) for r in range(1, k)]
    for r in range(1, k):
        G[f'R{r}'] = [('X',) * r + ('T',)]
    G['M'] = []
    for r in range(0, k - 1):
        s = k - 2 - r
        for c, d in (('a', 'b'), ('b', 'a')):
            A = f'A{r}{c}'; B = f'B{s}{d}'
            G['M'].append((A, B))
            G[A] = [('X',) * (k - 1) + (A, 'X'), ('X',) * r + (c,)]
            G[B] = [('X', B) + ('X',) * (k - 1), (d,) + ('X',) * s]
    G['S'] = [('N',), ('M',)]
    return G

def earley(G, start, w):
    n = len(w)
    S = [set() for _ in range(n + 1)]
    S[0] = {(start, rhs, 0, 0) for rhs in G[start]}
    for i in range(n + 1):
        agenda = list(S[i])
        while agenda:
            (A, rhs, dot, org) = agenda.pop()
            if dot < len(rhs):
                X = rhs[dot]
                if X in G:  # predict
                    for r in G[X]:
                        it = (X, r, 0, i)
                        if it not in S[i]:
                            S[i].add(it); agenda.append(it)
                    # nullable completion (aycock-horspool): if X already completed at i from i
                    for (B, r2, d2, o2) in list(S[i]):
                        if B == X and d2 == len(r2) and o2 == i:
                            it = (A, rhs, dot + 1, org)
                            if it not in S[i]:
                                S[i].add(it); agenda.append(it)
                elif i < n and w[i] == X:  # scan
                    S[i + 1].add((A, rhs, dot + 1, org))
            else:  # complete
                for (B, r2, d2, o2) in list(S[org]):
                    if d2 < len(r2) and r2[d2] == A:
                        it = (B, r2, d2 + 1, o2)
                        if it not in S[i]:
                            S[i].add(it); agenda.append(it)
    return any(A == start and dot == len(rhs) and org == 0 for (A, rhs, dot, org) in S[n])

def is_kth_power(w, k):
    n = len(w)
    if n % k: return False
    m = n // k
    return w == w[:m] * k

def main():
    k = int(sys.argv[1]); L = int(sys.argv[2])
    G = grammar(k)
    total = 0
    for n in range(0, L + 1):
        for t in itertools.product('ab', repeat=n):
            w = ''.join(t)
            g = earley(G, 'S', w)
            b = not is_kth_power(w, k)
            total += 1
            if g != b:
                print("MISMATCH", k, w, g, b); return
    print(f"k={k}: grammar == coPow_k on all {total} words of length <= {L}")

if __name__ == '__main__':
    main()
