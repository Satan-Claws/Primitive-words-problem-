# r20_stable.md — R20-A: does completeness + substitution + rotation force a G⁻-stable critical structure?

Scripts:
- `scripts/r20_stable_raney.py` → `scripts/r20_stable_raney_out.txt`: exhaustive n ≤ 16, plus an exact fold DP up to
  n = 1024 (~10 s).
- `scripts/r20_stable_profile.py` → `scripts/r20_stable_profile_out.txt`: Monte Carlo, n = 1001, 3000 uniform G⁻ words
  (~20 s).

Notation follows r17_bridge.
- P is the ±1 walk (a = +1).
- d_k = P(k) + P(n−k) − P(n).
- G⁻ = {d_k < 0 for all 1 ≤ k ≤ n/2}.
- A *cone* is a fixed context p[·]q, a critical linear SCC C, and all token sequences.
- (CONE) means that some cone has all its words in G⁻.

## Verdict

**The mechanism fails, for a precise reason.** Neither (1) nor (2) yields a bridge. The obstruction is explicit, and what
remains reduces to a coverage statement that does not involve G⁻.

1. **(1) "Positive fraction" does not rescue T8** [written proof].
   - By counting, positive G⁻-fraction in a critical cone means one of two things:
     - it is impossible, when the cone is word-saturated (κ < ½); or
     - it amounts to ambiguity concentration of degree exactly ½ (Prop F).
     Neither contradicts polynomial ambiguity.
   - T8_poly uses G⁻ only through *single-word* implications W ↦ W′ (NS pumping, Step-2 replacement, padding). Each of
     these maps is built to leave G⁻, so for L(G) = Q its image lies in Q ∖ G⁻.
   - A positive-fraction stable family is a Doob conditioning of the token walk. It is not a cone, so the renewal input
     Lemma R (i.i.d. tokens over all sequences) is not available (Prop PF).
   - The only way to salvage the argument is a stable sub-cone, and that is exactly (CONE).
2. **(2) "Instability forces alternative derivations" is false** [written proof + exhaustive check].
   - The explicit grammars H_R (§3) have language inside Q and ambiguity Σ|r| ≤ 3R (exactly |D| on the (1,1) family alone, which for R = 1 is **unambiguous**).
   - Every Dyck-factor substitution keeps a word of H_R inside L(H_R) ⊆ Q. Such substitutions leave G⁻ at the generic
     rates (ℓ^{−1/2} two-sided) [MC].
   - So instability of G⁻-derivations is compatible with bounded ambiguity.
   - H_R fails only on **coverage**:
     - At odd n it covers a fraction ≍ c_R/√n of G⁻ (exact DP: 1.6/√n for R = 1, 4.7/√n for R = 9, at n = 1023).
     - At n = 2ʲ it covers 0, because there every low-weight Raney certificate has gcd(r, n) ≥ 2.
3. **Reduction [precise].** An argument built only on local substitution stability of G⁻-derivations cannot separate a
   grammar G for Q from the bounded-ambiguity grammars H_R. Any contradiction must therefore come from completeness on
   the words that every bounded-weight cycle-lemma certificate misses. These are the balanced words with gcd(r, n) ≥ 2
   for all small weighted drifts r, i.e. the gcd ≥ 2 / tie core of RESEARCH_NOTE §3. G⁻ plays no role in that core.

## 1. Where G⁻ binds: the stability profile [MC + heuristic]

**Fold locality.** d_k pairs the letter at position k with the letter at position n+1−k. Under the uniform measure on G⁻,
(d_k) is a meander, so the slack is −d_k ≍ √k. A substitution of length ℓ at fold depth δ (its distance to the nearer end)
changes d only for k ≥ δ, and by O(ℓ). So it is stable w.h.p. iff ℓ ≪ √δ.

The binding constraints sit at **both ends simultaneously**. A tree can coordinate them only through a spanning linear
spine, i.e. a fold-implementing structure.

P(the substituted word is still in G⁻), for a block shuffle (which preserves D), with n = 1001
(`r20_stable_profile_out.txt`):

