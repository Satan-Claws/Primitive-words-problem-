# F — Computational report (round 1)

**Status: EVIDENCE ONLY.** Nothing here proves or refutes context-freeness of Q. Every
statement below about grammar sizes concerns finite truncations; the problem's own rules list
"finite computation" under *what does not count*. Where a statement is a theorem (e.g. the
symmetry-breaking lemma used in the SAT encoding, or soundness of a normal-form property) its
proof is given and is short; everything else is data.

Code: `/tmp/claude-5714/-home-shobhit--claude-spares-spare-fauO4P/6f48459d-5790-4a18-bccc-eabb8efc4544/scratchpad/compute/`
(`counts.py`, `mincnf.py`, `sweep.py`, `verify.py`, `table.py`, `classes.py`, `uniqfactor.py`;
raw SAT results in `sweep.jsonl`, `extra.jsonl`).
Reusable tool for other agents: `campaign/tools/check_grammar.py` (§3), example input
`campaign/tools/examples/nonsquares.txt`.
Environment: Python 3.12, numpy 1.26, python-sat 1.9.dev21 (CaDiCaL 1.5.3), 16 cores.

---------------------------------------------------------------------------------------------

## 1. Exact counts of Q ∩ {a,b}ⁿ, n ≤ 30

ψ(n) = Σ_{d|n} μ(d) 2^{n/d}. Brute force for n ≤ 22: for every x ∈ [0,2ⁿ) (bit string), x is
non-primitive iff x equals its cyclic rotation by d for some proper divisor d of n (vectorised
numpy). All 22 brute-force values agree with the Möbius formula. Last column ψ(n)/n is the
number of primitive conjugacy classes (= binary Lyndon words), used in §4.

| n | 2^n | primitive (Möbius) | non-primitive | brute force | classes ψ(n)/n |
|---|---|---|---|---|---|
| 1 | 2 | 2 | 0 | 2 (ok) | 2 |
| 2 | 4 | 2 | 2 | 2 (ok) | 1 |
| 3 | 8 | 6 | 2 | 6 (ok) | 2 |
| 4 | 16 | 12 | 4 | 12 (ok) | 3 |
| 5 | 32 | 30 | 2 | 30 (ok) | 6 |
| 6 | 64 | 54 | 10 | 54 (ok) | 9 |
| 7 | 128 | 126 | 2 | 126 (ok) | 18 |
| 8 | 256 | 240 | 16 | 240 (ok) | 30 |
| 9 | 512 | 504 | 8 | 504 (ok) | 56 |
| 10 | 1024 | 990 | 34 | 990 (ok) | 99 |
| 11 | 2048 | 2046 | 2 | 2046 (ok) | 186 |
| 12 | 4096 | 4020 | 76 | 4020 (ok) | 335 |
| 13 | 8192 | 8190 | 2 | 8190 (ok) | 630 |
| 14 | 16384 | 16254 | 130 | 16254 (ok) | 1161 |
| 15 | 32768 | 32730 | 38 | 32730 (ok) | 2182 |
| 16 | 65536 | 65280 | 256 | 65280 (ok) | 4080 |
| 17 | 131072 | 131070 | 2 | 131070 (ok) | 7710 |
| 18 | 262144 | 261576 | 568 | 261576 (ok) | 14532 |
| 19 | 524288 | 524286 | 2 | 524286 (ok) | 27594 |
| 20 | 1048576 | 1047540 | 1036 | 1047540 (ok) | 52377 |
| 21 | 2097152 | 2097018 | 134 | 2097018 (ok) | 99858 |
| 22 | 4194304 | 4192254 | 2050 | 4192254 (ok) | 190557 |
| 23 | 8388608 | 8388606 | 2 |  | 364722 |
| 24 | 16777216 | 16772880 | 4336 |  | 698870 |
| 25 | 33554432 | 33554400 | 32 |  | 1342176 |
| 26 | 67108864 | 67100670 | 8194 |  | 2580795 |
| 27 | 134217728 | 134217216 | 512 |  | 4971008 |
| 28 | 268435456 | 268419060 | 16396 |  | 9586395 |
| 29 | 536870912 | 536870910 | 2 |  | 18512790 |
| 30 | 1073741824 | 1073708010 | 33814 |  | 35790267 |

