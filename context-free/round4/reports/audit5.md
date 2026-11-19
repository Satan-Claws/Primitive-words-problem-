# audit5: adversarial audit of walk.md (claimed refutation of (Q½))

**Bottom line.** I could not break the headline. The claim that (Q½) is false is **CONFIRMED**: T(E′) is a CF subset of Q with |T(E′)_n| ≥ c·2^n·n^{-1/4} for all odd n. Every proof step was re-derived by hand. Every numerical claim was re-checked with my own scripts, which share no code with walk's.

Defects found:
- one wrong constant (a factor of 2);
- one informal phrasing;
- the T^k density claim is not rigorous as written. The exact identity in §4 below closes most of that gap.

**No resolution of "Q CF?" is claimed by walk, and none by me.**

Scripts are in `context-free/round4/scripts/audit5/`:

| Script | What it does |
|---|---|
| `brute.py` | Exhaustive check of E′, T, T², T³ and G for n ≤ 20, by decoding each word independently. Also a random-word check of rotation invariance. |
| `literal.py` | Builds T(E′) literally (substitute, then rotate, then swap) and compares it with the decoding test, n ≤ 14. |
| `exact.py` | Exact big-integer counts of T^k(E′) via a (length, #b) recursion. |
| `flt.py` | Float version of the same recursion for large n. It truncates D ≤ 12√n, so its values are lower bounds. |
| `avg.py` | Tests the averaging step of walk §3. |
| `gcount.py` | Closed-form counts for G. |

## 1. The T-operator lemma

### Lemma 1 (unique first-passage decomposition): CONFIRMED

- The pieces end exactly at the first-passage times to levels 1..D.
- Conversely, a concatenation of pieces reaches a new maximum exactly at each piece end. So "concatenation of pieces" ⇔ "Δ = D ≥ 1 and the word ends at a strict maximum".

### Lemma 2 (CF closure): CONFIRMED

- **Substitution.** σ(a) = {a} and σ(b) = (nonempty Dyck, with b as the opening bracket)·a are CF. CF languages are closed under CF substitution (LITERATURE: Hopcroft–Ullman 1979, Thm 6.2).
- **Cyclic shift.** Cyc preserves CF (LITERATURE: A. N. Maslov, "Cyclic shift operation for languages", Probl. Inf. Transm. 9 (1973); T. Oshiba, "Closure property of the family of context-free languages under the cyclic shift operation", Electron. Commun. Japan 55 (1972); also Hopcroft–Ullman 1979, Ex. 6.4c).
- **Swap and union.** Swap is a homomorphism, and CF languages are closed under union.
- **Grammar.** The grammar for σ(E′) is correct. K generates the balanced words over {X,Y}, so S generates #X − #Y = ±1. W generates Dyck words with b opening, and Z = bWaW generates the nonempty ones.
- **Literal construction.** substitute → rotate → swap equals the decoding test for every n ≤ 14 (`literal.py`). For example, 6942 words at n = 13 by both methods.

### Lemma 3 (soundness): CONFIRMED

The proof only needs σ(M) ⊆ Q. Rotation and swap are then absorbed because Q is closed under both. So the rotation point never has to align with x's boundary inside the proof.

Re-derivation:
1. Take w = f_1⋯f_D ∈ σ(v), with v ∈ M ⊆ Q. Then D = |v| ≥ 1, and the f_j are the unique pieces.
2. Φ(w) = v exactly. This uses the exclusion of z = ε in σ(b), so piece types are unambiguous.
3. Suppose w = x^p with p ≥ 2, and let e = Δ(x) = D/p.
4. Then S_t < e for all t < d. Otherwise S_{t+(p−1)d} ≥ D at a time before n, which contradicts the strict maximum at the end.
5. So x is itself a concatenation of e pieces, and by uniqueness the decomposition of w is the same e pieces repeated p times.
6. Hence v = Φ(x)^p, a contradiction.

Edge cases:
- ε is excluded because M ⊆ Q.
- Δ = 0 never occurs in T(M).
- Words of Cyc σ(M) have Δ ≥ 1, and their swaps have Δ ≤ −1, so the union is disjoint.

### Rotation questions: CONFIRMED (needed only for counting and for the certificate description)

Take w with Δ = D > 0 and extend it periodically to a bi-infinite word.
- The rotations that end at a strict maximum correspond exactly to the strict record times of that walk, taken against the whole past. This is because S_{j−n} = S_j − D < S_j.
- There are exactly D of them in each period (cycle lemma).
- Consecutive record times bound the same cyclic sequence of pieces. So Φ is well defined up to rotation.

COMPUTER-CHECKED on 3000 random words of length ≤ 30: there are |Δ| canonical rotations, and all of them give Φ values that are rotations of one another.

The count |words with Δ = D| = (n/D)·|canonical words| follows by double counting pairs (word, canonical start). It does not need primitivity.

### Minor phrasing issue

"Directly, T(E′) is the set …" must be read as: swap first if Δ < 0. With that reading it is correct (`literal.py`).

## 2. Brute-force primitivity: CONFIRMED

`brute.py` checks every word of length n ≤ 20. It finds 0 non-primitive words in E′, T(E′), T²(E′), T³(E′) and G.

Densities of T, T², T³ at odd n agree exactly with `exact.py`. For example, n = 19 gives 0.8112, 0.9267 and 0.9500.

## 3. Exact formula and the n^{-1/4} lower bound

### Count formula: CONFIRMED

- N(k,m) = [y^m](C−1)^k = [y^{m−k}] C^{2k} = (2k/2m)·C(2m, m−k) = (k/m)·C(2m, m−k), using C − 1 = yC².
- The values of k are (D∓1)/2, and the factor 2 comes from the swap.
- The table is reproduced exactly (n = 101, 1001, 10001 give 0.6262, 0.4027, 0.2455). At n = 100001 the density is 0.1448, and density·n^{1/4} = 2.575.

### Lower bound: CONFIRMED

Restrict to odd D ∈ [√n, 2√n] and k = (D−1)/2. Then:
- k²/m ≤ ~2, so C(2m, m−k) ≥ c·4^m/√m;
- (n/D)·(k/m) ≍ 1;
- each term is ≍ 2^{D+2m}/√(Dm) = 2^n·n^{-3/4};
- there are ~√n/2 terms.

This gives c·2^n·n^{-1/4} for all large odd n. That already contradicts O(2^n n^{-1/2}).

### Wrong constant (cosmetic): GAP

walk writes (8/π)·2^{-3/4}·Γ(1/4) and gives its value as ≈ 2.74. Re-deriving with a Riemann sum (odd D, step 2) gives (4/π)·2^{-3/4}·Γ(1/4) = 2.745. The printed formula equals 5.49. So the numeric value is right and the symbolic constant is off by a factor of 2.

### "dense.md's CRH is false": CONFIRMED, conditionally

dense.md's argument is CRH + P^R ⇒ (Q½). So the refutation of CRH is only as good as Theorem P^R, which I did not audit.

## 4. T^k density

### T^k(E′) CF and ⊆ Q for every k: CONFIRMED

This follows by induction from Lemmas 2 and 3. Since T(E′) has only odd lengths, every T^k(E′) lives on odd n.

### Density ≍ n^{-2^{-(k+1)}}: GAP in rigor as written (outline only), but numerically confirmed and fixable

The outline's step "Φ uniform up to 1 + o(1)" is asserted, not proved.

I found the following **exact identity** (PROVED, by the same double count). For rotation-closed M and odd n,

    dens_{T(M)}(n) = Σ_D P(|Δ_n| = D) · μ_{D,m}(M_D),   with μ_{D,m}(v) ∝ N(#_b v, m), m = (n−D)/2.

This holds because Σ_v (n/D)·N(k_v, m) = C(n, m).

- Let ρ = dμ/dUnif.
- In the bulk k = D/2 ± D^{0.6}, with D ≤ n^{0.6}, ρ = 1 + o(1): log ρ varies by O(D^{1.6}/m) there.
- Outside the bulk, ρ ≤ e^{O(D²/m)}·poly(D), while the uniform mass is e^{−2D^{0.2}}.
- Together this gives dens_{T(M)}(n) ≍ E[dens_M(|Δ_n|)] whenever dens_M(D) ≍ D^{-α}.
- Combined with the local CLT bound P(|Δ_n| = D) ≤ C/√n, this gives α ↦ α/2.

This is a sketch at the same level as walk's. A written proof needs these tail estimates made explicit.

Numerical check (`avg.py`) of actual density against E[dens_M(|Δ_n|)]:

| k | n = 101 | n = 1001 | n = 10001 |
|---|---|---|---|
| 1 | .6262 vs .6065 | .4027 vs .3979 | .2455 vs .2445 |
| 2 | .8855 vs .8718 | .8024 vs .7985 | .6908 vs .6898 |

Exact (truncated, so lower-bound) densities set against walk's Monte Carlo:

| Level | n = 1001 | n = 10001 | n = 100001 |
|---|---|---|---|
| T² (MC .805 / .699 / .567) | 0.8024 | 0.6908 | 0.5733 |
| T³ (MC .927 / .901) | 0.9211 | 0.8980 | not computed |

All are within Monte Carlo error. The empirical decay is still pre-asymptotic: density·n^{1/4} for T is still rising toward 2.745.

## 5. Even-n variant G

- **Soundness: CONFIRMED.** Suppose a canonical word is x^p. Its piece sequence then has period e pieces, so Σg = p·(Σg over one period) = ±1 forces p = 1.
- **CF: CONFIRMED.** The piece classes A = a, B = ba·Dyck·a and C = bb…a are each CF. The type condition #A − 2#B = ±1 is one-counter. Then apply substitution, Cyc and swap.
- **Counts: COMPUTER-CHECKED.** The closed form uses generating functions yC for B and y²C³ for C, with count (n/D)·multinomial·[y^{m−β−2γ}] C^{β+3γ}. It matches brute force for every n ≤ 20; for example, n = 18 gives 0.2953.
- **Large n.** Density is 0.1621 at n = 1000, 0.1002 at n = 10000 and 0.0592 at n = 100000. density·n^{1/4} ≈ 0.91, 1.00, 1.05, consistent with n^{-1/4}.
- **Gap.** No proof of G's lower bound is written; it is COMPUTER-CHECKED only. It is not needed for refuting (Q½).
- **Not audited.** "T^k(E′ ∪ G) covers even n" is Monte Carlo only.

## Verdicts

| Claim | Verdict |
|---|---|
| Lemma 1 | CONFIRMED |
| Lemma 2 (citations correct) | CONFIRMED |
| Lemma 3 | CONFIRMED |
| Canonical rotation / Φ up to rotation | CONFIRMED |
| Grammar = certificate test | CONFIRMED (n ≤ 14 literal; proof above) |
| Exact formula | CONFIRMED |
| Lower bound c·2^n·n^{-1/4} (odd n) ⇒ **(Q½) FALSE** | CONFIRMED |
| Asymptotic constant | GAP (typo: 4/π, not 8/π; numeric 2.74 correct) |
| CRH false | CONFIRMED, conditional on P^R |
| T^k CF and ⊆ Q | CONFIRMED |
| T^k density exponent | GAP (outline). Exact identity + RN bound sketch supplied; numerically confirmed |
| G sound and CF | CONFIRMED |
| G density n^{-1/4} | COMPUTER-CHECKED only |

## Registry entry
1. **Aimed at:** breaking walk.md's refutation of (Q½).
2. **Proved:**
   - Independent re-derivation of Lemmas 1–3, the cycle-lemma count and the n^{-1/4} lower bound.
   - The exact identity dens_{T(M)}(n) = Σ_D P(|Δ_n| = D)·μ_{D,m}(M_D).
3. **Missing step:** explicit tail estimates for the T^k exponent (Section 4); a proof of G's lower bound.
4. **Counterexamples found:** none to walk's claims. One constant typo.
5. **Strength:** not applicable (audit). (Q½) being false kills only the polynomial-rate density route.
6. **What would reopen the route:** a flaw in Lemma 3 (I found none), or a reading of (Q½) restricted to even n. Even under that reading, G is a CF subset of Q at density ≈ n^{-1/4} (computer-checked only).