| ℓ | depth 0 | depth 8 | depth 64 | depth 250 | two-sided outer | ℓ^{−1/2} |
|---|---|---|---|---|---|---|
| 4 | .730 | .987 | .999 | 1.000 | .552 | .500 |
| 16 | .484 | .934 | .995 | 1.000 | .279 | .250 |
| 64 | .339 | .794 | .962 | .990 | .146 | .125 |
| 256 | .216 | .622 | .867 | .926 | .064 | .062 |

- Two-sided outer tokens, which is what a spanning cone substitutes, give the ballot rate ≈ 1.1·ℓ^{−1/2}.
- One-sided substitution at an end decays like ≈ ℓ^{−1/4}. This exponent is a guess from the MC; it is not proved.
- Interior short blocks are stable with probability → 1, but they say nothing: the G⁻ constraint there has slack √n.

**Cyclic transport** (Theorem C, r17 §4). For G = G₀′, a tree of a word w ∈ G⁻ is a G₀-tree of z = rot_j w that is cut
at j. The two ends of w are **adjacent** leaves of z's tree, and w ∈ G⁻ says that T(z) is strictly midpoint-concave at
the cut (Lemma A, r6_miss). So "G⁻-stability of a substitution" means exactly "the substitution does not move the
argmax-type point away from the cut". A G₀ that is not aligned with the argmax never has this property, beyond the
generic rates above.

## 2. Answer to (1): positive-fraction stability

**Prop F (counting) [written proof].** Take a cone K in a grammar with ≤ n^κ trees per word.
- By Lemma R, trees_K(n) ≥ c·2ⁿ along a progression. So #words_K(n) ≥ c·2ⁿn^{−κ}.
- (a) The word-fraction of K_n inside G⁻ is ≤ |G⁻_n| / #words_K(n) ≤ C·n^{κ−½}. For κ < ½ it tends to 0.
- (b) Suppose the tree-fraction is ≥ c. Then Σ_{w∈K∩G⁻} amb(w) ≥ c·2ⁿ while |K ∩ G⁻| ≤ C·2ⁿ/√n. So the mean
  ambiguity on K ∩ G⁻ is ≥ c′√n.

*Proof.* Divide the two bounds. ∎

So "positive fraction" is either impossible or costs a fixed degree ½ of ambiguity. Fixed-degree lower bounds do not
count (prompt §7). The entropy view gives the same picture: G⁻ costs ½·log n bits and the quadrant costs log n bits,
while polynomial ambiguity has a budget of κ·log n bits. Measure statements about G⁻ or quadrant membership along a
cone therefore cannot contradict polynomial ambiguity. Only the *all*-sequences statement (CONE) can, which is why T8
needs it.

**Prop PF (T8 does not survive "positive fraction") [written proof, from the audit table of r17 §2 and
audit_t8poly_final §1].** Every use of L ⊆ G⁻ in T8_poly has the form "W ∈ L ⇒ W′ ∈ L ⊆ G⁻" for a *specific* W′:
- **NS:** W′ = W with m ≈ C_W + c + 1 copies of a cycle with D(s) ≥ 1 grafted left of n/4. By construction
  A_{W′}(k₀) > B_{W′}(k₀), so W′ ∉ G⁻ deterministically.
- **Step-2 replacement and the MS/PR padding** W′ = ρ·s: the same holds by design. Lemma Core says that W′ ∈ G⁻
  forces W into the quadrant.

For L(G) = Q, every such W′ lies in Q ∖ G⁻. A positive fraction of G⁻-words in the cone therefore gives **no**
information about the W′, since the maps are fixed and not random.

The measure-theoretic substitute fails too. The family of stable token sequences is the token walk conditioned on
{d < 0}, which is an h-transform.
- Its tokens are not i.i.d., and it is not closed under prepending tokens, so Lemma R does not apply.
- Its renewal mass equals G⁻'s own mass ≍ √N, so the squeeze has nothing to squeeze.

If the stable sequences contained a sub-cone (a sub-token-set T′ with fixed context, closed under prepending), then
either T′ is critical, which is (CONE) itself, or T′ is subcritical with bounded mass. So **positive fraction ⇒ T8
holds only via (CONE)**. Lemma Core fails for reasons of mass. This version fails for reasons of **closure**, and it
does so even at fraction → 1 (interior blocks, §1).

## 3. Answer to (2): an explicit bounded-ambiguity fragment whose G⁻-derivations are unstable

