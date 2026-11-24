# R4-B: one varying prime — Q_pp = {w ∈ Q : g(w) = 1 or a prime power}

Notation as in `R2/pcop.md`: g(w) = gcd(#a w, #b w), Cop = {g = 1}, NonPow_p = {w ≠ u^p}. Script: `round2/scripts/r4_pp_checks.py`.
Target: the **sandwich** Q_pp ⊆ L ⊆ Q (Q_pp itself is not CF, §0). No construction found. What I did find:
(i) every prime-power sandwich, even for ONE FIXED prime, contains a copy of the coprime sandwich P_cop; (ii) the "varying prime"
difficulty, isolated correctly, kills every chord-exposing grammar, even on {a^p b^p}.

## 0. Summary

| item | status |
|---|---|
| Q_pp is not CF (so L(G) = Q_pp is impossible; target is Q_pp ⊆ L ⊆ Q) | [written proof], one line from P2 |
| **Prop H.** For each fixed prime p: a CFL L with {w ∈ Q : g(w) = p} ∩ (a^p+b^p)* ⊆ L ⊆ Q and ambiguity f(n) gives L′ = h_p⁻¹(L) ∪ {a,b} with Cop ⊆ L′ ⊆ Q and ambiguity f(pn). So P(Q_pp) ⇒ P(Q ∩ {g = p^k}) ⇒ P_cop | [written proof] + [computational] (block lemma, 42 930 words, 0 failures) |
| **Cor U_p.** For every fixed prime p, no unambiguous CFL L has {w ∈ Q : g(w) = p} ⊆ L ⊆ Q. A fortiori none for Q_pp | [written proof] (Prop H + Theorem U; not audited) |
| Polynomial ambiguity of U_pp: same gap as P_cop (count sandwich, §6). Nothing new | [assessment] |
| Settles the [conjecture] in `R2/cyclic.md` §4 ("fixed active-prime problems reduce to P_cop-type sandwiches"), in the direction "contain P_cop" | [written proof] |
| **VP** (the isolated varying-prime question, §3): a poly-amb CFL that agrees with Q on every class with g a prime power ≥ 2, and is unconstrained elsewhere | **OPEN**. Not P_cop-hard by Prop H's mechanism |
| **Theorem V.** No CFG exposing one valid mismatch chord (span ≡ 0 mod n/p, p \| g) covers infinitely many of the words a^p b^p (p prime), even under VP's relaxed soundness and at any ambiguity | [written proof] + [computational] (ray mechanism, 423 163 rays, 0 unresolved) |
| Count / ratio certificates (balanced prefix, cycle-lemma minima, Parikh windows) | blocked: each needs a test of the form ψ(x) ∝ ψ(w), and that is multiplicative (§4) |

## 1. Q_pp is not CF

Suppose it were. Then S = ψ(Q_pp) is semilinear and S ⊇ P. By P2 (`R2/pcop.md` §2), S contains vectors whose gcd has arbitrarily many
prime factors. But every vector of ψ(Q_pp) has gcd 1 or a prime power, which is a contradiction. ∎ So the target is a sandwich
Q_pp ⊆ L ⊆ Q. That is also the form that matters for building Q.

## 2. Prop H: every prime-power sandwich contains the coprime sandwich

**Block lemma.** Fix a prime p and let h_p(a) = a^p, h_p(b) = b^p. For non-unary u, h_p(u) ∈ Q ⇔ u ∈ Q, and g(h_p(u)) = p·g(u).
*Proof.* The gcd claim is L2. (⇐ of primitivity is clear: u = v^k gives h_p(u) = h_p(v)^k.) Suppose h_p(u) = v^k with k ≥ 2, and let r = |v|.
- If p | r, then v is block-aligned, v = h_p(v′), and u = v′^k because h_p is injective.
- If p ∤ r, then the cyclic word h_p(u) is invariant under rotation by r. Take a block end i (i ≡ p−1 mod p) and put s = r mod p ∈ [1, p−1].
  Then i+r and i+1+r sit at block offsets s−1 and s, so they lie in the same block, and h[i] = h[i+r] = h[i+1+r] = h[i+1].
  Every block boundary therefore joins equal letters, so u is unary, which is a contradiction. ∎
[computational: `r4_pp_checks.py` (a), p = 2, 3, 5, |u| ≤ 14/12/10, 42 930 words, 0 failures]

**Prop H.** Let L be a CFL with ambiguity f, with Q^{(p)} := {w ∈ Q : g(w) = p} ∩ h_p(Σ*) ⊆ L ⊆ Q. Put L′ = h_p⁻¹(L) ∪ {a, b}.
- **Soundness.** If u ∈ L′ is non-unary then h_p(u) ∈ Q, so u ∈ Q by the block lemma. The letters a and b are primitive.
- **Coverage.** If u ∈ Cop is non-unary, then h_p(u) ∈ Q and g = p. So h_p(u) ∈ Q^{(p)} ⊆ L, and u ∈ L′.
- **Ambiguity.** Pullback along the uniform prefix code h_p preserves tree counts exactly (§5.4 / `PA/poly_S4M.md`: DFA product with
  h_p(Σ*), then block decoding). So amb_{L′}(u) ≤ f(p|u|) + 1.

Hence P_cop holds whenever such an L exists. Since Q_pp ⊇ Q^{(p)}: **P(Q_pp) ⇒ P(Q ∩ {g = p^k}) ⇒ P_cop**, for every single fixed p. ∎

**Cor U_p (unambiguous).** Let L be unambiguous with Q^{(p)} ⊆ L ⊆ Q. Then L ∩ h_p(Σ*) is unambiguous (DFA product), so its
generating function H(x,y) is algebraic. F_{L′}(x,y) = H(x^{1/p}, y^{1/p}) + x + y is algebraic over ℚ(x^{1/p}, y^{1/p}), hence over ℚ(x,y),
and it is a power series with the right coefficients. The proof of Theorem U uses only this algebraicity, together with
Cop ⊆ L′ ⊆ Q. So the proof applies verbatim and gives a contradiction. ∎
- So the "one fixed prime" slice (g = 2, say) is already inherently ambiguous as a sandwich. G_2 = NonPow_2 does not contradict this:
  NonPow_2 ⊄ Q.
- The extension to polynomial ambiguity hits exactly the P_cop gap (`R2/pcop.md` §5). No new mechanism.

**Consequences for the task.**
- The question "is there a poly-amb sandwich for Q_pp?" is at least as hard as P_cop. Even the fixed-prime version is.
- Prime-power sandwiches therefore cannot isolate the varying prime: the cross-ratio exclusion core (B) of `R2/cyclic.md` §4 is inside
  every one of them.
- Core (A) (multi-prime witnesses at fixed ratio) is absent from Q_pp. By L3, Q_pp on every fixed-#a slice is Q ∩ Π_{p^k} = NonPow_p ∩ Π_{p^k},
  so linear ambiguity per slice is achievable.
- The reverse transfer fails as in `R2/pcop.md` §4. Morphisms give g(src) | g(tgt), so a Q_pp-guarantee pulls back only to
  prime-power or coprime classes, and no transfer lifts P(Q_pp) to the full problem.

[computational: `r4_pp_checks.py` (b), all words n ≤ 18 with g = p^k ≥ 2 (208 204 words): w ∈ Q ⇔ w is not n/p-periodic, 0 failures. This is L1 specialised.]

## 3. The isolated varying-prime question VP, and Theorem V

**VP.** Is there a polynomially ambiguous CFL L with L ∩ C = Q ∩ C, where C = {w : g(w) is a prime power ≥ 2}? L is unconstrained on
g = 1 and on multi-prime classes.
- Each fixed-p part has a uniform answer, G_p (`R2/uniform.md` §1), and so does any finite set of primes.
- Pulling VP back along h_p gives soundness only on p-power classes. So Prop H does **not** make VP P_cop-hard, and VP is the honest
  "one varying prime" core.
- VP ∧ P_cop does not obviously give P(Q_pp), because the union of the two languages need not be sound on multi-prime classes.
  [assessment]

**Valid chord.** In w (|w| = n), a marked pair i < i′ with w_i ≠ w_{i′} is *valid* if (n/p) | (i′−i) for a prime p | g(w).
It then certifies w ≠ u^p, and when g = p^k that is primitivity. The union over p of G_p with chords marked is the model case.

**Theorem V.** Let G′ be a CFG over Σ × {0,1}. Assume every word of L(G′) has exactly two marks, at a mismatched pair, and that the pair is valid
whenever g(w) is a prime power ≥ 2 (VP-relaxed soundness). Then only finitely many words a^p b^p (p prime) lie in π(L(G′)), at any ambiguity.

*Proof.*
1. **Reduce to tuples.**
   - Intersect with the regular shape a*a′a*b*b′b*. A mismatch in a^m b^m has its a-mark first.
   - Relabel by a deterministic GSM into a₁*a′a₂*b₁*b′b₂*, which keeps the language CF.
   - Take Parikh images and intersect with {X = Y}. This gives a semilinear set S of tuples (x,y,z,t) with x+y = z+t = m−1, n = 2m,
     and chord span d = y+z+1.
2. **Pick a ray.** Suppose some linear set Λ ⊆ S covers infinitely many primes m.
   - Some generator v of Λ has v_m > 0. Choose P₀ ∈ Λ with m(P₀) = m₀ prime and m₀ > v_m.
   - On the ray P₀ + ℕv, the quantities m(t) = m₀ + v_m t and d(t) are affine.
   - By Dirichlet the ray contains infinitely many primes, and it contains the prime powers m* = q^{φ(v_m)+1} for large primes
     q ≡ m₀ mod v_m (since m* ≡ q ≡ m₀).
3. **Proportional case: d(t)/n(t) ≡ ρ constant.**
   - At a prime m (g = m, so n/p = 2), validity means d = 2j with 0 < j < m. Then ρ = j/m is in lowest terms, with denominator m.
   - Two different primes on the ray would give ρ two different denominators, which is a contradiction.
4. **Otherwise.** gcd(n(t), d(t)) divides the nonzero constant Δ = n(t)·d′ − d(t)·n′.
   - At m* = q^K (K ≥ 2), validity needs (n/q) | d, so gcd(n, d) ≥ 2q^{K−1}, which exceeds |Δ| for large q.
   - That is a contradiction.

So every linear set covers finitely many primes, and S is a finite union of them. ∎

- [computational: `r4_pp_checks.py` (c).] For all 423 163 rays with prime base m₀ ≤ 30 and |v| ≤ 5:
  - 418 733 have an invalid prime-power point among their first 200 points;
  - the other 4 430 fail exactly at the predicted point q^{φ(v_m)+1};
  - 0 rays are unresolved.
  A naive scan capped at m ≤ 5000 finds "valid" rays covering 162 primes. The predicted witnesses lie beyond the cap, which is why the
  Dirichlet step is needed.

**Reading.**
- Theorem V is the one-varying-prime analogue of Theorem W. W: two primes in one word. V: one prime that varies across words, here
  even with fixed slope 1:1 and a single defect.
- The family is trivially covered by a⁺b⁺ (unambiguous, inside Q). So V restricts mechanisms, not languages.
- Any uniform VP grammar must hide its witness: it cannot expose a chord of span ≡ 0 mod n/p. The reason is the same in every case:
  enforcing a span n/p by ratio counting needs the ratio p−1 : 1 fixed per linear component.
- V does not cover multi-mark or "hidden counter" certificates (same caveat as W).

## 4. Construction attempts (all blocked; [assessment] unless marked)

- **(a) Chord with varying ratio.** Exposed: dead (Theorem V). Hidden, as {xσyzτt : |xt| = (k−1)|yz|+…, k ≥ 2}: soundness also needs
  k | g, not just k | n. Example: abaaba = (aba)², g = 2, has a span-n/3 mismatch. "k | g" is a divisibility of both letter counts by a
  word-dependent k, which is not semilinear.
- **(b) Parikh windows / balanced prefixes.** w = u^p forces every cyclic window of length n/p to have ψ = ψ(w)/p.
  - Every p-free variant ("a window x with ψ(x) ∝ ψ(w) but …", "ψ(w) = kψ(x)") is a test ψ(x) ∝ ψ(w). On a*b*a*b* that is il = jk, il > jk, …,
    which is not CF (S4C §3).
  - "ψ(w) = kψ(x), mismatch at span |x|" is also **unsound** for k = p^j with j ≥ 2: the span n/p^j need not be a period of u^p.
- **(c) Cycle-lemma minima.** μ(w) = number of global minima of the cyclic walk with slope ψ(w)/g.
  - p ∤ μ ⇒ w ≠ u^p, and μ = 1 ⇒ w ∈ Q, which covers Cop.
  - But "unique minimum" compares one prefix against all prefixes at a word-dependent slope, which is non-CF
    (a^i b^j a^k b^l, il > jk). μ = 1 also misses many primitive words with g ≥ 2.
- **(d) Slice #b = p prime.** There, w ∈ Q ⇔ the b-gap sequence is not constant. That is easy on the slice, but off it the certificate must
  reject gap sequences of period m/q for m = #b = q^k. That is VP again, one level down (the S4N-style self-reduction).

## 5. Exact open sub-questions left

1. **VP** (§3) with hidden certificates. Theorem V excludes exposed chords. An unambiguous-VP obstruction would need U-type control of
   rows where the coprime coefficients are *unconstrained*. Tried: the p-section of row p is 1/(1−y^p)², but the off-section is free, so the
   singularity count is not forced. Open.
2. **P_cop**, unchanged. By Prop H it lower-bounds every prime-power sandwich, Q_pp included.
