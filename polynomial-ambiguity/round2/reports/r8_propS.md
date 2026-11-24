# r8_propS.md — R8-A: Prop S gaps G1/G2 toward T8 (negative side)

Status: final. **T8 NOT proved.** Main finding: the Prop S + G1 + G2 route is circular, so it cannot prove T8 even for
unambiguous G (Theorem C below). Prop S and Cor S′ never use L ⊆ G⁻. Two smaller positive items: the exact threshold, and an
anchored-rectangle bound n^{−4/3} that does use G⁻ set-structurally.
Script: `round2/scripts/r8_propS_anchor.py` (<1 s; the m = 800 check took about 3 s).

## 0. Threshold [DP exact to N = 2000 + standard ballot asymptotics]
G⁻_n is a fold ballot. The pairs (v_i, v_{n−1−i}) give lazy steps e ∈ {−1, 0, +1} with probabilities ¼, ½, ¼, and every partial sum
over k ≤ N = ⌊n/2⌋ must be < 0. The DP gives P·√N = 0.2821 = 1/(2√π) at N = 125 … 2000, so
**|G⁻_n| = (1 + o(1)) 2ⁿ/√(2πn).** Each conjugacy class has ≤ n elements, so rotation-density (|Rot(L)_n| ≥ δ2ⁿ) needs
**|L_n| ≥ δ2ⁿ/n**. That is a ≍ n^{−1/2} fraction of G⁻_n. G⁻ itself averages ≈ √(n/2π) rotations per class.

## 1. Theorem C (circularity): Prop S does not use G⁻, and G1 is an identity [written proof]
Record a spine s as its labelled path *with child directions*. In one tree, distinct leaves have distinct such paths. Let G be any
unambiguous grammar (no hypothesis on L). For each position a ∈ [0, n), each w ∈ L_n has one tree and that tree has one spine to
position a. Hence, for **every** a,
  Σ_s |X_{s,a}|·|Y_{s,n−1−a}| = |L_n|.   (∗)
(The factorisations of x through L(A_1)⋯L(A_t) are unique by unambiguity, so |X_{s,a}| counts words.)
Consequences:
- Step 1 of Prop S can use |L_n| in place of |G⁻_n|. Steps 2–3 then give *for every unambiguous G*: a fixed spine carries
  O_s(|L_n|/n). This is stronger than Cor S′, and it holds without any G⁻ hypothesis (e.g. for Σ*). **So Prop S/S′ is a count-level
  fact about unambiguous grammars. The r7 remark "not a §6 count-only route" is wrong**: the set-level closure x c y ∈ L ⊆ G⁻ is only
  ever used to bound by |G⁻_n|, which is weaker than (∗).
- A fully uniform version of step 2 says centre slice ≤ (C/εn)·Σ_{|a−N|≤εn} slice_{s,a}. Summed over s, (∗) turns it into
  |L_n| ≤ C′|L_n|. That is a tautology. **So no uniformity statement (G1) over spines, added to Prop S, can yield T8.** The per-spine
  O(1/n) is exactly the 1/n that comes from spreading |L_n| over n positions.
- Packing alone cannot work either. Every word is a singleton rectangle {x}·c·{y}, which is trivially closed under uncoupling at its
  own lengths. Any proof of T8 must use that the X_s, Y_s are products of finitely many nonterminal languages *shared across
  spines*. It cannot be spine-local.

## 2. G2: word-level distinctness [written proof + example]
- Distinct (a, factorisation) always give distinct *trees*. They give distinct *words* iff those words are unambiguous. For
  amb ≤ Cnᵏ, (∗) holds with the tree count |T_n| ≤ Cnᵏ|L_n| in place of |L_n|, so Theorem C's circularity holds verbatim.
- Distinctness genuinely fails inside G⁻. Take S → b A a B a, A → aA | ε, B → aB | ε. With the centre spine fixed (through the middle a),
  every split gives the same word b a^{n−1} ∈ G⁻ (d_k = (k−1) − k < 0), and amb = n − 2. So one spine can contribute ≍ n copies of
  one word, and multiplicity n^k is attained.