(Matches OEIS A027375 for the values I remember: 2, 2, 6, 12, 30, 54, 126, 240, 504, 990.)
Non-primitive count = 2^{n/2}+O(2^{n/3}) for even n, 2 for prime n.

---------------------------------------------------------------------------------------------

## 2. Minimum CNF grammar size for truncations (SAT)

### 2.1 Quantity computed
For a target T ⊆ {a,b}⁺ and n ≥ 1:

* `le`: k_≤(T,n) = min #nonterminals of a CNF grammar G (rules A→BC, A→c; no ε, no unit
  rules) with **L(G) ∩ Σ^{≤n} = T ∩ Σ^{≤n}** (G may generate anything longer);
* `eq`: k_=(T,n) = same with **L(G) ∩ Σⁿ = T ∩ Σⁿ** (other lengths unconstrained).

Targets: `all` = Σ⁺, `NS` = non-squares, `NC` = non-cubes, `NSC` = neither square nor cube,
`Q` = primitive words. Number of rules is unrestricted (≤ 2k + k³).

Trivially k_≤(T,n) is non-decreasing in n; for a CF target it is eventually constant
(bounded by the CNF size of any grammar for T); **Q is CF iff k_≤(Q,n) is bounded**. So the
only thing that could in principle be "seen" is unbounded growth — which no finite table can
show.

### 2.2 Encoding (file `mincnf.py`)
Nonterminals 0..k−1, 0 = start S. Variables:

* `t[A,c]` (rule A→c), `r[A,B,C]` (rule A→BC);
* `d[A,w]` ⇔ A ⇒* w, for all words 1 ≤ |w| < n and all A, and for |w| = n only A = S;
* `q[B,C,w]` ⇔ ∃ split w = uv (u,v ≠ ε) with d[B,u] ∧ d[C,v];
* auxiliaries `p[B,C,w,i]` (split i witness) and `s[A,B,C,w]` (rule + split witness).

Clauses: |w|=1: d[A,c] ↔ t[A,c]. |w| ≥ 2: d[A,w] → ⋁_{B,C} s[A,B,C,w]; s → r[A,B,C];
s → q[B,C,w]; r[A,B,C] ∧ q[B,C,w] → d[A,w]; q → ⋁_i p_i; p_i → d[B,u_i]; p_i → d[C,v_i];
d[B,u_i] ∧ d[C,v_i] → q. Because derivability of w in CNF depends only on strictly shorter
words, these clauses force d to coincide with CYK semantics (induction on |w|), so the
encoding is exact (no spurious fixpoints). Target: unit clauses ±d[S,w] for all constrained w.

**Symmetry breaking (proved WLOG).** Lemma: if a CNF grammar with k nonterminals satisfies
the constraint, so does one with ≤ k nonterminals in which the non-start nonterminals have
pairwise distinct, nonempty languages restricted to Σ^{<n}. Proof: non-start nonterminals
are only used on proper factors of words of length ≤ n, i.e. on lengths ≤ n−1. If two
non-start B, C have L(B)∩Σ^{<n} = L(C)∩Σ^{<n}, replace C by B in every right-hand side; by
induction on m ≤ n, L(X)∩Σ^m is unchanged for every X (a split of a length-m word uses
factors of length < m ≤ n where B and C agree). Now C is unreachable and can be deleted
(fewer nonterminals); likewise a non-start nonterminal with empty truncated language is
useless. ∎ Hence we impose that the 0/1 vectors (d[X,w])_{|w|<n} for X = 1..k−1 are
**strictly lex-decreasing** (standard prefix-equality chain encoding). Since every
solvable instance has a solution of ≤ k nonterminals satisfying this, and k is searched
upward from the previous lower bound, the first SAT k is the exact minimum.

