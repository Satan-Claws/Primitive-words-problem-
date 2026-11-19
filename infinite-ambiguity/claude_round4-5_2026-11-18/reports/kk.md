# Agent "kk": report (bounded-language route, Q_n = Q ∩ (ab*)^n)

**I do not claim a proof of either resolution.** The main new result is a barrier, proved for every n. The
near-constant / one-scale pumping obstruction (bounded.md L6, finiteindex.md Lemma F) **never fires, for any n
and any positive direction h**. The obstruction is defeated by an explicit, uniform family of stratified
structures: the **(weighted) reflection matchings**. This turns bounded's computer checks C1 (n ≤ 30) and my
reruns (n = 42, 60) into one theorem with a two-line CRT proof.

Scripts: `infinite-ambiguity/claude_round4-5_2026-11-18/scripts/kk/` (`reflection_check.py`, `out_reflection.txt`; `near_constant.py` +
`arr2.py` copied from `scripts/bounded/`, with outputs `out_nc42.txt` and `out_nc60.txt`).

## 0. Notation and exact criterion

- n ≥ 2. For each prime p | n, let a_p = v_p(n), D = n/p, and V_D = {x ∈ Q^n : x_i = x_{i+D}} (indices mod n).
- E_n = N^n \ ∪_p V_{n/p}.
- (LITERATURE + PROVED in bounded.md L1/L2) Q_n is CF ⇔ E_n is a finite union of **stratified linear sets**
  c + N P. Here P is finite, and every p ∈ P has ≤ 2 nonzero coordinates. Crossing is forbidden: there are no
  p, p' ∈ P and i<j<k<l with p_i p_k p'_j p'_l ≠ 0.
- Note (PROVED, trivial): crossing of 2-sparse supports is a *cyclic* notion. Rotating coordinates maps
  stratified sets to stratified sets. So the "Cyc-closure" freedom (devil.md: some CF L ⊆ Q containing a
  conjugate of each primitive word suffices) gives **nothing new** on (ab*)^n slices.
- Hard region: B1 in devil.md shows E_n \ W_n is CF, where W_n = Σ_p V_{n/p}. So everything is about
  E_n ∩ W_n. In Fourier terms (ω = e^{2πi/n}), V_{n/p} is the set of vectors whose spectrum lies on the
  frequencies k ≡ 0 mod p. W_n is the set of vectors whose spectrum avoids the frequencies coprime to n.

**One-scale obstruction criterion (PROVED: bounded.md L6 for h = 1; finiteindex Lemma F; the general-h
version below has the same proof).** Let h ∈ Z_{>0}^n and D_h = {d ∈ D(n) : h ∈ V_d}. Let δ ∈ Z^n with
δ ∉ V_d for d ∈ D_h (so N h + Mδ ∈ E_n for N ≫ M). Suppose that for every stratified P_1 with h a strictly
positive rational combination of all of P_1, there is d ∈ D_h with δ ∈ span(P_1) + V_d. Then Q_n is not CF.

Proof: Dickson's lemma on N h + Mδ inside one piece gives P_1. Writing δ = Σ r_p p + v with v ∈ V_d and moving
along P_1 produces a point of V_d inside the piece. ∎

## 1. Theorem A: reflection escape (PROVED, every n)

For c ∈ Z_n, let ρ_c(i) = c − i (mod n), acting on vectors by (ρ_c x)_i = x_{c−i}. Define
P_c = {e_i + e_{c−i} : i ≠ c−i} ∪ {e_i : 2i ≡ c}.

- **P_c is stratified.** The chords {i, c−i} are parallel, so they split into two nested families on
  [0,c] and [c+1,n−1].
- **P_c contains 1.** 1 = Σ P_c up to the factor 1/2 on pairs.
- **span(P_c) = Sym_c := ker(1−ρ_c).**

**Lemma A1 (PROVED).** δ ∈ Sym_c + V_D ⇔ (1−ρ_c)δ ∈ V_D.

Proof.
- (⇒) ρ_c preserves V_D, because D | n.
- (⇐) v := (1−ρ_c)δ ∈ V_D is ρ_c-antisymmetric. So δ − v/2 ∈ Sym_c and v/2 ∈ V_D. ∎

