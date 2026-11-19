# poly_AG: constructive near-grammars (Task G) and slice witness grammars (Task A)

## Task G
**[searched]** `walk.md` / `builder3.md` exist nowhere in the working tree, in any branch, in deleted git history,
or elsewhere on the filesystem. Their grammars could not be implemented. As substitutes I used the repo's only explicit
near-grammars: G_A = coPow_2 (`scripts/devil/copow_grammar.py`, k=2), and G_B = length dispatch
(n even → M_2; n odd with 3|n → M_3 ∩ odd length via Bar-Hillel; n ≡ ±1 mod 6 → non-constant words).
Script: `scripts/poly/ag_near.py` (generic exact tree counter plus Bar-Hillel in `ag_common.py`).

[computational] The tree counts match these closed forms on every word with |w| ≤ 12 and on 300 random words with |w| ≤ 22:
amb_A(w) = #{i < n/2 : w_i ≠ w_{i+n/2}} for even n, and 1 for odd n.
amb_B(w) = mism_2 (n even), mism_3 (n odd, 3|n), 1 or 0 otherwise.

| grammar | smallest words in L(G) Δ Q | count of L Δ Q, n ≤ 12 | max amb at length n (n ≤ 24; exhaustive to 20) | extremal word |
|---|---|---|---|---|
| G_A | aaa, bbb (non-square powers) | 32 | n/2 (n even), 1 (n odd) | a^{n/2} b^{n/2} |
| G_B | a, b; ababab (cube, not square) | 18 | n/2 (n even), 2n/3 (n odd, 3|n), 1 otherwise | a^{n/3} b^{n/3} a^{n/3} |

The growth is linear (degree 1). There is no exponential term.

## Task A: witness-union grammars for Q_n = Q ∩ (ab*)^n, with n fixed
For each prime p | n, a certificate is a block pair (i, j) with j − i = n/p ("adj"), or j ≡ i mod n/p ("cls"),
and e_i ≠ e_j. A CF gadget b^x[..]b^y with x ≠ y (unique parse) realizes a system of one certificate per prime
when the pairs are laminar: disjoint or strictly nested, with all endpoints distinct.
amb(w) = #laminar systems. This count does not depend on the exponent sizes.
Script: `scripts/poly/ag_slice.py n1,n2,.. V mode`.

| n | primes | uncovered primitive patterns (V=2) adj / cls | max amb adj / cls |
|---|---|---|---|
| p ∈ {2,3,5,7,11,13} | 1 | 0 / 0 | n−1 / ⌊n²/4⌋ |
| 4, 8, 9, 16 | 1 | 0 / 0 | n − n/p / same |
| 6 | 2, 3 | 27/27 (all; V=3: 116/116) | 0 / 0 |
| 10 | 2, 5 | 21 / 20 (V=3: 47/45) | 14 / 16 |
| 12 | 2, 3 | 240 / 180 | 7 / 8 |
| 14 | 2, 7 | 28 / 28 | 44 / 56 |
| 15 | 3, 5 | 39 / 15 | 52 / 70 |

[computational, plus a one-line proof] For a single-defect vector (all e_k equal except one), every certificate has the defect block
as an endpoint. With ≥ 2 primes, certificates therefore always share an endpoint, so they are never laminar.
All single-defect words are uncovered for every n with ≥ 2 distinct primes.
Other uncovered families:
- n = 2·odd: period-2 vectors with a local swap, e.g. 0010101101 and 00101010110101.
- n = 12: double defects such as 0^9 101.

Where the construction breaks: the failure is not a growth in ambiguity. For prime-power n, ambiguity stays bounded per n
(linear adj, quadratic cls). Language coverage fails instead, exactly on words that need one block compared
against two others, e.g. {b^x..b^y..b^z : y ≠ x, y ≠ z}. That is the 3-way crossing that KK theory has to avoid by other means.