- Choosing a canonical tree per word destroys the product structure X_s × Y_s: a shifted copy may have a different canonical spine.
  So "words with a chosen tree" loses uncoupled closure. In any case G2 is moot given §1.

## 3. Anchored rectangles: a genuine G⁻ gain, n^{−4/3} [cone-exit theorem for fixed g; conjecture for the optimum over g; DP]
Uncoupled closure at *all* lengths gives two things.
(i) Lemma R's threshold g(k) = max_{x∈X_s,|x|≥k} F_x(k) is uniform over lengths.
(ii) **Anchoring**: with y₀ the shortest word of Y_s (length ν), x c y₀ ∈ G⁻ for every x ∈ X_s. So X_s ⊆ {F ≤ g} ∩ (lag-ν G⁻).
The symmetric statement holds for Y_s with x₀ (length μ).
For μ = ν = O(1) and g = k/2 + O(1), each side is a 2D simple walk (u, v) = (F − k/2, R − k/2) confined to a cone of angle 3π/4
({u ≤ 0, u ≤ v}, respectively {v ≥ 0, v ≥ u}). The cone-exit exponent is π/(2·3π/4) = 2/3 (Denisov–Wachtel), so
**|X_{s,N}||Y_{s,N}| ≲ 4^N N^{−4/3}**, against N^{−1} from Lemma R alone.
DP (relaxed conditions, so these are upper bounds; g = k/2 + λ√k): per-side exponents −0.660, −0.663, −0.665 at m = 200, 400, 800;
best product −1.316, −1.324, −1.329 (prediction −4/3). The optimum is at λ = 0, symmetric as in Lemma R.
Optimality of g ≈ k/2 for general (non-√k) g is a [conjecture]. The degradation in μ, ν (≈ (μν)^{2/3}, saturating at μ, ν ~ √N) is a [heuristic].
Meaning: spines whose hanging sides have short minimal yields each carry ≤ N^{−1/3} of the threshold. T8 would still need a bound on how
many such spines can be active at once. That is a cross-spine statement (§1).

## 4. Exact gap (what T8 now needs)
**Cross-spine packing lemma (open).** For a CFG (unambiguous first), the family {X_s c Y_s} of centre-spine rectangles has, for each
nonterminal A on the spine, the shared factorisation X_s = X_{s≤A}·X_{A→s′}. One must show that the rectangles carrying ≥ δ2ⁿ/n in
total cannot all be (near-)anchored-threshold. Equivalently, the finite-nonterminal sharing must force many of them to sit far from
the G⁻ cone optimum. Neither spine-local smoothness (Theorem C) nor per-rectangle bounds (Lemma R, §3) can supply this.

## Status
| claim | label |
|---|---|
| |G⁻_n| ~ 2ⁿ/√(2πn); rotation-dense needs |L_n| ≥ δ2ⁿ/n (≍ n^{−1/2} of G⁻) | DP exact to N = 2000 + standard asymptotics |
| Thm C: (∗) identity; Prop S/S′ hold without G⁻; any G1 uniformity gives only a tautology | written proof |
| G2: word distinctness ⇔ unambiguity of those words; multiplicity ≍ n inside G⁻ attained; canonical trees break closure | written proof + example |
| Anchored rectangle ≲ 4^N N^{−4/3} (g = k/2) | cone-exit (cited) + DP; optimality over g is a conjecture |
| T8 (even unambiguous) | OPEN: needs the cross-spine packing lemma |

## 5. Reconciliation with audit_r7 (root message)
- Caveat 1 (spines record child direction): §1 already assumes it. (∗) needs it so that X_s is a product and each leaf has a unique spine.
- Caveat 2 (non-strongly-connected systems need residue-class asymptotics): this affects step 2 of Prop S only. **Theorem C does not
  depend on it.** (∗) is an exact identity, and the tautology argument assumes the *strongest* possible uniform smoothness. Whether
  step 2 is proved via Drmota–Lalley–Woods or periodic residue classes, a G1 route still yields only |L_n| ≤ C|L_n|. So Prop S stays
  true (audit) but is not a route to T8.
- The closed form |G⁻_n| = C(n−1, n/2) (even n) agrees with §0: C(n−1, n/2)/2ⁿ·√(2πn) → 1 (0.9975 at n = 100).
