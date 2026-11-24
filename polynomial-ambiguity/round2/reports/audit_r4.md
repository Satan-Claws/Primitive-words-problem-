# audit_r4.md — R5-C: adversarial audit of Prop H (`R2/r4_pp.md`) and the coverage-loop gadgets (`R2/r4_core.md`)

Scripts (written from the definitions; the candidates' scripts were not used):
- `scripts/audit_r4_pullback.py`: block lemma and edge cases, plus a literal pullback grammar G′ with exact tree counts vs CYK on h_p(u). Runtime 12 s.
- `scripts/audit_r4_gadgets.py`: independent LIN/FOLD/FL₃/LF₃/PF₂/RLF membership, soundness on every non-primitive word, fold-identity assertion, coverage cross-check. Run as `python audit_r4_gadgets.py 24 16` (17 s).

## Verdicts

| candidate | verdict |
|---|---|
| 1. Prop H (and the block lemma) | **SURVIVES.** The proof is correct, the edge cases are fine, and the tree-count identity is exact. Caveats below. |
| 1′. Cor U_p | **SURVIVES conditionally.** The transfer step is fine. It inherits Theorem U, which this audit did not check. |
| 2. Lemma S + gadgets FL, LF, PF, FOLD, LIN | **SURVIVES.** Sound, and genuine CFGs with O(n) ambiguity. |
| 2′. RLF | **SURVIVES with a caveat.** It is semantically sound. The wrap-run grammar is realisable, but the sketch leaves the split rule unspecified (see below). |

## 1. Prop H

**Block lemma.** The proof is correct, and it works for any p ≥ 2, not only primes. Take a block end i. If p ∤ r, the positions i + r and i + 1 + r sit at offsets s − 1 and s with 1 ≤ s ≤ p − 1, so they are in the same block. Hence every block boundary joins equal letters, and u is unary. Computational check: p = 2, 3, 4, 5 with |u| ≤ 14/11/10/9 (39 928 words), 0 failures. The check covers primitivity equivalence, g(h_p u) = p·g(u), and coverage of Cop.

**Edge cases.**
- Unary u = a^k (k ≥ 1): h_p(u) = a^{pk} with pk ≥ 2 is not primitive, so a^{pk} ∉ L ⊆ Q, and h_p⁻¹(L) contains no unary word. The coprime unary words are exactly a and b, since g(a^k) = k. Adding {a, b} by hand is therefore necessary and sufficient. It is disjoint from h_p⁻¹(L), so the ambiguity is f(p|u|) on non-unary words and 1 on a, b.
- ε: h_p(ε) = ε ∉ Q, so ε is never in L′.
- Soundness and coverage follow as stated.

**Tree-count identity (the main point to check).** The CF realisation is the literal grammar G′:
- Nonterminals are (A, q, q′), where q is a state of the block DFA: (offset o ∈ ℤ_p, current block letter c).
- A → BC becomes (A,q,q′) → (B,q,s)(C,s,q′) for every s.
- A → x at offset 0 emits x (this is the u-letter) and moves to (1, x).
- A → x at offset o ≠ 0 emits ε, requires x = c, and advances the offset.

Block letters split across different G-subtrees cause no problem. The letter is emitted by whichever leaf sits at offset 0, and the other p − 1 leaves are ε-leaves checked by the state. Every G-tree for h_p(u) has a unique consistent annotation, because the states are determined by positions. So the correspondence is a bijection, and #trees_{G′}(u) = #trees_G(h_p u) exactly.

G′ has ε-rules but no infinite tree families: every subtree has ≥ 1 leaf, so an ε-yield subtree has ≤ p − 1 leaves. If an ε-free grammar is wanted, ε-elimination only merges trees, so counts never increase.

[computational] 40 random ambiguous CNF grammars. p = 2 with |u| ≤ 6 and p = 3 with |u| ≤ 4: 6 240 tests, 4 207 with a nonzero count, counts up to 9.7·10¹¹, **0 mismatches**.

**Caveats.**
- (i) amb(L′) ≤ f(p n) presupposes a grammar for L with amb ≤ f. Normalising to CNF can only lower the counts.
- (ii) Cor U_p is simpler than written. By the identity above, h_p⁻¹(L) ∪ {a, b} is directly an *unambiguous* CFL, so its generating function is algebraic by Chomsky–Schützenberger. The x^{1/p} argument is unnecessary but correct, since h_p is injective. The conclusion still rests on Theorem U, which is unaudited.
- (iii) The reduction direction is correct: Q_pp ⊆ L gives Q^{(p)} ⊆ L.

## 2. Coverage-loop gadgets

**Lemma S.** Correct.
- (i) Rotation by |u| fixes every cyclic window feature, so each level set is a union of free ℤ_p-orbits. This holds for every K, including n < K, where windows wrap several times.
- (ii) For non-unary u^p, the cyclic run sequence has r ≡ 0 mod p and is (r/p)-periodic.
- The small cases agree. r = 1 cannot occur for u^p. For r = 2, α̂(1) = α₀ − α₁, which vanishes for u².

**Fold identity.** A pure-sign certificate (m,±) forces Σ x_k sin(2π(k − m/2)/N) ≠ 0, because the weight is nonzero off the two centres. The script asserts this numerically for every certificate it finds, for every feature (x^b, x^f, x^f − x^h, α, β), and it never fails.

**Independent brute force** (`audit_r4_gadgets.py 24 16`).
- **Soundness:** all 8 714 non-primitive words with n ≤ **24** (the task asked for 18). The number of gadgets accepting any of them is **0**.
- **Definition match:** S0 (LIN + FOLD) gives .9761 / .9225 at n = 12 / 16, which matches r4_core §2 (.976 / .923). S4 covers 100% of Q_n for n ≤ 16, which also matches.

**CF realisation and ambiguity.** Annotated window alphabet Σ^K × consistency DFA, then projection. The DFA reads c₀ (it does not guess it) and stores its first K − 1 letters for the wrap check, so it is deterministic. Each w has exactly one consistent annotation, so the projection is injective on R_K and tree counts are preserved. This needs n ≥ K; the finitely many words with n < K are handled separately, as stated.
- FL pieces are deterministic one-counter languages, so each is unambiguous. The union bound ≤ #pieces is fine.
- The LF/PF bounds 12n and 6n are correct: there are 12 factors and 6 unordered pairs, and (m,+) for f − h equals (m,−) for h − f.

**RLF wrap run.** The semantics is sound. The only open point is the grammar, and it is fixable.
- Non-crossing: reflection chords on a circle are parallel, hence non-crossing, and this survives cutting the circle anywhere, including inside the wrap run. So the arc diagram of a^s … a^t against its partner a^ℓ is non-crossing, as claimed.
- The sketch does not say how a^ℓ is split into the part matched with a^s and the part matched with a^t. A naive split multiplies the tree count by up to ℓ + 1 ≤ n. That is still polynomial, but it breaks the "exactly one derivation per comparison" claim.
- A canonical unambiguous split exists:
  - "<": a^s U a^{s+e} a^t V a^t, e ≥ 1.
  - "=": e = 0.
  - ">": if ℓ ≥ t, then a^{x+e} U a^x · a^t V a^t; if ℓ < t, then a^s U · a^ℓ V a^{ℓ+e}, with e ≥ 1.
- The wrap run must also get a fixed index convention (say index 0), so that a certificate is not counted under two indexings.

With these fixes, amb ≤ 2r holds. I did not build or tree-count the literal RLF grammar, so this part stays [written], not [computational].

**No fatal flaw found in either candidate.**
