# S4S — SAT synthesis of small CNF grammars agreeing with Q up to length L [computational]

**Claim.** Minimal CNF grammars (start S, N nonterminals) that agree with Q (primitive words over {a,b}) on all
words of length ≤ L exist only for very small L: L grows by about one per extra nonterminal. Small grammars
do **not** follow Q for long. The finite language Q∩Σ^{≤L} needs N ≳ L, and the SAT search found no cheap structure.

**Method.** `scripts/poly/s4s_sat_grammar.py` uses pysat (CaDiCaL 1.5.3) with CEGAR. The CYK derivability vars D(u,A) are created lazily, only
for substrings of sampled words, with an exact encoding (h = split conjunction, g = "u ⇒ BC", f = rule∧g).
Each candidate is checked by exact vectorised CYK on **all** words of length ≤ L+2, and any disagreements are added to the sample.
UNSAT on a sample means UNSAT overall, so the UNSAT rows are certified lower bounds. The search uses no symmetry breaking.

| N | max L with agreement | status at L+1 | first disagreement of found grammar |
|---|---|---|---|
| 1–2 | 0 | UNSAT at L=1 | — |
| 3 | 3 | UNSAT (L=4) | len 4: abab, baba accepted |
| 4 | 5 | UNSAT (L=6) | len 6: aabaab, ababab, … (8 words) |
| 5 | 5 | UNSAT (L=6) | len 6: same 8 words |
| 6 | ≥6 | L=7 solve timed out (>200 s) | len 7: abababa, bababab, … (6) |
| 7 | ≥7 | L=8 solve timed out (>200 s) | len 8: aaabaaab, aabbaabb, … (12) |

**Best grammars** (unused nonterminals can occur):
```
N=4 (L=5): S->AB|AC|BA|CA|CB|a|b  A->AA|CB|a  B->AC|BB|BC|CA|b  C->BA|BC|CA|CC
N=6 (L=6): S->AE|BE|CD|DC|EB|a|b  A->AC|a  B->AA|AE|DA|EA|a  C->AC|AE|CE  D->BA|DA|EB|ED|a|b  E->CE|b
N=7 (L=7): S->AF|BC|CB|CD|DC|a|b  A->AC|BA|BC  B->BA|b  C->AC|a  D->BB|BC|CB|DA|FA|FB|b
           E->AB|AC|CA|EC|a|b  F->CD|CF|EB|FB|a|b
```
**Ambiguity** (max / mean number of derivation trees on the Q-words of each length):
- N=4: 1,1,2,6,19 (len 1–5).
- N=6: 1,2,4,7,24,53.
- N=7: 1,2,3,7,17,51,120 (mean 18.2 at length 7).

The ambiguity grows roughly exponentially. The found grammars are highly ambiguous.

**Structure.** The grammars reject a^n and b^n with "contains both letters" machinery: they derive ab or ba
somewhere, using chains such as A→AC|a and C→AC|a. They then patch the few short powers (abab, (ab)^3, (aab)^2) one at a time.
Every failure comes from **squares/powers of length L+1**, which the grammar has not learned: it either accepts a new power
or loses a primitive neighbour such as abababa. None of the grammars has a generalising mechanism.

**Status.** EXPLORATORY / negative for "small grammars follow Q unusually far". The values L(3)=3, L(4)=L(5)=5 are certified.
The values for N=6 and N=7 are lower bounds, because the solver timed out on the next length.
The results come from short runs (about 3 min per N) and do not bear on whether Q is context-free.
Reproduce: `python3 scripts/poly/s4s_sat_grammar.py NMIN NMAX LMAX TIMEOUT TOTAL` (e.g. `3 5 14 30 90`).