**Construction.** Fix weights (α, β) ∈ {(1,1), (1,2), (2,1)} and r ≥ 1. Put
Rₐ(r) = {z : every proper prefix has α#a − β#b > 0, and α#a(z) − β#b(z) = r}.

For (1,1) this is the language a·Dyck·a·Dyck·⋯·a·Dyck with r factors a·Dyck. That grammar is
unambiguous: split at the last visits of the levels 1…r−1.

Intersect with the regular set {|z| : gcd(r, |z|) = 1}, and add the mirror family with the roles of a and b exchanged.
Let H_R be the cyclic closure (Theorem C) of the union over r ≤ R.

**Prop H [written proof + exhaustive check].**
- (i) **L(H_R) ⊆ Q.** If w = zᵖ, then p | r and p | n, so p | gcd(r, n) = 1.
- (ii) **amb_{H_R}(w) = Σ over applicable families of #{j : rot_j w ∈ Rₐ(r)} = Σ |r| ≤ 3R** (each family contributes |r|). This is the cycle lemma
  (Dvoretzky–Motzkin). Exhaustive check for (1,1), R = 3, n ≤ 16: 20862 words, 0 non-primitive, 0 cases with
  amb ≠ |D|. H₁ restricted to the (1,1) family is **unambiguous**.
- (iii) **Substitution closure inside Q.** Replacing a Dyck subtree of z's tree by any Dyck word preserves r. So every
  substitution image of a derivation of w ∈ L(H_R) ∩ G⁻ stays in L(H_R) ⊆ Q.
- (iv) **Instability.** These substitutions leave G⁻ at the rates of §1. Shuffles preserve D, and the MC table is
  exactly this situation for the (1,1) family.

**Coverage** (exact fold DP, `r20_stable_raney_out.txt`): |L(H_R) ∩ G⁻| / |G⁻| · √n.

| n | R = 1 | R = 9 |
|---|---|---|
| 63 | 1.59 | 2.91 |
| 255 | 1.59 | 3.05 |
| 1023 | 1.60 | 4.73 |
| 64 | 0.03 | 0.17 |
| 256 / 1024 | 0 | 0 |

At n = 2ʲ every centred certificate has r even. The off-centre weights (1,2) and (2,1) give odd r, but only far from
balance, where G⁻ has almost no mass.

**Consequence for (2).** The proposed step "a G⁻-derivation that is not substitution-stable must have many alternative
derivations" is false: H₁ is an unambiguous counterexample on its own language. What separates H_R from a grammar for Q
is purely quantitative coverage. H_R reaches ≍ R/√n of G⁻, and nothing at n = 2ʲ, while G must reach all of it.

So in the mechanism the G⁻ condition is a **red herring**. Completeness must be used on the balanced words with
gcd ≥ 2, the core that no bounded-weight cycle-lemma certificate reaches, and G⁻-stability says nothing there.

## 4. F1 check
- Prop F and Prop PF are accounting and no-go statements. Prop H is a construction. None of them bounds the density of
  an arbitrary CFL ⊆ Q.
- The single positive implication, "positive tree-fraction ⇒ mean ambiguity ≥ √n", uses ambiguity explicitly and has
  fixed degree. It is not a target result.

## Status
| claim | label |
|---|---|
| Fold locality / stability profile (two-sided ≈ ℓ^{−1/2}; one-sided ≈ ℓ^{−1/4}; interior → 1) | MC (n = 1001) + heuristic; the ℓ^{−1/4} exponent is a guess |
| Prop F: positive G⁻-fraction in a cone ⇒ κ ≥ ½, mean ambiguity ≥ c√n on its G⁻ part | written proof (uses Lemma R) |
| Prop PF: T8 uses single-word maps designed to exit G⁻; the positive-fraction family is not a cone; salvage = (CONE) | written proof (relative to audited T8_poly structure) |
| Prop H: H_R ⊆ Q, amb = \|r\| ≤ R, substitution-closed, G⁻-unstable | written proof + exhaustive check (n ≤ 16) |
| Coverage of G⁻ by H_R: ≍ c_R/√n at odd n, 0 at n = 2ʲ | exact DP (n ≤ 1024) |
| Mechanism "completeness + substitution + rotation ⇒ G⁻-stable critical structure" | **FAILS**; reduces to completeness on the gcd ≥ 2 balanced core, where G⁻ is irrelevant |
