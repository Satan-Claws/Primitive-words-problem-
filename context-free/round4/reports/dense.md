# Report of agent "dense": the (Q½) density question

**Claim status: no proof of either resolution.** I found no CF L ⊆ Q of density ≫ n^{-1/2}. I give three results:
- (A) An explicit **non-CF** certificate language W ⊆ Q with **positive density**. It is sound (PROVED). Its density is ≈ 0.66–0.8 (COMPUTER-CHECKED) and bounded below by a constant (PROVED via Donsker). So any proof of (Q½) must use context-freeness essentially, not only "every certificate is sound".
- (B) **Theorem P^R** (PROVED): Theorem P extends to *regular ∩ k-gram-count* languages. Every power-free L = R ∩ V_k^{-1}(S), with R regular and S semilinear, has |L_n| = O(2^n n^{-1/2}). This class is strictly larger than CS_k ∪ FR-type classes.
- (C) The analysis of why every natural dense certificate needs "two counters", and the precise missing lemma (CRH).

Scripts are in `context-free/round4/scripts/dense/`:
- `window.c`: exhaustive check, n ≤ 22, about 1 min;
- `mc.c`: Monte Carlo up to n = 2001.

Notation: a = +1, b = −1, S_t is the prefix walk of w, extended periodically by S_{t+n} = S_t + D with D = Δ(w).

## A. A positive-density certificate (sound, apparently not CF)

**Definition.** w ∈ W iff one of the following holds:
- (W+) D ≥ 1 and ∃ i: S_t ≤ S_i for all t ∈ (i, i+⌊n/2⌋];
- (W0) D = 0 and ∃ i: S_t < S_i for all t ∈ (i, i+⌊n/2⌋];
- (W−) D ≤ −1 and ∃ i: S_t ≥ S_i for all t ∈ (i, i+⌊n/2⌋].

**Soundness (PROVED).** Suppose w = u^p with p ≥ 2 and d = n/p ≤ ⌊n/2⌋. Then S_{i+d} = S_i + e with e = Δ(u) = D/p.
- If D ≥ 1, then e ≥ 1, so S_{i+d} > S_i. This contradicts (W+) at t = i+d.
- If D = 0, then S_{i+d} = S_i, which contradicts (W0).
- (W−) is the mirror image of (W+).

Fact used: a window of length ⌊n/2⌋ contains i+d for *every* proper period d at once. This is the "all primes at once" mechanism that mismatch certificates lack.

**Positive density (PROVED, standard).** If the first argmax i of S on [0,n] satisfies i ≤ n/2 and S_n ≥ 1, then (W+) holds at i. By Donsker, P(argmax ∈ [0,½], B_1 > 0) > 0 for Brownian motion, and the argmax functional is a.s. continuous. So liminf |W_n|/2^n > 0.

**Data (COMPUTER-CHECKED, `window.c`, exhaustive).**
- W contains no non-primitive word for any n ≤ 22.
- Density of W: n = 19: .7515, 20: .7658, 21: .8041, 22: .7140.
- For comparison, E′·√n ≈ 0.77 (odd n).
- Monte Carlo (`mc.c`, 4000 samples each): n = 100: .703, n = 401: .679, n = 1000: .662, n = 2001: .661.

**Why W is (very probably) not CF (IDEA, not proved).** The certificate needs three things at once:
- a walk constraint on the window, which needs a counter;
- a length comparison "window ≥ n/2", which needs a fold or second counter;
- a sign for D.

