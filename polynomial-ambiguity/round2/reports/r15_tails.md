# r15_tails.md — R15-B: heavier tails −1−2^{−k} (k ≥ 2)

Status: **partial.**
- (3) Citation check: done. The exponent set is confirmed (Banderier–Drmota Thm 3). r14's *mechanism* is
  **wrong**: tails −1−2^{−k} come from k stacked critical **nonlinear** SCCs, never from critical linear ones
  (Lemma ST, written proof of part (i), checked numerically).
- (2) Sharpening the cone exponent: **no-go** for the literal idea (Prop S).
- (1) Opening up the block: **no-go** for the literal idea. There is no internal critical linear structure.
- **New: Thm PR2^β** (written proof modulo the same uniform Denisov–Wachtel wedge bound r14 already cites). It adds
  a *quadrant phase* to the squeeze, which shrinks the superset by m^{−1/3}, where m = min(U-side length, V-side
  length). It closes:
  - every **balanced** case (U-part and V-part length tails with the same exponent), for every k;
  - k = 2 whenever the lighter tape also carries a critical block (its length tail is ≥ y^{−1/2}).
- **Open:** unbalanced tapes. The heavier tape has exponent 2^{−k}, the lighter has 2^{−j} with j < k (or is
  exponentially light), except (k, j) = (2, 1). k = 2 with an exponentially light tape is **exactly borderline**
  (N^{1/4} vs N^{1/4}).
- T8_unamb stays **OPEN**.

Scripts:
- `scripts/r15_tails_stack.py` → `r15_tails_stack_out.txt`: stacked grammars, exponents.
- `scripts/r15_tails_cone.py` → `r15_tails_cone_out.txt`: exact DP for the quadrant-then-wedge law.

## 1. Citation check (Banderier–Drmota) [checked against the source]
Source: Banderier & Drmota, "Formulae and asymptotics for coefficients of algebraic functions", CPC 24 (2015);
I read the DMTCS/FPSAC 2013 version (dmtcs.episciences.org/2366).

**Theorem 3 ("dyadic critical exponents for N-algebraic functions").** The critical exponent of an N-algebraic
(even R₊-algebraic) function is either 2^{−k} for some k ≥ 1, or −m·2^{−k} for some m ≥ 1 and k ≥ 0.
- In the aperiodic case, f_n ~ Aρ^{−n}n^{−1−α}.
- In the periodic case the same holds within each residue class.
- Prop 1: every value occurs. The witness is y₁ = z(y₂ + y₁²), y₂ = z(y₃ + y₂²), y₃ = z(1 + y₃²), which gives (1−2z)^{1/8}.
  That is a stack of **nonlinear** SCCs.

Consequence for us: a block with μ(B) < ∞ and radius ½ has coefficients n^{−1−2^{−k}}. The other branch,
n^{−1+m2^{−k}}, has divergent μ. So the r13/r14 statement of the exponent set is **correct**, provided "per residue
class" is added for periodic blocks.

## 2. Lemma ST (where heavy tails come from) [(i) written proof; (ii) B–D mechanism, checked numerically]
(i) If μ(B) < ∞, then no SCC reachable from B is linear with ρ(M(½)) = 1.

*Proof.* Such an SCC satisfies Y = A + M Y at z = ½. Here A(½) ≥ 0 and A(½) ≠ 0, because a reduced grammar has
exits. Let w > 0 be the left Perron vector of M. Then w(I − M)μ = 0, but wA > 0. So μ(Y) = ∞, and μ(B) ≥ 2^{−|st|}μ(Y) = ∞. ∎

(ii) So B's exponent 2^{−k} comes from k critical **nonlinear** SCCs stacked along a dependency chain. Each one turns
an input singularity (1−2z)^{β} into (1−2z)^{β/2}, by Y−τ ∝ √(input). Subcritical SCCs, linear or not, pass the
exponent through.

**This corrects r14 §5.2.** The critical *linear* SCC is the C of PR2, sitting *above* the heavy block. Its renewal
mass is N^{β} (check: X = 1 + (x/2)Y₂X has coefficient n^{−3/4}).

Numerical check (`r15_tails_stack_out.txt`, n ≤ 4096). Local exponents, n = 256 → 4000:

| series | definition | local exponent | target |
|---|---|---|---|
| D | 1 + z²D² | −1.4875 → −1.4992 | −3/2 |
| Y₂ | 1 + z³DY₂² | −1.164 → −1.200 | −5/4 |
| Y₃ | 1 + z³Y₂Y₃² | ≈ −1.03 | −9/8 |
| X | linear critical over Y₂ | −0.770 → −0.754 | −3/4 |
| Xₛ | linear subcritical over Y₂ | −1.10 → −1.15 | −5/4 |

