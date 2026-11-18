# poly_S2K — explicit mixed cover of E_6 (closes the S2D gap for n = 6); two-prime generalisation

Script: `scripts/poly/s2k_rect.py` (`box6 4`; `sample n p q T [m]`). Literature (KK, devil §4) not re-derived beyond n=6.

## 1. Rectangle certificate (PROVED, any n with exactly two primes p,q)
A=n/p, B=n/q, R_i = {i, i+A, i+A+B, i+B} (mod n). u = x_{i+A} − x_{i+B}, w = x_{i+A+B} − x_i.
On V_p (x_t = x_{t+A}): u = −w. On V_q: u = w. Hence |u| ≠ |w| ⇒ x ∈ E_n.
The diagonals {i,i+A+B}, {i+B,i+A} are nested on the cycle (0<B<A<A+B<n) ⇒ non-crossing in any linear cut.
Cone pieces (4 per rectangle): w>|u|, w<−|u|, u>|w|, u<−|w|; each = stratified linear set
base e_b, periods e_a+e_b, e_b, e_c+e_d, e_b+e_c, e_b+e_d, e_s (s ∉ R) [(a,b) dominant diagonal, (c,d) other]:
all chords share an endpoint or nest ⇒ stratified (COMPUTER-CHECKED: linear set == region in box ≤4).
Pieces are disjoint per rectangle.

## 2. n = 6 cover (PROVED; COMPUTER-CHECKED box ≤ 4)
Distinct rectangles (R_i = R_{i+3}): {1,4,6,3}, {2,5,1,4}, {3,6,2,5} → 12 cone pieces, plus
B1 pieces sign L(x) for L ∈ {x4+x5−x1−x2, x1+x6−x3−x4} (basis of W_6^⊥): 4 one-counter pieces. Total 16.
Proof of coverage on W_6 (x = a+b, a 3-per., b 2-per.): for rectangle R_1, w+u = −2δ ≠ 0, w−u = 2(a3−a1);
rotations give a1=a2, a2=a3. R fails only if the corresponding a-equality holds; two failures ⇒ a constant ⇒ x ∉ E.
So every x ∈ E∩W_6 lies in ≥ 2 cone pieces; x ∉ W_6 lies in a B1 piece.
Ply (distinct pieces): ≤ 3 on W_6, ≤ 3+2 = 5 overall (script reports 6/8 counting each rectangle twice).
Box ≤4: |E|=15480, uncovered 0, |E∩W_6|=180. Each piece unambiguous after splitting by sign of the other diagonal
(independent periods). ⇒ Q∩(ab*)^6 has a CFG of ambiguity ≤ 5 (via ab⁺; ab* zeros handled identically since
the linear sets live in ℕ^6 and the a-blocks are fixed).

## 3. Generalisation (COMPUTER-CHECKED samples, 20000 random a+b, entries ≤3 each)
- n = pq squarefree (n=10, 15): n rectangles cover all sampled E∩W_n; analogous proof plausible ⇒ O(n) pieces,
  ply O(n) (OPEN-proof, CONJECTURED).
- n non-squarefree (12, 18, 20, 24): uncovered points exist even with all multiples A∈(n/p)ℤ, B∈(n/q)ℤ,
  e.g. n=12 x=(1,2,3,3,1,3,3,2,1,3,3,3). Rectangle scheme does NOT generalise; poly(n) ambiguity for p^a q^b: OPEN.

## 4. Three or more primes (n = 30)
Only from the citation in devil §4 (not re-verified, server unreachable): KK prove CF for two prime powers,
(1997) three prime powers, and Kászonyi 2010 whenever Σ_{p|n}1/p < 4/5. n = 30 = 2·3·5 is a product of three
prime powers, so per that citation Q∩(ab*)^30 IS CF (via the 1997 three-prime-power result, not the 4/5 rule,
since 1/2+1/3+1/5 = 31/30). Four or more primes with Σ1/p ≥ 4/5 (e.g. 210): as cited, OPEN.
Caveat: the "1997 three prime powers" clause is second-hand; treat as LITERATURE-UNVERIFIED.