Natural reformulations that look cheaper do not avoid this:
- replacing length by |y|_b > |x|_b (also sound, since a window shorter than d holds ≤ |u|_b b's);
- taking the window to be a first-passage piece longer than the rest (this also kills all periods).
In each case the walk structure of the window crosses the pairing that measures its length. With a single counter, every variant collapses to D ∈ {0, ±1}-type certificates, which have density n^{-1/2}.

Builder's n/6 half-imbalance certificate is the same phenomenon: it needs a fold plus a count. Combinations tried that stay CF all have density O(n^{-1/2}):
- "exactly one first-passage piece in a regular R": sound, CF. The weight is concentrated on D = O(1), so the density is O(n^{-1/2}).
- Δ ∈ {±1,±2} together with a non-square check: sound, but probably not CF, and n^{-1/2} anyway.

## B. Theorem P^R: regular ∩ k-gram counts (PROVED)

Let R be regular and S ⊆ N^{Σ^k} semilinear. Let L = R ∩ {w : V_k^lin(w) ∈ S} (linear, non-cyclic k-gram counts). If L contains no proper power, then |L_n| = O(2^n n^{-1/2}).

Examples covered that Theorem P does not cover:
- languages whose regular part enforces order or anchoring, e.g. R ∩ {Δ = 1};
- any count condition combined with arbitrary regular side conditions;
- every L′ ⊆ such a power-free language. This includes Koga's {v⟩ : v Dyck} ⊆ E′, and every CF language contained in one.

*Proof.*
1. **Reduction to cyclic counts.** Split by the first and last (k−1)-letter words α, β (a regular condition, absorbed into R). Then V^lin = V^cyc − W_{αβ}, so the condition becomes V^cyc ∈ S_{αβ} ∩ E, which is semilinear. Write it as a finite union of linear sets M = c + Np_1 + … + Np_r in E.
2. **Rank-deficient M.** These give O(2^n n^{-1/2}) by density4's Lemma AC, unchanged; it is an upper bound and R only shrinks the set.
3. **Full-rank M: setup.** Let I = [Λ_E : ZΛ_M]. Let A be a complete DFA for R, and K the minimal ideal of its transition monoid. Fix a word u, with |u| ≥ k−1, whose action e is an idempotent of K. Let G_e = eKe be the corresponding maximal subgroup.
4. **Claim.** If some w ∈ L ∩ V^{-1}(M) contains u as a factor, then L contains a proper power.
   - (a) Insert h = (uρu)^m right after an occurrence of u, where |G_e|·I divides m. The action of uρu is e·a(ρ)·e ∈ G_e, so the action of h is e. Every state after u lies in Im(e), so the state run is unchanged, and so is the action of the whole word, since a(w_1) e e a(w_2) = a(w).
   - (b) Because |u| ≥ k−1, the cyclic counts change by exactly m·V^cyc(uρu). This lies in mΛ_E ⊆ ZΛ_M.
   - (c) By Eulerian splicing through a ρ_0 that visits every de Bruijn vertex, V^cyc(uρu) = V^cyc(uρ_0u) + λz for any integral z ≥ 0 in E. Choose z in the relative interior of cone(p_i) and λ large. The result is s with: s ∈ R; s ≡ c (mod ZΛ_M); V(s) in the interior of the cone; action of s in K.
   - (d) K is completely simple, so a(s) lies in a group H. Take q ≥ 2 with q ≡ 1 mod lcm(I, |H|). Then a(s^q) = a(s), so s^q ∈ R. Also V(s^q) = qV(s) ≡ c, and for q large it lies deep inside the cone.
   - (e) A finitely generated semigroup contains all points of its group that lie deep inside its cone. Hence V(s^q) ∈ M. Also s^q has the same α, β. So s^q ∈ L, a contradiction.
5. **Conclusion.** Every word of L ∩ V^{-1}(M) avoids u, so there are at most Cλ^n of them with λ < 2. Summing over components gives the bound. ∎

Remark: q need not be prime here. The only arithmetic needed is q ≡ 1 mod I.

## C. What is missing

The gap between B and the target is exactly the "non-count" information that A uses: walk extrema over windows of length ≈ n/2. Reflection dominance and mismatches are the same kind of information, but they are exponentially sparse or tied to a single prime.

**Missing lemma (CRH, CONJECTURED).** For every CF L ⊆ Q there is a power-free count-regular K = R ∩ V_k^{-1}(S) with |L_n \ K_n| = O(2^n n^{-1/2}).

- CRH together with P^R gives (Q½), and (Q½) gives "Q not CF".
- W shows that CRH is false for languages that are merely sound. So any proof of CRH must use context-freeness. Concretely, one must show that no CF language can carry W-type information, i.e. a windowed walk constraint plus a length comparison, on a ≫ n^{-1/2} fraction of words.
- A clean testable sub-question: **is W (or W+ restricted to a regular slice) non-CF?** A proof via a bounded slice and Ginsburg stratification would be the first rigorous instance of "dense sound certificates need two counters".

## Registry entry
1. **Aimed at:** a CF L ⊆ Q with density ≫ n^{-1/2} (would kill the density route), or else (Q½) for a larger class.
2. **Proved:**
   - W ⊆ Q with liminf density > 0. It is not shown to be CF and is probably not CF.
   - Theorem P^R: power-free regular ∩ k-gram-count languages, and all their subsets, have density O(n^{-1/2}).
3. **Missing step:** CRH (§C). Equivalently, (Q½) for arbitrary CFGs. A first test case is "W is not CF".
4. **Counterexamples:**
   - No CF counterexample to (Q½) was found.
   - W is a non-CF counterexample to the "soundness alone forces n^{-1/2}" heuristic (data n ≤ 22, Monte Carlo n ≤ 2001).
5. **Strength:** CRH and (Q½) are STRONGER than "Q not CF".
6. **Reopen or kill:**
   - Kill: a CF implementation of any W-type certificate (windowed walk extremum + length ≥ n/2, or + b-majority) on a ≫ n^{-1/2} fraction of words.
   - Advance: prove W (or a slice of it) is not CF, then generalise to "windowed-extremum" certificates.
