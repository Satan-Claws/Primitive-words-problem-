#!/usr/bin/env python3
"""
check_grammar.py -- test a context-free grammar against the language Q of primitive words.

EVIDENCE TOOL ONLY: agreement up to length N proves nothing about longer words.

USAGE (command line)
    python3 check_grammar.py GRAMMAR_FILE [--N 20] [--alphabet ab] [--start S]
                             [--target Q|NS|NC|NSC] [--show 10]
                             [--long 21-30] [--samples 200] [--seed 0]
                             [--word abaab ...]

    GRAMMAR_FILE format (one or more rules per line, '#' starts a comment):
        S  -> A B | a | eps
        A  -> a A b | B
        B  -> ab B          # a token that is not a nonterminal is a terminal *string*:
                            # 'ab' means the two terminals a, b
    * Nonterminals = exactly the symbols that occur on some left-hand side.
    * Every other RHS token must consist of alphabet letters; it is split into letters.
    * Empty word: 'eps', 'ε', 'epsilon', or an empty alternative ("A -> | a").
    * Start symbol: the first LHS, unless --start is given.
    * Any CFG form is accepted (unit rules, epsilon rules, long right-hand sides,
      useless symbols, left recursion...).

    What it does:
      1. Computes L(G) ∩ Σ^m exactly for every m <= N (bitset dynamic programming
         over all |Σ|^m words; N=20 over {a,b} takes seconds to a minute and ~2 MB per
         nonterminal).  Prints, per length, |L∩Σ^m|, |T∩Σ^m| and the two error counts,
         then the first (shortlex) counterexamples on each side:
            "in L(G) but not in T"   (L ⊄ T: soundness failures)
            "in T but not in L(G)"   (T ⊄ L: completeness failures)
         Also reports whether ε ∈ L(G) (ε must NOT be in Q).
      2. --long A-B : for each length m in [A,B], runs an Earley recognizer on ALL
         non-primitive words of length m (they are few: O(|Σ|^{m/2})) and on
         --samples random words (rejecting non-primitive ones), reporting errors.
      3. --word w1 w2 ... : Earley membership for the given words.
    Exit code 0 iff no counterexample was found.

USAGE (Python API)
    import sys; sys.path.insert(0, '<campaign>/tools'); import check_grammar as cg
    G = cg.parse_grammar(open('g.txt').read())          # or build the dict yourself:
    # G = {'start': 'S', 'rules': {'S': [('A','B'), ('a',), ()], ...}}
    #   (RHS tuples of symbols; a symbol is a nonterminal iff it is a key of rules;
    #    otherwise it must be a single alphabet letter; () is epsilon)
    report = cg.check(G, alphabet='ab', N=16, target='Q', show=10)   # prints + returns dict
    langs = cg.language_bitsets(G, 'ab', 12)  # {nt: [bool np.array of size k^m for m=0..12]}
    cg.earley(G, 'abab')                       # -> False/True
    Word <-> index: word w_1...w_m  <->  sum w_i * k^(m-i)  (letters indexed by position in
    the alphabet string), so array order is lexicographic order.

TARGETS: Q = primitive words (ε excluded), NS = non-squares (not of the form uu; ε is a
square), NC = non-cubes, NSC = neither square nor cube.
"""
import sys, re, random, argparse
import numpy as np

EPS_TOKENS = {'eps', 'ε', 'epsilon', 'EPS', 'λ', 'lambda'}

# ----------------------------------------------------------------------------- parsing
def parse_grammar(text, start=None, alphabet=None):
    raw = []
    for line in text.splitlines():
        line = line.split('#', 1)[0].strip()
        if not line:
            continue
        if '->' not in line:
            raise ValueError(f"no '->' in line: {line!r}")
        lhs, rhs = line.split('->', 1)
        lhs = lhs.strip()
        if not lhs or len(lhs.split()) != 1:
            raise ValueError(f"bad LHS in line: {line!r}")
        raw.append((lhs, rhs))
    nts = {l for l, _ in raw}
    rules = {nt: [] for nt in nts}
    for lhs, rhs in raw:
        for alt in rhs.split('|'):
            syms = []
            for tok in alt.split():
                if tok in EPS_TOKENS:
                    continue
                if tok in nts:
                    syms.append(tok)
                else:
                    for ch in tok:
                        if alphabet is not None and ch not in alphabet:
                            raise ValueError(f"token {tok!r} is neither a nonterminal nor "
                                             f"a string over the alphabet {alphabet!r}")
                        syms.append(ch)
            rules[lhs].append(tuple(syms))
    if start is None:
        start = raw[0][0]
    if start not in nts:
        raise ValueError(f"start symbol {start!r} has no rules")
    return {'start': start, 'rules': rules}

