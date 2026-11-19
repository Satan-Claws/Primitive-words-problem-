# Round 4 — agent "thue": cube-free near-powers against free-loop iteration (Theorem A′)

**I do not claim a proof of either resolution.**

The task was to build primitive words W_p = (cube-free root u)^k with a defect, mark only a cube-free region, and
force every Theorem A′ decomposition (ogden.md) to produce a proper power.

**Outcome:** a barrier. The defender (the side choosing the decomposition) escapes on every instance I tested. Each
escape is certified *exactly*, for all sequences c ∈ [m]* of unbounded length, not by a bounded search.

I also prove the lemmas that explain the escape and that turn "does this window escape?" into a finite,
decidable question.

Scripts are in `infinite-ambiguity/claude_round4-5_2026-11-18/scripts/thue/`:
- `common.py`: certificates and the exact decision procedure;
- `survey.py`, `check_escape.py`, `stats.py`: the instance surveys;
- `validate.py`: a brute-force cross-check;
- `hard.py`: an earlier attack search.

Each script runs in under 30 s on one core.

## 0. Setting

Theorem A′ (ogden.md §1) gives w = u v₁⋯v_m z x_m⋯x₁ y. Each v_jx_j carries a mark, and
u v_{c₁}⋯v_{c_r} z x_{c_r}⋯x_{c₁} y ∈ L for every c ∈ [m]*.

The defender may take every x_j = ε. Such a decomposition is an admissible choice of the theorem: it arises when
the loops' right parts are empty, and the defender only needs to exhibit one decomposition.

With all x_j = ε, write W = α g β, where g = v₁⋯v_m is the "window", and set r = βα. Let M = {v₁,…,v_m}*. The
generated words α σ β (σ ∈ M) are conjugates of σ r. So:

> the window **escapes** ⇔ σ r is primitive for every σ ∈ M (σ = ε included).

## 1. Lemmas (all PROVED)

**L-UC (unique circular factor).** Let a circular word C of length N contain some word δ (|δ| ≤ N) at exactly one
circular position. Then C is primitive.

*Proof.* If C = t^e with e ≥ 2, rotation by |t| permutes the circular positions. It has no fixed point (since
0 < |t| < N) and it maps occurrences of δ to occurrences of δ. Its orbits all have size e, so the number of
occurrences is a multiple of e ≥ 2, which is not 1. ∎

**L-UF (unique-factor escape).** Suppose δ occurs exactly once in r (as a linear factor), |r| ≥ 2|δ| − 2, and δ is
not a factor of s σ p for any σ ∈ M. Here s is the suffix of r of length |δ|−1 and p is the prefix of r of
length |δ|−1. Then the window escapes.

*Proof.* Take a circular occurrence of δ in σ r.
- Either it lies inside the linear segment r,
- or it contains a letter of σ or crosses a boundary between σ and r (for σ = ε, the junction end(r)→start(r)).
  In that case it extends at most |δ|−1 letters into r on each side, so it is a factor of sσp.

So the number of occurrences is 1 + 0, and L-UC applies. ∎

The condition "δ ∉ Fact(sMp)" is decidable: run the KMP automaton of δ over s, then over the regular set M, then
over p (`delta_free`).

**L-PAR (Parikh escape).** Suppose ψ(v_j) = c_j(α,β) for all j, with gcd(α,β) = 1, and
gcd(A + nα, B + nβ) = 1 for every n in the numerical semigroup ⟨c_j⟩, where (A,B) = ψ(r). Then the window escapes.

*Proof.* We have ψ(σr) = (A + nα, B + nβ). A power t^e has both letter counts divisible by e. ∎

Special case: if all loops are balanced (|v|_a = |v|_b) and |W|_a − |W|_b = ±1, then every window escapes. This
covers, for example, letter-insertion defects in Thue–Morse-coded words, using aligned loops from {ab,ba}⁺.

**L-PS (structure of a power-producing σ).** Suppose σ r = t^e with e ≥ 2 and n = |r|. Then one of the following
holds:
1. |t| ≥ n, and then r ∈ Fact(σ) ⊆ Fact(M); or
2. P := |t| < n, P is a period of r, t is the suffix of r of length P, and σ is the prefix of t^ω of length
   eP − n ≥ 2P − n.

*Proof.*
- If |t| ≥ n, then t = t′r and σ = (t′r)^{e−1}t′.
- Otherwise r is a suffix of t^e longer than t, so r has period |t|, and the rest follows by reading t^e. ∎

**Corollary (exact decision, PROVED; implemented as `full_escape`).** Suppose r ∉ Fact(M); this is decidable by
running r's KMP automaton over M. Then the window escapes iff, for no period P < n of r, does the text t^ω admit
an M-parse reaching a position pos with pos ≡ −n (mod P) and pos ≥ 2P − n.

For each P this is a reachability question over the finite state set (pos mod P, pos below 2P − n?), so the
procedure is exact and covers all σ, with no truncation.
- When r ∈ Fact(M), the procedure answers "undecided"; this never happened in the escapes below.
- Cross-check (`validate.py`): on 3000 random (r, loops) pairs it agreed with brute force (|σ| ≤ 14) in all 2100
  decided cases. There was no case "escape claimed but brute force found a power".

**L-μ (Thue–Morse renormalisation).** Let μ: a↦ab, b↦ba. Then μ(x) is primitive ⇔ x is primitive.