Search: `le` mode starts at k_≤(T,n−1) (valid lower bound); `eq` mode starts at 1.
Timeout 2400 s per (T,mode,n,k) instance; a timeout stops that series (entry "≥k").
**Every SAT grammar was re-verified independently** by `verify.py`, which recomputes the
language of the returned grammar with the bitset DP of `check_grammar.py` (a different
algorithm, itself cross-checked against Earley on 300 random grammars) and compares with
the target on the constrained lengths: all verified, 0 failures. UNSAT answers are
CaDiCaL's word (no DRAT proof check was run) — treat lower bounds as solver-certified only.

### 2.3 Results

**mode le** (L(G)∩Σ^{≤n} = T∩Σ^{≤n})

| T \ n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | – |
| NS | 1 | 3 | 3 | 5 | 5 | 6 | 6 | 6 | 6 | 6 | 6 |
| NC | 1 | 1 | 3 | 4 | 4 | 6 | 6 | 6 | ≥7 | – | – |
| NSC | 1 | 3 | 3 | 4 | 5 | 7 | 7 | 7–8 | – | – | – |
| Q | 1 | 3 | 3 | 4 | 4 | 6 | 7 | 7 | 7–8 | – | – |

**mode eq** (L(G)∩Σ^n = T∩Σ^n)

| T \ n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | – |
| NS | 1 | 2 | 1 | 3 | 1 | 5 | 1 | 5 | 1 | ≥5 | – |
| NC | 1 | 1 | 2 | 1 | 1 | 3 | 1 | 1 | ≥5 | – | – |
| NSC | 1 | 2 | 2 | 3 | 1 | 5 | 1 | 5 | ≥5 | – | – |
| Q | 1 | 2 | 2 | 3 | 2 | 5 | 2 | 5 | ≥5 | – | – |

Hardest instances (solve time s):
- NC eq n=9 k=4: False in 1037.44s (175422 vars, 488824 clauses)
- NC le n=9 k=6: False in 3133.38s (428916 vars, 1206510 clauses)
- NS eq n=8 k=4: False in 150.84s (79422 vars, 219512 clauses)
- NS eq n=8 k=5: True in 2640.08s (129926 vars, 361184 clauses)
- NS eq n=10 k=4: False in 1892.95s (383806 vars, 1076600 clauses)
- NS le n=10 k=6: True in 59.41s (932212 vars, 2636526 clauses)
- NS le n=11 k=6: True in 427.34s (2012532 vars, 5717742 clauses)
- NSC eq n=8 k=4: False in 147.61s (79422 vars, 219512 clauses)
- NSC eq n=8 k=5: True in 1980.32s (129926 vars, 361184 clauses)
- NSC eq n=9 k=4: False in 987.28s (175422 vars, 488824 clauses)
- NSC le n=8 k=8: True in 6224.9s (379130 vars, 1066726 clauses)
- Q eq n=8 k=4: False in 153.63s (79422 vars, 219512 clauses)
- Q eq n=8 k=5: True in 2127.07s (129926 vars, 361184 clauses)
- Q eq n=9 k=4: False in 1192.64s (175422 vars, 488824 clauses)
- Q le n=7 k=6: False in 62.74s (88308 vars, 244590 clauses)
- Q le n=8 k=7: True in 1131.01s (278262 vars, 780382 clauses)
- Q le n=9 k=8: True in 7214.15s (825338 vars, 2335718 clauses)

Legend: a number = exact minimum (SAT at k, solver-UNSAT at k−1 or k−1 below the monotone
lower bound); `a–b` = UNSAT below a proved/timeout at a, SAT at b; `≥a` = solver UNSAT for
all k < a, timeout at a; `–` = not attempted. Timeouts: 2400 s solver interrupt (some UNSAT
answers arrived slightly after it), hard 3600 s wall limit per instance. The extra upper
bounds Q le n=9 ≤ 8 and NSC le n=8 ≤ 8 were run separately with a 3000 s+ budget (they took
7214 s and 6225 s — the interrupt was not honoured promptly by CaDiCaL during preprocessing).
NS le n = 11: k = 6 (SAT, 2.0M variables, 427 s; the lower bound 6 comes from n = 10).