# ----------------------------------------------------------------- normalisation
def _binarize(G, alphabet):
    """Return (nts, unary, binary, eps, term) where every rule has RHS of length <= 2,
    terminals are replaced by fresh nonterminals T<c> with L = {c}."""
    rules = G['rules']
    for nt, alts in rules.items():
        for rhs in alts:
            for s in rhs:
                if s not in rules and s not in alphabet:
                    raise ValueError(f"symbol {s!r} in rule for {nt!r} is neither a "
                                     f"nonterminal nor a letter of {alphabet!r}")
    termnt = {c: ('#T', c) for c in alphabet}
    nts = list(rules) + list(termnt.values())
    unary, binary, eps = [], [], set()
    fresh = [0]
    def sym(s):
        return s if s in rules else termnt[s]
    for A, alts in rules.items():
        for rhs in alts:
            rhs = [sym(s) for s in rhs]
            if len(rhs) == 0:
                eps.add(A)
            elif len(rhs) == 1:
                unary.append((A, rhs[0]))
            else:
                cur = A
                while len(rhs) > 2:
                    fresh[0] += 1
                    X = ('#B', fresh[0])
                    nts.append(X)
                    binary.append((cur, rhs[0], X))
                    cur, rhs = X, rhs[1:]
                binary.append((cur, rhs[0], rhs[1]))
    return nts, unary, binary, eps, termnt

def language_bitsets(G, alphabet='ab', N=20, verbose=False):
    """L(X) ∩ Σ^m for every nonterminal X (including internal ones) and m = 0..N,
    as boolean numpy arrays of length k^m (lexicographic word order)."""
    k = len(alphabet)
    nts, unary, binary, eps, termnt = _binarize(G, alphabet)
    L = {X: [] for X in nts}
    for m in range(N + 1):
        size = k ** m
        cur = {X: np.zeros(size, dtype=bool) for X in nts}
        if m == 0:
            for X in eps:
                cur[X][0] = True
        if m == 1:
            for i, c in enumerate(alphabet):
                cur[termnt[c]][i] = True
        L_m = cur
        for X in nts:
            L[X].append(L_m[X])
        # contributions from proper splits (fixed, all factors shorter)
        if m >= 2:
            for (A, B, C) in binary:
                for i in range(1, m):
                    lb, lc = L[B][i], L[C][m - i]
                    if lb.any() and lc.any():
                        L_m[A] |= np.outer(lb, lc).ravel()
        # fixpoint for same-length dependencies: unit rules and nullable splits
        changed = True
        while changed:
            changed = False
            for (A, B) in unary:
                new = L_m[A] | L_m[B]
                if not np.array_equal(new, L_m[A]):
                    L_m[A][:] = new; changed = True
            for (A, B, C) in binary:
                new = L_m[A]
                if L[B][0][0]:
                    new = new | L_m[C]
                if L[C][0][0]:
                    new = new | L_m[B]
                if not np.array_equal(new, L_m[A]):
                    L_m[A][:] = new; changed = True
        if verbose:
            print(f"  length {m} done", file=sys.stderr)
    return L

# ----------------------------------------------------------------- targets
def target_mask(m, k, target='Q'):
    """bool array over Σ^m: membership in the target language."""
    size = k ** m
    if m == 0:
        return np.array([False])   # ε is not primitive, and is a square and a cube
    x = np.arange(size, dtype=np.int64)
    def is_power(e):
        if m % e:
            return np.zeros(size, dtype=bool)
        d = m // e
        rot = (x * k ** d) % size + x // k ** (m - d)   # rotation by d letters
        return rot == x
    if target == 'Q':
        res = np.ones(size, dtype=bool)
        for d in range(1, m):
            if m % d == 0:
                rot = (x * k ** d) % size + x // k ** (m - d)
                res &= rot != x
        return res
    if target == 'NS':
        return ~is_power(2)
    if target == 'NC':
        return ~is_power(3)
    if target == 'NSC':
        return ~is_power(2) & ~is_power(3)
    raise ValueError(target)

def is_primitive(w):
    return len(w) > 0 and (w + w).find(w, 1) == len(w)

def word_of(idx, m, alphabet):
    k = len(alphabet)
    out = []
    for _ in range(m):
        idx, r = divmod(idx, k)
        out.append(alphabet[r])
    return ''.join(reversed(out)) if m else 'ε'

# ----------------------------------------------------------------- Earley
def earley(G, w):
    """Earley recognizer for an arbitrary CFG (handles ε and unit rules)."""
    rules, S = G['rules'], G['start']
    # nullable set
    nullable, ch = set(), True
    while ch:
        ch = False
        for A, alts in rules.items():
            if A not in nullable and any(all(s in nullable for s in r) for r in alts):
                nullable.add(A); ch = True
    n = len(w)
    chart = [set() for _ in range(n + 1)]
    GAMMA = ('#start',)
    chart[0].add((GAMMA, (S,), 0, 0))
    for i in range(n + 1):
        agenda = list(chart[i])
        while agenda:
            item = agenda.pop()
            A, rhs, dot, org = item
            if dot < len(rhs):
                X = rhs[dot]
                if X in rules:   # predict
                    for r in rules[X]:
                        it = (X, r, 0, i)
                        if it not in chart[i]:
                            chart[i].add(it); agenda.append(it)
                    if X in nullable:   # Aycock-Horspool
                        it = (A, rhs, dot + 1, org)
                        if it not in chart[i]:
                            chart[i].add(it); agenda.append(it)
                elif i < n and w[i] == X:   # scan
                    chart[i + 1].add((A, rhs, dot + 1, org))
            else:   # complete
                for (B, r2, d2, o2) in list(chart[org]):
                    if d2 < len(r2) and r2[d2] == A:
                        it = (B, r2, d2 + 1, o2)
                        if it not in chart[i]:
                            chart[i].add(it); agenda.append(it)
    return (GAMMA, (S,), 1, 0) in chart[n]