- Y₂ and Y₃ converge slowly, because the correction terms are only n^{−1/4} (resp. n^{−1/8}) smaller. The drift is
  monotone towards the target.
- U(N)/N^{1/4} = 1.157, 1.095, 1.048 for N = 256, 1024, 4096, which is consistent with Θ(1).

## 3. Prop S (no-go for idea (2)) [written proof + cited DW asymptotic]
The squeeze's upper bound is a count of **uniform letter words**, and |G⁻_n ∩ Valley_C| ≍ 2ⁿn^{−2/3}. The lower
bound holds because DW gives P(τ > m) ~ κV(x)m^{−p/2} exactly, and the DP gives m^{2/3}P → 0.332 (r14 audit, and the
m = 0 row here).

Hence **no** argument whose only input is "L ⊆ G⁻ ∩ Valley_C" can exclude a language of density n^{β−1} with β ≤ 1/3.
The increment law of L enters only through the lower (renewal) bound. Under L's own measure, the cone survival is 1,
since L ⊆ cone deterministically. So stable-law or Lévy cone exponents are irrelevant to the squeeze. The superset
itself has to shrink, using L's structure. §5 does exactly that.

## 4. Idea (1) (open up the block) [observation]
By Lemma ST(i) there is no critical linear SCC inside a heavy block. The only critical linear structure there is the
*spine* of the top nonlinear SCC Y_k (Y_k ⇒ αY_kβY_kγ, with spine loops (αTβ, γ) or (α, βTγ), T ∈ L(Y_k)).
- It is not injective: a pointed tree has multiplicity ≍ #Y_k-nodes.
- Its loops contain whole Y_k-blocks, so its renewal has the **same** tail 2^{−k}.
- The leftmost-spine (injective) version is subcritical: its loop weight is ½ at the critical point.

So going "one level down" does not improve the renewal exponent. I found no way to use it.

## 5. Theorem PR2^β (quadrant phase) [written proof modulo the uniform DW wedge bound, as in r14 §4]
**Setting.** As in PR2:
- a critical linear SCC C with i.i.d. tokens (u, v) ~ π;
- a U-level block and a V-level block in C-rules, so both MS bounds hold: A(k) ≤ C_U for k ≤ ℓ_U := |pU| and
  B(k) ≥ −C_V for k ≤ ℓ_V := |Vq|;
- L ⊆ G⁻ and injectivity;
- token-length tail F̄(y) ≍ y^{−β} with β = 2^{−k}.

Put M(W) := min(ℓ_U, ℓ_V) ≤ n/2.

**Lemma QW.** The set of W ∈ {a,b}ⁿ ∩ G⁻ ∩ Valley_C with (A, B)(k) ∈ Q := {A ≤ C, B ≥ −C} for all k ≤ m has
density ≤ c_C m^{−1/3}n^{−2/3}.

*Proof.*
1. If m > n/4, then P(τ_Q > m) ≤ c m^{−1} ≤ c′m^{−1/3}n^{−2/3}.
2. Otherwise, apply the Markov property at m, and in phase 2 the uniform bound
   P_x(τ_{W_i} > t) ≤ C(1+|x|)^{4/3}t^{−2/3} for each Valley wedge W_i (3π/4).
3. That leaves E[(1+|X_m|)^{4/3}; τ_Q > m]. In Q, A and B are *independent* one-dimensional walks (disjoint letters).
   Hölder gives E[|A_m|^{4/3}; τ^A > m] ≤ E[A_m²; τ^A > m]^{2/3}·P(τ^A > m)^{1/3}.
4. Optional stopping for A_{k∧τ}² − (k∧τ)/4 gives E[A_m²; τ > m] ≤ ¼·Σ_{k<m}P(τ > k) ≤ c√m. Reflection gives
   P(τ > m) ≤ c m^{−1/2}.
5. So the expectation in step 3 is ≤ c(√m)^{2/3}(m^{−1/2})^{1/3}·m^{−1/2} = c m^{−1/3}. ∎

Check (`r15_tails_cone_out.txt`, exact DP, T = n/2 = 512): m^{1/3}T^{2/3}P = 0.48, 0.53, 0.57, 0.60, 0.615 for
m = 4 … 64. That is stable and slowly converging. In one dimension, √m·P(τ > m) = 0.797 and E[S²; τ>m]/√m ≈ 1.5.

**Lemma Bal (γ-balance).** For each side s ∈ {U, V}:
- let β_s be the exponent of the s-part length tail, π(|s| > y) ≍ y^{−β_s};
- put β_s := 1 if that tail is exponential;
- assume π(s ≠ ε) > 0 (the two-tape case; the one-tape case is §6).