Example (file `campaign/tools/examples/sat_Q_le8_k7.txt`): the SAT-found 7-nonterminal CNF
grammar for Q ∩ Σ^{≤8},
```
N0 -> a | b | N2 N3 | N2 N5 | N2 N6 | N3 N2 | N3 N6 | N4 N6 | N5 N2 | N6 N2 | N6 N3 | N6 N4
N1 -> a | N2 N2 | N3 N2 | N4 N2 | N6 N3
N2 -> a          N3 -> b
N4 -> N2 N1 | N2 N2 | N3 N3 | N3 N5
N5 -> N2 N3 | N3 N3 | N4 N3 | N6 N2
N6 -> N2 N5 | N3 N1
```
`check_grammar.py --N 12` on it: exact at lengths ≤ 8 and also at 10, 11; it accepts the 6
cubes (aab)³-type at length 9 and 12 non-primitive words at length 12 (first:
`aabaabaab, abaabaaba, abbabbabb, …`); no false negatives. Typical behaviour of
truncation-optimal grammars: they encode the finitely many periods relevant below n.


### 2.4 Reading of the table (honest)

* **Not distinguishable.** For n ≤ 9, Q ∩ Σ^{≤n} = NSC ∩ Σ^{≤n} minus the unary words a⁵, b⁵,
  a⁷, b⁷ (a word ρᵉ with ρ primitive is a square iff 2|e and a cube iff 3|e, so the non-primitive
  NSC words are exactly ρᵉ with e ≥ 5, gcd(e,6)=1; the first non-unary one is (ab)⁵, length 10). So within the
  feasible range the SAT experiment compares Q with NSC up to a regular (unary) correction;
  it cannot "see" the unboundedly many prime exponents, which is precisely the feature that
  would make Q non-CF. The non-squares (a CF language) reach 6 nonterminals at n = 6 and stay
  there through n = 11; the non-cubes (also CF) need ≥ 7 at n = 9; Q and NSC are both at 7
  for n = 7 and 8 (NSC: 7–8 at n = 8), Q is 7–8 at n = 9. Note that NC (a CF language)
  grows as fast as Q in this window — growth at n ≤ 9 says nothing. Differences of ±1 at these n
  reflect small-length coincidences (e.g. at n = 6, Q needs 6 but NSC needs 7; a plausible
  but unverified explanation is that Q also excludes a⁵,b⁵, so "no unary word of length ≥ 2"
  becomes a uniform rule).
* Exact-length slices behave very differently from the ≤n truncations: for prime n,
  k_=(Q,n) = 2 (Σⁿ minus aⁿ, bⁿ) and for n not divisible by 2 (resp. 3), k_=(NS,n) = 1
  (resp. k_=(NC,n)=1). The hard slices are the composite n, where k_=(Q,n) = k_=(NS,n) =
  k_=(NSC,n) = 5 for n = 6 and n = 8; at n = 9 Q, NSC and NC are ≥ 5 (timeout at 5), NS at
  n = 10 is ≥ 5. Up to the reach, k_=(Q,n) equals k_=(NSC,n) whenever both are known, except
  primes n ≥ 5 where Q has to exclude aⁿ, bⁿ (2 vs 1).
* Cost: the hard instances (le n = 8–9, eq n = 8–10) have 10⁵–10⁶ variables; UNSAT at
  k = 6–7 takes ~20–50 min (NC le n=9, k=6: 3133 s) and k = 7 at n = 9 times out. Pushing to n ≥ 10–15, where Q and NSC
  first differ non-trivially ((ab)⁵, (ba)⁵ at length 10; then a¹¹; (aab)⁵-type at 15; …), would need a
  much better encoding (e.g. incremental, or restricting to grammars of a structured shape).
  **Recommendation:** do not invest more in this route; even a large table cannot refute or
  confirm CF-ness, and the regime where Q differs from the CF comparators starts exactly
  where SAT becomes infeasible.