# ----------------------------------------------------------------- main check
def check(G, alphabet='ab', N=20, target='Q', show=10, quiet=False):
    k = len(alphabet)
    L = language_bitsets(G, alphabet, N)[G['start']]
    out = print if not quiet else (lambda *a, **kw: None)
    fp, fn = [], []   # (length, idx)
    out(f"Checking L(G) against {target} over alphabet {alphabet!r} for lengths 0..{N}")
    out("%3s %10s %10s %8s %8s" % ('m', '|L∩Σ^m|', '|T∩Σ^m|', 'L-T', 'T-L'))
    tot_fp = tot_fn = 0
    for m in range(N + 1):
        T = target_mask(m, k, target)
        a, b = L[m] & ~T, T & ~L[m]
        na, nb = int(a.sum()), int(b.sum())
        tot_fp += na; tot_fn += nb
        out(f"{m:>3} {int(L[m].sum()):>10} {int(T.sum()):>10} {na:>8} {nb:>8}")
        if len(fp) < show:
            fp += [(m, int(i)) for i in np.flatnonzero(a)[: show - len(fp)]]
        if len(fn) < show:
            fn += [(m, int(i)) for i in np.flatnonzero(b)[: show - len(fn)]]
    fpw = [word_of(i, m, alphabet) for m, i in fp]
    fnw = [word_of(i, m, alphabet) for m, i in fn]
    out(f"\nTotal: {tot_fp} words in L(G) \\ {target}, {tot_fn} words in {target} \\ L(G) (lengths <= {N})")
    out(f"First words in L(G) but not in {target}: {fpw if fpw else 'none'}")
    out(f"First words in {target} but not in L(G): {fnw if fnw else 'none'}")
    return {'false_positives': tot_fp, 'false_negatives': tot_fn,
            'first_fp': fpw, 'first_fn': fnw}

def nonprimitive_words(m, alphabet):
    """All non-primitive words of length m (as strings)."""
    res = set()
    for d in range(1, m):
        if m % d == 0:
            k = len(alphabet)
            if k ** d > 2_000_000:
                raise ValueError("too many")
            for idx in range(k ** d):
                u = word_of(idx, d, alphabet)
                res.add(u * (m // d))
    return sorted(res)

def long_check(G, alphabet, lo, hi, samples, seed, target='Q', show=10):
    if target != 'Q':
        print("--long only supports target Q"); return 0
    rng = random.Random(seed)
    errs = 0
    for m in range(lo, hi + 1):
        bad_np = [u for u in nonprimitive_words(m, alphabet) if earley(G, u)]
        bad_p, tested = [], 0
        while tested < samples:
            w = ''.join(rng.choice(alphabet) for _ in range(m))
            if not is_primitive(w):
                continue
            tested += 1
            if not earley(G, w):
                bad_p.append(w)
        errs += len(bad_np) + len(bad_p)
        print(f"length {m}: non-primitive accepted: {len(bad_np)} {bad_np[:show]}; "
              f"random primitive rejected: {len(bad_p)}/{samples} {bad_p[:show]}")
    return errs

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('grammar')
    ap.add_argument('--N', type=int, default=20)
    ap.add_argument('--alphabet', default='ab')
    ap.add_argument('--start', default=None)
    ap.add_argument('--target', default='Q', choices=['Q', 'NS', 'NC', 'NSC'])
    ap.add_argument('--show', type=int, default=10)
    ap.add_argument('--long', default=None, help='range A-B of longer lengths for Earley tests')
    ap.add_argument('--samples', type=int, default=200)
    ap.add_argument('--seed', type=int, default=0)
    ap.add_argument('--word', nargs='*', default=None)
    a = ap.parse_args()
    G = parse_grammar(open(a.grammar).read(), a.start, a.alphabet)
    if a.word:
        for w in a.word:
            print(f"{w}: in L(G) = {earley(G, w)}, primitive = {is_primitive(w)}")
        return
    rep = check(G, a.alphabet, a.N, a.target, a.show)
    errs = rep['false_positives'] + rep['false_negatives']
    if a.long:
        lo, hi = map(int, a.long.split('-'))
        errs += long_check(G, a.alphabet, lo, hi, a.samples, a.seed, a.target, a.show)
    sys.exit(0 if errs == 0 else 1)

if __name__ == '__main__':
    main()
