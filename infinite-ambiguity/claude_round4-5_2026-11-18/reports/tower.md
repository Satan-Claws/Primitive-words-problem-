# Report of agent "tower": the unbounded tower N_∞, its grammar form, and mixed depth

**Claim status.** No proof of either resolution is claimed, and I did not find a CF L ⊆ Q of positive density.
Scripts are in `infinite-ambiguity/claude_round4-5_2026-11-18/scripts/tower/`:
- `tower.py`: N_∞ exhaustive up to n = 19, and Monte Carlo;
- `mixed.py`: the mixed-depth grammar;
- `collapse.py`: streaming machines.

## 1. N_∞ = Cyc(L′) (PROVED)
Define L′ as the least language with E′ ⊆ L′, σ(L′) ⊆ L′ and swap σ(L′) ⊆ L′. There is no inner rotation.

- **Soundness (PROVED).** walk's Lemma 3 proves σ(M) ⊆ Q for every M ⊆ Q, and that proof never uses Cyc. By induction on length, L′ ⊆ Q.
- **Rotation identity (PROVED).** Cyc σ(M) = Cyc σ(Cyc M). By the cycle lemma, the D canonical rotations of w have as type words exactly the D rotations of Φ(w).
- **Consequence.** Cyc(L′) = N_∞, the least N with N = E′ ∪ T(N).
- So **if L′ is CF, then N_∞ is CF, and N_∞ has positive density.**
- L′ is the language of uniform-depth substitution trees, an ET0L-type language with two tables, σ and swap∘σ. Its natural grammar needs one nonterminal per depth.

## 2. Density of N_∞ (COMPUTER-CHECKED)
- **Exhaustive check:** 0 non-primitive words for n ≤ 19. Density on odd n is 0.984 at n = 9, 0.966 at n = 15 and 0.959 at n = 19.
- **Monte Carlo:** density is 0.9465, 0.949, 0.948 and 0.947 at n = 101, 1001, 10001 and 100001.
- **The limit is a constant < 1.** The losses are towers that reach a unary type word, for example bbb, at small levels.
- **Depth.** The typical depth is about log log n, and the depth distribution at n = 10^5 is concentrated on 2–4.
- **Unbounded depth is needed (follows from walk).** The words of depth ≤ k lie in a finite union of T^j(E′), whose density is O(n^{-2^{-(k+2)}}). So any positive-density sub-certificate of N_∞ needs unbounded depth.

## 3. Mixed depth is unsound (COUNTEREXAMPLE, COMPUTER-CHECKED)
Let X → b | Z a, where Z is a nonempty Dyck word over (X, a). Substituting X for b in E′, then taking Cyc and swap, gives a CF language.
- It is not contained in Q: (aab)^3 and (abb)^3 lie in it at n = 9.
- It covers 2^n − 2 words on odd n, which is everything except the unary words.

The deterministic "collapse" variant also fails. It restores only one fresh level after a cascade instead of j fresh levels (the COL mode of `collapse.py`). It accepts a^n for every n ≥ 2.

The absolute-level variant (the ABS mode) is sound for n ≤ 9.

**Diagnosis.** Unique decoding needs the absolute level count. In the PDA, a letter that cascades through j fresh levels must restore j markers above a modified counter, which is a second unbounded counter.

## 4. Unions of towers
- A union of T^k(E′) over k ≤ K is CF for every fixed K, but its density is still → 0.
- The union over all k is N_∞. Its CF status equals the open question.
- No CF realization was found. Both natural relaxations, mixed depth and collapse, lose soundness, and the failure starts at n = 9 for mixed depth and at n = 2 for collapse.

## Registry entry
1. **Aimed at:** a CF L ⊆ Q of positive upper density, as a stepping stone to a cycle-free G with L(G) = Q.
2. **Proved:**
   - L′ ⊆ Q.
   - N_∞ = Cyc(L′).
   - Bounded-depth parts of N_∞ have density → 0.
   - **Computer-checked:** N_∞ has density ≈ 0.947 and is sound for n ≤ 19.
3. **Missing step:** either
   - (a) a CF L ⊆ N_∞ (or a CF L ⊆ Q) with lim sup |L_n|/2^n > 0, which needs unbounded tower depth with absolute levels; or
   - (b) "N_∞ is not CF" (CONJECTURED). Bounded slices look semilinear, so this needs an unbounded-slice or Ogden argument.
4. **Counterexamples:** (aab)^3 for mixed depth; a^n for the collapse variant.
5. **Strength:** (b) is weaker than "Q not CF". Even a CF N_∞ would not give Q, because N_∞ misses about 5% of words.
6. **What would reopen the route:** a decoding that is unique without absolute levels, for example codes marking the level, or a homogeneous functional f(x^p) = p f(x) with O(1) typical values and CF level sets.