**Lemma A2 (PROVED).** Let p | n be prime, D = n/p, and δ ∉ V_D. Then B_p := {c ∈ Z_n : (1−ρ_c)δ ∈ V_D} lies in
a single residue class mod p^{a_p}.

Proof.
1. Take c, c' ∈ B_p and put s = c'−c. Subtracting, (ρ_{c'} − ρ_c)δ ∈ V_D. Reindexing j = c−i gives
   w := τ_sδ − δ ∈ V_D, where (τ_sδ)_j = δ_{j+s}.
2. Suppose v_p(s) < a_p. Then g := gcd(s,n) divides D.
3. Put z_j = δ_{j+D} − δ_j. Then z_{j+s} − z_j = w_{j+D} − w_j = 0. So z is s-periodic and n-periodic, hence
   g-periodic, hence D-periodic.
4. Then 0 = δ_{j+pD} − δ_j = Σ_{t<p} z_{j+tD} = p·z_j. So z = 0, i.e. δ ∈ V_D. This is a contradiction.
5. Hence p^{a_p} | c'−c. ∎

**Theorem A (PROVED).** Let n ≥ 2, let 𝒫 be any set of primes dividing n, and let δ ∈ Q^n with δ ∉ V_{n/p} for
all p ∈ 𝒫. Then there is c ∈ Z_n with δ ∉ Sym_c + V_{n/p} for every p ∈ 𝒫.

Proof. By A2, each B_p avoids all but one class r_p mod p^{a_p}. By CRT, pick c ≢ r_p (mod p^{a_p}) for all
p ∈ 𝒫. By A1, c works. ∎

**Corollary A3 (PROVED).** For every n and every δ ∈ Z^n \ ∪_p V_{n/p}, there is c such that the stratified
linear set δ⁺ + N P_c lies in E_n. Here δ⁺ = δ + const·1 ≥ 0. This set contains all of N·1 + δ.

- Proof: if y = δ⁺ + s with s ∈ Sym_c lies in V_D, then (1−ρ_c)δ = (1−ρ_c)y ∈ V_D, a contradiction.
- Hence, **for every n and B**, the near-constant slab E_n ∩ {max − min ≤ B} is covered by finitely many
  stratified linear subsets of E_n.
- More precisely, x ∈ E_n is covered at level B iff some c has (1−ρ_c)x ∉ ∪_p V_{n/p} and
  ‖(1−ρ_c)x‖_∞ ≤ B. In words: x is primitive "relative to a reflection axis" and is near-symmetric about that
  axis.
- This replaces bounded's machine certificates C1 (n ≤ 30) by a uniform proof, and covers n = 210.

**Theorem B (PROVED): no one-scale obstruction exists for any positive direction h.**
Let h ∈ Z_{>0}^n be arbitrary and let δ satisfy δ ∉ V_d for d ∈ D_h.
1. Use the *weighted* reflection P_{c,h} = {h_i e_i + h_{c−i} e_{c−i}} ∪ {h_i e_i : 2i ≡ c}. It is stratified,
   with h = Σ P_{c,h} up to a factor, and span(P_{c,h}) = D_h·Sym_c (D_h is diagonal scaling by h).
2. For d ∈ D_h, scaling by the d-periodic h preserves V_d. So δ ∈ span(P_{c,h}) + V_d ⇔ h^{-1}δ ∈ Sym_c + V_d.
3. Apply Theorem A to h^{-1}δ with 𝒫 = {p : n/p ∈ D_h}. This gives a P_1 escaping every d ∈ D_h.

So the criterion of §0 is never satisfied. ∎ (h with zero entries was not treated; see §4.)

**Computer checks (COMPUTER-CHECKED, exact Fractions, `reflection_check.py`, output `out_reflection.txt`).**
The script asserts both A2 (single class mod p^{a_p}) and the existence of a good c.
- Exhaustive, h = 1: n = 6 with δ ∈ {0,1,2}^6, and n = 10, 12, 15 with δ ∈ {0,1}^n.
- Exhaustive, n = 6: three non-constant periodic h.
- Random hard δ ∈ W_n with h = 1 or random periodic h: n = 30, 42, 60, 210.
- No failures.
- Separately, bounded's arrangement search (random non-crossing matchings, exact verification) also kills
  the near-constant criterion at n = 42 (18 matchings) and n = 60 (14 matchings).

## 2. What an obstruction would now have to look like (task (a))

Any proof that some Q_n is not CF via Ginsburg must use a **genuinely multi-scale** family.

- The family is y = N h + M g + δ (N ≫ M ≫ 1) or a higher flag, where the second direction g is not
  absorbed. Concretely, h^{-1}g must have **no reflection axis c** that is simultaneously good (Thm A) for
  h^{-1}(Mg+δ).
- The argument must also exploit periods of the piece *outside* P_1 (the cone condition at the g-scale),
  which Lemma L6/F does not see.
- This matches bounded's C2: in the oriented two-scale model the coverer must orient witnesses, and the
  restricted strategy already fails for 72/720 orders at n = 6, although Q_6 is CF.
- So a two-scale criterion must be strictly weaker than "restricted coverer fails". I did not formulate one
  with a proof.

(IDEA) The natural next lemma would be a flag version of L6. If P_1 ⊆ P_2 are the period sets used at
scales N and M, the escape must be δ ∉ span(P_2) + V_d with g ∈ relint cone(P_2) mod span(P_1). The coverer
now chooses a pair (reflection for h, structure for g) that must not cross. The reflection chords for h are
all parallel to one axis, so g-periods must nest in the two nested families. Whether this is always possible
is exactly the open combinatorial core. I see no CRT-type argument for it.

## 3. Status of tasks (b), (c)

**(b)** No general KK proof and no counterexample.
- Theorem A gives the near-symmetric part of E_n uniformly.
- A full KK proof would need to cover points far from every reflection-symmetric vector, i.e. with
  ‖(1−ρ_c)x‖ unbounded for every good c. That needs extra non-crossing periods supported where x is
  asymmetric.
- Evidence keeps pointing to KK being TRUE: every one-scale obstruction is now provably dead for all n.

**(c)** Other bounded slices. The same arguments apply to any slice whose non-primitivity locus is a union of
"cyclic period" subspaces V_d of a block-length vector:
- (a^+b^+)^n with both exponent vectors;
- slices with fixed separators a^{e_i}. Here fixing e kills some V_d outright, so 𝒫 shrinks and Theorem A
  still applies.

Theorem A works for any subset 𝒫 of primes, so the one-scale barrier holds on all such slices as well. I
found no bounded slice with different combinatorics (crossing forced at one scale). By finiteindex B1, every
CF bounded slice has finite index anyway.

## 4. Registry entry

1. **Aim:** find n with Q ∩ (ab*)^n not CF (refute Kászonyi–Katsura), or prove KK for all n as a barrier.
2. **Strongest proved:**
   - Theorems A/B: for every n, every h ∈ Z_{>0}^n and every admissible δ, a weighted reflection structure
     P_{c,h} escapes. The one-scale Dickson / near-constant obstruction (L6, F) cannot prove non-CF of any
     Q_n.
   - Corollary A3: the near-constant slab of E_n is covered by explicit stratified linear subsets, for every n.
   - Rotation remark: stratification is rotation-invariant, so Cyc-closure gives no extra freedom.
3. **Missing step (precise):** a two-scale (flag) obstruction lemma. It would assert that there exist
   h, g ∈ Z_{>0}^n and δ such that, for every pair of stratified P_1 ⊆ P_2 with h ∈ relint cone(P_1) and
   g ∈ relint cone(P_2) + span(P_1), there is d ∈ D_h ∩ D_g with δ ∈ span(P_2) + V_d. It would also have to
   show, by a Dickson argument on N h + M g + δ, that this condition implies non-CF. Neither the lemma nor its soundness is proved. Alternatively, a
   construction covering E_n \ (near-reflection-symmetric region) would prove KK.
4. **Counterexamples:** none to KK. The near-constant criterion is refuted for all n (Theorem A).
5. **Strength:** "Q_n not CF for some n" is strictly stronger than needed in one sense, since it implies Q not
   CF. The missing two-scale lemma is a statement about one fixed n, so it is weaker than "Q not CF" in scope,
   but it would contradict the expert conjecture KK.
6. **What would reopen:** a two-scale family with h^{-1}g having no reflection axis compatible with all
   primes, for which every non-crossing extension of a reflection fails. A computer search over n = 6..30 for
   two-scale families is the next experiment. Since Q_6 is CF, any criterion must pass n = 6, 10, 12, 14,
   15, 18, 20, 21, 30 (known CF from the literature for ≤ 3 prime powers).