---------------------------------------------------------------------------------------------

## 3. Generic tester: `campaign/tools/check_grammar.py`

```
python3 campaign/tools/check_grammar.py GRAMMAR_FILE [--N 20] [--alphabet ab] [--start S]
        [--target Q|NS|NC|NSC] [--show 10] [--long 21-30 --samples 200 --seed 0]
        [--word w1 w2 ...]
```
Grammar file: lines `S -> A B | a | eps` (`#` comments; nonterminals = symbols that occur as
some LHS; any other token is a terminal string split into letters, e.g. `ab B`; ε =
`eps`/`ε`/empty alternative). Any CFG form (ε-rules, unit rules, long RHS, useless symbols).

What it does:
1. **Exact** computation of L(G) ∩ Σ^m for all m ≤ N by bitset dynamic programming
   (each nonterminal ↦ boolean array over Σ^m in lexicographic order; a binary rule
   A→BC contributes `outer(L_B[i], L_C[m−i]).ravel()`; same-length dependencies from
   unit rules and nullable symbols resolved by a monotone fixpoint per length). Prints
   per length |L∩Σ^m|, |T∩Σ^m|, #(L∖T), #(T∖L), and the first counterexamples on each side
   in shortlex order, plus ε-membership. N = 20 over {a,b} takes well under a second for
   small grammars, ~2 MB per (binarised) nonterminal.
2. `--long A-B`: Earley recognizer on **all** non-primitive words of each length in [A,B]
   (only O(2^{m/2}) of them) and on random primitive words.
3. `--word`: Earley membership for given words.
Exit code 0 iff no discrepancy. Python API: `parse_grammar`, `check`, `language_bitsets`,
`earley`, `target_mask` (see the module docstring).

Validation: bitset DP vs Earley agree on all words of length ≤ 7 for 300 random grammars
with ε/unit/long rules (0 mismatches). On the classical non-square grammar
(`tools/examples/nonsquares.txt`) it reports exact agreement with NS for all lengths ≤ 20,
and against Q it reports the expected false positives
`aaa, bbb, aaaaa, bbbbb, ababab, bababa, aaaaaaa, …, aabaabaab` and 38 non-primitive
words accepted at length 15 under `--long 15-16`.

---------------------------------------------------------------------------------------------

## 4. Sanity data for the "rotation of a CF set" route

Route: find a CF language P ⊆ Q meeting every primitive conjugacy class; then
Q = Cyc(P) is CF (cyclic shift preserves CF). Necessary: (i) **soundness** P ⊆ Q;
(ii) **coverage** every class meets P. (Note: P = Q itself would do, so a sound+complete
CF P is exactly as hard as the problem; the data only shows how far natural candidates are.)

Candidates (class covered iff some rotation satisfies P; soundness checked on all
non-primitive words of length ≤ 20):

* P1 linear "unique longest a-run";
* P2 linear "b aᵏ b occurs exactly once, k = max a-run";
* P3 cyclic "unique longest cyclic a-run" (word contains b) — rotation-invariant;
* P4 P3 or the same for b;
* P5 `aᵏ b v` with |v|_a < k — **context-free** (one counter) and sound;
* P6 P5 ∪ mirror(P5) — CF, sound;
* P7 gcd(|w|_a, |w|_b) = 1 — rotation-invariant, sound, not CF (non-semilinear Parikh set);
* P8 P4 ∨ P7.

Soundness proofs (P3–P8): if w = uᵐ, m ≥ 2, contains both letters, every cyclic a-run of w
occurs ≥ m times, so no cyclic run is uniquely longest (P3, P4); P5 forces a cyclic a-run of
length ≥ k with all other a's (< k of them) outside it, so the max cyclic run is unique
(⇒ P3); P7: |uᵐ|_a = m|u|_a and |uᵐ|_b = m|u|_b.