*Proof.* Suppose μ(x) = t^e with e ≥ 2.
- If |t| is odd, then e is even, so μ(x) = (t²)^{e/2} with |t²| even.
- A root of even length is a prefix of μ(x) at even alignment, hence equal to μ(y) for some y. Then x = y^{e′}
  by injectivity of μ on aligned blocks. ∎

Consequence: if the marked region, the window and the complement are all μ-aligned, the defender may choose
μ-images as loops. The A′ game on μ(V) then reduces exactly to the game on V. Thue–Morse structure therefore gives
the attacker no leverage that the preimage did not already have.

## 2. The "defect duplication" idea, rigorously

Say the defect lies in r, i.e. the defender's window avoids it. By L-PS, a power-producing σ must do one of two
things:
1. contain all of r (case 1), in which case the defect pattern must be produced inside an M-product; or
2. be the length-(eP−n) prefix of t^ω, where P is a period of r. For a single-letter defect at position d of r,
   any period P that is a multiple of the root length must satisfy P > max(d, n−d) (IDEA-level for general
   defects). Then t contains the defect, and σ must spell the corresponding piece of t: again a copy of the defect
   inside an M-product.

So the attacker must force the loops of every window to generate the defect's neighbourhood. The loops are chosen
by the defender after seeing W and the marks, and windows can be placed anywhere among the marks. The attacker
has no means of forcing this.

If the marks cover the defect, the defender either places the window away from the defect, or keeps the defect
inside the window and picks loops whose monoid cannot repair it. Both happen in the data (`stats.py`). Between 89%
and 99.8% of instances escape with a window that avoids the defect, and the remaining instances escape with a window
containing it.

## 3. Computation (COMPUTER-CHECKED; exact for all σ ∈ M, finite instance sets)

Setup for the surveys:
- W = U^k with one defect: a letter flip, an insertion of a or b, or a deletion, at every position. Only primitive
  W are kept.
- Marks D = every interval of length ρ (every start position).
- m = 3 loops, window length ≤ ρ+4.
- An instance counts as a success if some x = ε window satisfies `full_escape` = True.

| U (mirror-symmetric = conjugate to its reversal?) | k | ρ | instances | escapes certified |
|---|---|---|---|---|
| abbabaab (TM₈, mirror) | 2 | 6 | 720 | 720 |
| abbabaab (mirror) | 3 | 6 | 1848 | 1848 |
| abbaba (non-mirror) | 3 | 6 | 954 | 954 |
| abbabaa (non-mirror) | 3 | 6 | 1365 | 1365 |
| aababb (non-mirror) | 3 | 6 | 954 | 954 |
| abaabb (non-mirror) | 4 | 6 | 1848 | 1848 |
| abbabaabba (non-mirror) | 3 | 8 | 2790 | 2790 |
| abbabaabbaab (mirror) | 3 | 8 | 4212 | 4212 |
| aabababb (non-mirror) | 3 | 6 | 1848 | 1848 |
| TM₁₆ (mirror) | 2 | 8 | 3232 | 3232 |

There were **no failures** in 19,771 instances, and this includes non-mirror roots, as the coordinator's CL1 note
required.

How the escapes are certified:
- Most escapes are certified by L-PAR or L-UF alone (`survey.py`: e.g. TM₁₆, k = 3: 1884 PAR + 180 UF of 2064).
- The rest need the period analysis of the Corollary.
- The certified escaping windows use short, non-commuting loops, for example (a, bb, baba) or (abba, b, ab). This
  is exactly the "fresh non-commuting loops" behaviour that ogden.md reported, now with unbounded certificates.

## 4. Conclusion / barrier

The proposed witness shape, "cube-free power with a defect, marks in a cube-free region", does not defeat A′ on
any tested instance. L-PS shows why: making the word a power requires an M-product to reproduce or erase the
defect's neighbourhood (or all of r). The defender picks the loops, and, by L-μ, cube-free / Thue–Morse structure
can be renormalised away.

**CONJECTURED (barrier E).** For every primitive W, every m, and every mark set D with |D| ≥ C(m), some x = ε
window in A′ escapes.

If barrier E is true, then no A′-based argument (with any witness family) can prove Q not CF. Barrier E is
consistent with ogden.md's Theorem B: per-word iteration is a strict weakening of CF-ness.

## Registry entry (thue)
1. **Aim:** a family W_p (cube-free near-power with a defect, marks in a cube-free region) such that every A′
   decomposition (m free loops) yields a proper power for some c ∈ [m]*. This would give Q ∉ CF.
2. **Proved:**
   - L-UC: a unique circular factor implies primitivity;
   - L-UF: unique-factor escape criterion, decidable;
   - L-PAR: Parikh escape, including the balanced-loops / imbalance ±1 case;
   - L-PS: structure of power-producing σ, giving an exact decision procedure for the escape of a window with
     x = ε;
   - L-μ: Thue–Morse renormalisation of the game.
3. **Missing step:** ∃m ∀p ∃ primitive W with marks D (|D| ≥ p) such that for every x = ε window of m loops each
   containing a mark (and also every window with x_j ≠ ε), some σ ∈ M makes σr a proper power. By L-PS, this is
   equivalent to forcing every window's monoid M to contain r as a factor, or a period-P prefix of t^ω of the
   right length.
4. **Counterexamples:** all 19,771 tested instances escape with exact certificates, so the proposed family fails
   at every tested size. This includes non-mirror roots.
5. **Strength:** the missing step is stronger than "Q not CF". Evidence (barrier E) says it is false.
6. **Reopen if:** an iteration theorem in which loops are transplanted into other contexts (cross-word, as in
   ogden §4.6b). Within a single word, the defender's choice of loops always escapes in our data.