Let γ := β / max(β_U, β_V), where β = min(β_U, β_V). Then for some c > 0, the renewal mass of sequences with total
length ≤ N and M ≥ cN^{γ} is ≥ cN^{β}.

*Proof.*
1. Lemma R gives U(N) ≥ c_R N^{β}.
2. Sequences with r < εN^{β} tokens have mass ≤ εN^{β}, since each fixed r has mass ≤ 1.
3. Sequences with r > LN^{β} and length ≤ N have mass ≤ Σ_r exp(−r F̄(N)) ≤ C N^{β} e^{−cL}.
4. For r ≤ LN^{β} tokens and x = (r/K)^{1/β_s}: P(ℓ_s < x) ≤ exp(−r·π(|s| ≥ x)) ≤ e^{−cK}, because a sum is at
   least its largest term. For β_s = 1, Chernoff on #{s ≠ ε} does the same job.
5. Choose ε small, then L and K large. ∎

**Theorem PR2^β.** If β > (1 − γ)/3, the pair map is not injective.

*Proof.*
1. Lower bound: injectivity and Lemma Bal give word mass ≥ cN^{β}, carried by words with n ≤ N + |pwq| and
   M ≥ cN^{γ}.
2. Upper bound: those words satisfy Lemma QW with m = cN^{γ}, so their mass is ≤ Σ_{n≤N} c m^{−1/3}n^{−2/3} = O(N^{(1−γ)/3}).
3. These are incompatible when β > (1 − γ)/3. ∎

**Coverage**, with β = 2^{−k} and lighter-side exponent 2^{−j} (j < k), or j = 0 meaning β_max = 1.
The condition reads 2^{j} > 2^{k} − 3.
- **Balanced** (j = k): γ = 1, so every k is covered. A typical L-word then has both sides of length ≍ n, and the
  quadrant costs n^{−1}.
- **k = 2, j = 1**: γ = ½, and ¼ > 1/6. Covered.
- **k = 2, j = 0**: ¼ = ¼. **Borderline**: the squeeze is off by a constant only.
- **k ≥ 3, j < k**: not covered.
- With the conditional-moment refinement, the cone phase would give m^{−4/3}·…. That is not applicable here, since
  Q is a quadrant (π/2) and not a π/4 cone.

Caveat: Lemma Bal needs both a lower and an upper side-tail bound with exact exponents. B–D Thm 3 gives regular
n^{−1−2^{−j}} asymptotics per residue class. The tail of a *token* side-length is a finite mixture of products of
block tails, so its exponent is the minimum one [standard; not written out].

## 6. One-tape and remaining cases
- **One-tape** (v ≡ ε, or u ≡ ε): PR1 (r13 §5) uses only μ(L) = ∞, not a rate. So it holds for **all** k.
- **Exact remaining gap:** two-tape, unbalanced, and the heavier tape of exponent 2^{−k} with k ≥ 3 (any lighter
  j < k), or k = 2 with an exponentially light tape (borderline).
  - A typical word there has ℓ_light ≍ N^{γ} with γ = 2^{j−k}, and the quadrant phase is too short.
  - A fix needs a superset of density o(n^{2^{−k}−1}) for words with one side of length n^{γ}. For example: use the
    i.i.d. token structure *inside* the long side (all token orders lie in L), which Q ignores.
- T8_unamb stays OPEN, with this gap and the side-mismatch and one-sided items of R15-A and R15-C.

F1 check: everything uses G⁻ and Valley geometry (wedges and quadrant), which the language Q (density 1) does not have.

## Status
| claim | label |
|---|---|
| B–D Thm 3 exponent set; finite-μ ⇒ n^{−1−2^{−k}} | checked against source |
| r14 "heavy tails from critical linear SCCs" | **false**; Lemma ST: stacked critical nonlinear SCCs |
| Lemma ST(i): no ρ = 1 linear SCC below a finite-μ block | written proof |
| Prop S: no squeeze through G⁻ ∩ Valley_C alone for β ≤ 1/3 | written proof + cited DW |
| Idea (1) (open the block) | no-go observation |
| Lemma QW: quadrant-then-wedge density m^{−1/3}n^{−2/3} | written proof modulo uniform DW wedge bound; DP check |
| Lemma Bal | written proof (tail regularity cited) |
| **Thm PR2^β**: balanced tapes, all k; k = 2 with j = 1 | written proof modulo DW |
| Unbalanced k ≥ 3; k = 2, j = 0 (borderline); T8_unamb | **OPEN** |