Coverage = #classes (Lyndon words of length n) having a rotation in P, with percentage.

| n | classes | P1 | P2 | P3 | P4 | P5 | P6 | P7 | P8 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2 | 1 (50.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 2 (100.0%) | 2 (100.0%) |
| 2 | 1 | 1 (100.0%) | 0 (0.0%) | 1 (100.0%) | 1 (100.0%) | 1 (100.0%) | 1 (100.0%) | 1 (100.0%) | 1 (100.0%) |
| 3 | 2 | 2 (100.0%) | 1 (50.0%) | 2 (100.0%) | 2 (100.0%) | 2 (100.0%) | 2 (100.0%) | 2 (100.0%) | 2 (100.0%) |
| 4 | 3 | 3 (100.0%) | 2 (66.7%) | 3 (100.0%) | 3 (100.0%) | 3 (100.0%) | 3 (100.0%) | 2 (66.7%) | 3 (100.0%) |
| 5 | 6 | 5 (83.3%) | 5 (83.3%) | 5 (83.3%) | 6 (100.0%) | 5 (83.3%) | 6 (100.0%) | 6 (100.0%) | 6 (100.0%) |
| 6 | 9 | 8 (88.9%) | 8 (88.9%) | 8 (88.9%) | 9 (100.0%) | 8 (88.9%) | 9 (100.0%) | 2 (22.2%) | 9 (100.0%) |
| 7 | 18 | 15 (83.3%) | 16 (88.9%) | 14 (77.8%) | 18 (100.0%) | 13 (72.2%) | 16 (88.9%) | 18 (100.0%) | 18 (100.0%) |
| 8 | 30 | 26 (86.7%) | 27 (90.0%) | 24 (80.0%) | 28 (93.3%) | 21 (70.0%) | 25 (83.3%) | 16 (53.3%) | 30 (100.0%) |
| 9 | 56 | 49 (87.5%) | 51 (91.1%) | 43 (76.8%) | 56 (100.0%) | 34 (60.7%) | 44 (78.6%) | 38 (67.9%) | 56 (100.0%) |
| 10 | 99 | 88 (88.9%) | 90 (90.9%) | 77 (77.8%) | 92 (92.9%) | 55 (55.6%) | 70 (70.7%) | 26 (26.3%) | 94 (94.9%) |
| 11 | 186 | 166 (89.2%) | 169 (90.9%) | 140 (75.3%) | 180 (96.8%) | 89 (47.8%) | 122 (65.6%) | 186 (100.0%) | 186 (100.0%) |
| 12 | 335 | 304 (90.7%) | 307 (91.6%) | 256 (76.4%) | 313 (93.4%) | 144 (43.0%) | 196 (58.5%) | 134 (40.0%) | 323 (96.4%) |
| 13 | 630 | 572 (90.8%) | 576 (91.4%) | 472 (74.9%) | 598 (94.9%) | 233 (37.0%) | 338 (53.7%) | 630 (100.0%) | 630 (100.0%) |
| 14 | 1161 | 1061 (91.4%) | 1065 (91.7%) | 874 (75.3%) | 1086 (93.5%) | 377 (32.5%) | 546 (47.0%) | 340 (29.3%) | 1104 (95.1%) |
| 15 | 2182 | 1998 (91.6%) | 2003 (91.8%) | 1628 (74.6%) | 2050 (94.0%) | 610 (28.0%) | 932 (42.7%) | 1056 (48.4%) | 2118 (97.1%) |
| 16 | 4080 | 3740 (91.7%) | 3745 (91.8%) | 3045 (74.6%) | 3813 (93.5%) | 987 (24.2%) | 1510 (37.0%) | 2048 (50.2%) | 3947 (96.7%) |
| 17 | 7710 | 7064 (91.6%) | 7070 (91.7%) | 5719 (74.2%) | 7204 (93.4%) | 1597 (20.7%) | 2554 (33.1%) | 7710 (100.0%) | 7710 (100.0%) |
| 18 | 14532 | 13317 (91.6%) | 13323 (91.7%) | 10780 (74.2%) | 13553 (93.3%) | 2584 (17.8%) | 4144 (28.5%) | 4490 (30.9%) | 13859 (95.4%) |
| 19 | 27594 | 25252 (91.5%) | 25259 (91.5%) | 20388 (73.9%) | 25718 (93.2%) | 4181 (15.2%) | 6954 (25.2%) | 27594 (100.0%) | 27594 (100.0%) |
| 20 | 52377 | 47892 (91.4%) | 47899 (91.5%) | 38674 (73.8%) | 48775 (93.1%) | 6765 (12.9%) | 11290 (21.6%) | 24664 (47.1%) | 50463 (96.3%) |

Soundness (first non-primitive words satisfying P, lengths <= 20):
- P1 unique longest a-run (linear): ['aa', 'aaa', 'aaaa', 'aaaaa', 'aaaaaa', 'abaaba']
- P2 b a^k b once, k=max a-run (linear): ['abab', 'baba', 'aabaab', 'abaaba', 'abbabb', 'baabaa']
- P3 unique longest cyclic a-run: none (sound up to this length)
- P4 unique longest cyclic a-run or b-run: none (sound up to this length)
- P5 a^k b v, |v|_a<k  [CF]: none (sound up to this length)
- P6 P5 or mirror  [CF]: none (sound up to this length)
- P7 gcd(|w|_a,|w|_b)=1: none (sound up to this length)
- P8 P4 or P7: none (sound up to this length)

Smallest-n uncovered class (Lyndon representative) per property, n in {8,12,16,20}:
- P1 unique longest a-run (linear): {8: 'abababbb', 12: 'aabaabaababb', 16: 'aaaabaaaabaaaabb', 20: 'aaaaabaaaaabaaaaabab'}
- P2 b a^k b once, k=max a-run (linear): {8: 'aaaaaaab', 12: 'aaaaaaaaaaab', 16: 'aaaaaaaaaaaaaaab', 20: 'aaaaaaaaaaaaaaaaaaab'}
- P3 unique longest cyclic a-run: {8: 'aabaabab', 12: 'aaaabaaaabab', 16: 'aaaaaabaaaaaabab', 20: 'aaaaaaaabaaaaaaaabab'}
- P4 unique longest cyclic a-run or b-run: {8: 'aabaabab', 12: 'aaaabaaaabab', 16: 'aaaaaabaaaaaabab', 20: 'aaaaaaaabaaaaaaaabab'}
- P5 a^k b v, |v|_a<k  [CF]: {8: 'aabaabab', 12: 'aaaabaaaabab', 16: 'aaaaaabaaaaaabab', 20: 'aaaaaaaabaaaaaaaabab'}
- P6 P5 or mirror  [CF]: {8: 'aabaabab', 12: 'aaaabaaaabab', 16: 'aaaaaabaaaaaabab', 20: 'aaaaaaaabaaaaaaaabab'}
- P7 gcd(|w|_a,|w|_b)=1: {8: 'aaaaaabb', 12: 'aaaaaaaaaabb', 16: 'aaaaaaaaaaaaaabb', 20: 'aaaaaaaaaaaaaaaaaabb'}
- P8 P4 or P7: {8: None, 12: 'aaaabaaaabab', 16: 'aaaaabaaaaababab', 20: 'aaaaaaabaaaaaaababab'}

Observations (evidence):
* P1, P2 are **unsound** already at length 4–6: `abaaba` = (aba)² has a unique longest
  linear a-run; `abab` has a unique `b aᵏ b`. The linear "unique run" ideas must be
  replaced by cyclic ones (or by a normal form `aᵏ b v` with all a-runs of v < k).
* Sound run-based normal forms (P3/P4) sit at ≈74% / ≈93% of classes for n = 12..20 (slowly
  decreasing) and do not approach 100%; the uncovered classes are the "(aᵏb)ʲ-with-defect" families, e.g. `aaaabaaaabab`,
  `aaaaaaaabaaaaaaaabab` — runs repeated, primitivity witnessed only by a small defect far
  from the long runs. Any CF normal form must handle exactly these: it has to compare long
  blocks for *equality-with-a-defect*, which is the non-p-th-power check again.
* The genuinely CF sound candidates (P5, P6) have coverage decaying roughly geometrically
  (P5: 13% of classes at n = 20; looks like a Fibonacci count F_{n}: 1597, 2584, 4181, 6765
  at n = 17..20 — exact Fibonacci numbers, an observed pattern, not proved here).
* Shortest cyclically-unique factor (a once-occurring cyclic factor certifies primitivity;
  table below): the max over classes is ⌊n/2⌋ for 2 ≤ n ≤ 20 (attained by two-block words
  aⁱ b aʲ b, e.g. a¹⁰ b a⁸ b at n = 20), the mean is small (≈3.2 at n = 20, growing slowly,
  consistent with ~log n). So "guess a uniquely occurring factor"
  certificates are short on average but linear in the worst case — and verifying
  uniqueness of a factor is not a CF operation in general.

s(w) = least L such that some cyclic factor of length L occurs exactly once in the cyclic word of w.

| n | classes | max s(w) | max s/n | mean s(w) | a maximiser |
|---|---|---|---|---|---|
| 2 | 1 | 1 | 0.50 | 1.00 | ab |
| 3 | 2 | 1 | 0.33 | 1.00 | aab |
| 4 | 3 | 2 | 0.50 | 1.33 | aabb |
| 5 | 6 | 2 | 0.40 | 1.67 | aaabb |
| 6 | 9 | 3 | 0.50 | 2.00 | aaabab |
| 7 | 18 | 3 | 0.43 | 2.11 | aaaabab |
| 8 | 30 | 4 | 0.50 | 2.40 | aaaabaab |
| 9 | 56 | 4 | 0.44 | 2.46 | aaaaabaab |
| 10 | 99 | 5 | 0.50 | 2.65 | aaaaabaaab |
| 11 | 186 | 5 | 0.45 | 2.68 | aaaaaabaaab |
| 12 | 335 | 6 | 0.50 | 2.81 | aaaaaabaaaab |
| 13 | 630 | 6 | 0.46 | 2.81 | aaaaaaabaaaab |
| 14 | 1161 | 7 | 0.50 | 2.93 | aaaaaaabaaaaab |
| 15 | 2182 | 7 | 0.47 | 2.93 | aaaaaaaabaaaaab |
| 16 | 4080 | 8 | 0.50 | 3.00 | aaaaaaaabaaaaaab |
| 17 | 7710 | 8 | 0.47 | 3.05 | aaaaaaaaabaaaaaab |
| 18 | 14532 | 9 | 0.50 | 3.11 | aaaaaaaaabaaaaaaab |
| 19 | 27594 | 9 | 0.47 | 3.14 | aaaaaaaaaabaaaaaaab |
| 20 | 52377 | 10 | 0.50 | 3.21 | aaaaaaaaaabaaaaaaaab |

---------------------------------------------------------------------------------------------

## 5. Bottom line
All of this is evidence. (1) Counts verified. (2) Minimum CNF sizes of truncations of Q
track those of NSC/NS (5–7 nonterminals at n ≤ 7–9) and cannot distinguish Q from CF
comparators in the feasible range, because Q and NSC differ only on unary words below
length 10. (3) A tested, documented grammar checker is available for other agents.
(4) Natural sound normal forms for the rotation route cover ≤ ~93% of classes (cyclic-run
based, non-CF) or a vanishing fraction (CF ones, Fibonacci-many); the uncovered families
(aᵏb)ʲ·(small defect) are exactly the hard "near-power" words.
