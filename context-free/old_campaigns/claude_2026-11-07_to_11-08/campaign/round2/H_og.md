# Round 2 / H: settling OG(Q) — status report

Researcher H. **Verdict: OG(Q) is not settled in either direction.** Neither (a) nor (b) is achieved. What this report does have:

1. **An exact, annotation-free reformulation (Theorem 1).** OG(Q) holds iff, for every s, Ogden's lemma holds for Q when both ends of each pumped factor must carry equal colours under an *arbitrary* s-colouring of cut points. The prover chooses that colouring after p. This is strictly more power than "regular counters mod m". It removes π and R from the problem.
2. **An exact description of what annotation can and cannot forbid (Theorem 2).** In particular, synchronized partner loops with any prescribed length ratio always survive.
3. **Three rigidity tools, with full proofs.**
   - Lemma U (fresh conjugates): a marked loop with a conjugate absent from z is safe for every i ≥ 1.
   - Lemma 4 (clustering of small-exponent failures).
   - Theorem 5 / 5\* (labelled-sequence and run-skeleton rigidity): for two long small-period runs that are consecutive in the skeleton, at most **one** pair of length changes makes z non-primitive.
4. **The partner principle (Corollary 5.3, rigorous).** Every negative design whose marked pumps sit inside a long small-period run, with another long small-period run reachable within the Ogden window, fails. This includes all the run, counter, wall and block-marker designs suggested for (a), and A's factorial family.
5. **A list of necessary conditions on any counterexample to OG(Q)** (§6). The exact residual gap is stated in §7. It is theorem-strength: it is the "one exponent per candidate, unboundedly many primes" core already met by routes B and E.

Audit note (from the coordinator): the general claim in A that "OG is closed under cyclic shift" is withdrawn. Nothing here depends on it.
- Theorem 1 is a statement about π⁻¹(Q) ∩ R itself.
- The link "closure chain + Ogden refutes Q ⇔ ¬OG(Q)" uses only two facts: any allowed chain is a single rational transduction τ of Q (Q is closed under rotation and reversal), and parts (a) and (b) of A's Theorem A for rational transductions.

Code and outputs are in `/tmp/claude-5714/-home-shobhit--claude-spares-spare-fauO4P/6f48459d-5790-4a18-bccc-eabb8efc4544/scratchpad/r2_og/`. They are evidence only.

Notation.
- z ∈ {a,b}⁺ is primitive, n = |z|. Cut points are 0..n.
- A decomposition (a,b,c,d) with a ≤ b ≤ c ≤ d means v = z[a,b) and x = z[c,d), and z_i = u vⁱ w xⁱ y.
- It is **good** if z_i ∈ Q for all i ≥ 0.
- A cyclic word W is cyclically P-periodic if W[j] = W[j+P mod |W|]. Then W is a power of period gcd(P,|W|). So for 0 < P < |W| it is non-primitive.

---

## 1. Theorem 1: OG(Q) ⇔ CPL(Q)

**Definition (CPL_s).** There is p such that for every primitive z, every D ⊆ [0,n) with |D| ≥ p, and every map χ : {0..n} → [s], there is a good decomposition (a,b,c,d) satisfying:
- vx meets D;
- |vwx ∩ D| ≤ p;
- χ(a) = χ(b) if v ≠ ε, and χ(c) = χ(d) if x ≠ ε ("colour loops").

**Theorem 1.** OG(Q) ⇔ CPL_s holds for every s ≥ 1. (CPL_1 is plain Ogden for Q.)

*Proof.* (⇐) Let π : Δ → {a,b} be letter-to-letter and R = L(A) with A a complete DFA with s states.
- Given ζ ∈ π⁻¹(Q) ∩ R with marks D, put χ(c) = δ(q₀, ζ[0,c)) and z = π(ζ).
- CPL_s gives a decomposition whose v and x are state loops. So ζ_i ∈ R for all i, and π(ζ_i) = z_i ∈ Q.

(⇒) Suppose CPL_s fails. Let Δ = {a,b} × [s] × [s], let π(σ,c,c') = σ, and let R_s be the set of words whose consecutive letters (σ,c,c')(σ',e,e') satisfy c' = e. R_s is regular (a local condition).
- A word ζ ∈ R_s is the same thing as a pair (z, χ): χ(t) is the "after" colour of letter t−1 and the "before" colour of letter t.
- Take (z, D, χ) defeating CPL_s at p, and let ζ be the coded word. Consider any decomposition of ζ meeting Ogden's conditions.
- If v ≠ ε and χ(a) ≠ χ(b), then in ζ₂ the junction inside vv joins after-colour χ(b) to before-colour χ(a). So ζ₂ ∉ R_s. The same holds for x.
- Otherwise v and x are colour loops, so every ζ_i lies in R_s (at i = 0 the junctions u|w and w|y match because χ(a) = χ(b) and χ(c) = χ(d)). By the choice of (z, D, χ), some π(ζ_i) = z_i ∉ Q.

Either way the decomposition fails. So Ogden fails for π⁻¹(Q) ∩ R_s at p, and since this holds for every p, Ogden fails for that language. ∎

**What this changes.** "R cannot count" is replaced by an exact statement: R's power is exactly an s-colouring of cut points, **chosen after p and arbitrary**. The colouring need not be regular or periodic, and it may depend on z. So a negative construction may use non-periodic annotation patterns. A positive proof must beat arbitrary colourings, not only modular ones.

---

## 2. What colourings can and cannot forbid (Theorem 2)

Fix an s-colouring χ. All five statements are pigeonhole arguments.

**(a) Loops are dense.** Among any s+1 cut points, two share a colour. So there is a colour loop between some two of them.
- In particular, among the cut points just before s+1 consecutive marks there is a colour loop containing between 1 and s marks.
- Hence colourings can never make marked loops impossible. They can only make them long in unmarked length, and they can choose which ones exist.

**(b) Period-aligned loops.** For any cut point c and any π ≥ 1, among c, c+π, …, c+sπ two share a colour. So there is a colour loop of length jπ with 1 ≤ j ≤ s. Among c, c+π, …, c+2sπ some colour occurs three times, which gives two colour loops with a common start and different lengths, both multiples of π.

**(c) Synchronized partners (product pigeonhole).** Let c₀ < … < c_{s²} be cut points and f(c) = Δ + μc with μ ∈ ℕ⁺, mapping them to cut points. Colour each c_j by the pair (χ(c_j), χ(f(c_j))). Two indices j < k share the pair, so v = z[c_j, c_k) and x = z[f(c_j), f(c_k)) are simultaneously colour loops with |x| = μ|v|.
- So partner loops with **any fixed ratio** μ, at any fixed offset Δ, always survive.
- With c_j = c + jL and L = lcm(π, π′), this gives equal-length partner loops aligned to two different periods.

**(d) Walls (what *can* be forbidden).** Choose walls w₁ < w₂ < … and colour every cut point strictly between w_t and w_{t+1} with t mod s.
- Then every colour loop crossing a wall crosses at least s walls. So, under dense marking, loops can be confined to segments.
- This is optimal: the first cut points after s+1 consecutive walls contain a repeated colour, so some loop crosses at most s walls.
- Likewise, colouring by position mod m (m ≤ s) inside a segment forces every loop there to have length ≡ 0 mod m. One cannot force divisibility by any m > s, by (b).

**(e) Summary.** The prover can (i) confine loops to segments between walls, (ii) force loop lengths ≡ 0 mod m for m ≤ s, segment by segment, (iii) choose freely where marks go. The prover cannot (iv) remove period-aligned loops of length ≤ sπ in any long π-periodic stretch, or (v) prevent synchronized partner loops of any fixed ratio at any fixed offset, once both regions hold enough cut points.

---

## 3. Large exponents and Lemma U (fresh conjugates)

**Lemma 3 (large i).** Let z = u v y be primitive with 1 ≤ ℓ = |v| < n. If z_i = u vⁱ y ∉ Q for some i ≥ 2, then (i−1)ℓ ≤ n−2.

*Proof.*
- Write z_i = r^q with q ≥ 2, and let P = |r| ≤ n_i/2, where n_i = n + (i−1)ℓ. Suppose (i−1)ℓ ≥ n−1. Then P ≤ (i−1)ℓ + 1/2, so P ≤ (i−1)ℓ.
- Let ρ = |root(v)|. The factor vⁱ has periods P and ρ, and length iℓ ≥ P + ℓ ≥ P + ρ − gcd(P,ρ). By Fine–Wilf it has period g = gcd(P,ρ).
- A factor of v^∞ of length ≥ ρ with period g | ρ makes a conjugate of root(v) a power unless g = ρ. Conjugates of primitive words are primitive, so ρ | P.
- z_i is cyclically P-periodic and contains a factor of length ≥ P with period ρ | P. Hence z_i is cyclically ρ-periodic.
- Deleting i−1 copies of v (each of length ≡ 0 mod ρ) preserves cyclic ρ-periodicity. So z is cyclically ρ-periodic with ρ < n, a contradiction. ∎

**Lemma U.** Let z = u v y be primitive with |v| = ℓ < n. If some conjugate f of v is not a cyclic factor of z, then u vⁱ y ∈ Q for every i ≥ 1.

*Proof.* Fix i ≥ 2. Write z_i cyclically as v₁ v₂ ⋯ vᵢ C with C = yu, and let J_t be the junction between v_t and v_{t+1} (t = 1..i−1).

- **Windows away from interior junctions are cyclic factors of z.** Take a cyclic window of length ≤ ℓ that does not strictly contain any J_t. It lies inside some v_t, or inside the stretch vᵢ C v₁ ≅ vCv. Every window of length ≤ ℓ ≤ n inside vCv is a factor of (vC)(vC), hence a cyclic factor of z.
- **f occurs at every interior junction.** f is a conjugate of v and not a factor of z, so f = v[e,ℓ)v[0,e) with 0 < e < ℓ. It therefore occurs at each J_t, starting at J_t − ℓ + e.
- **f occurs only there.** By the first point, every cyclic occurrence of f strictly contains some J_t. So its start lies in [J₁−ℓ+1, J_{i−1}−1]. Hence the occurrence set S is nonempty and lies in an arc of diameter (i−1)ℓ − 2.
- **Contradiction.** If z_i = r^q, then S is invariant under rotation by P = n_i/q. So S contains q points spaced P apart, and any arc containing them has diameter ≥ (q−1)P ≥ n_i/2. Thus (i−1)ℓ − 2 ≥ (n + (i−1)ℓ)/2, i.e. (i−1)ℓ ≥ n+4. This contradicts Lemma 3. ∎

**Check.** Exhaustive over all primitive z with |z| ≤ 12 and all factors v (`x2_fresh.py`, i ≤ 3n+6): 0 violations among 69,279 fresh pumps at n = 12. The hypothesis is needed: 2,608 stale pumps at n = 12 have a bad i ≥ 2. For instance, every unary loop in a run is stale; A's factorial family consists of stale loops.

**Consequence.** For fresh marked loops, only i = 0 (deletion) can fail. Lemma U has no two-sided analogue as stated: windows straddling x-junctions can recreate f.

---

## 4. Lemma 4: clustering of small-exponent failures

**Lemma 4a.** Let W, W′ ∉ Q have equal length N and differ only inside a cyclic arc D with |D| ≤ N/6. Then W = W′.

*Proof.* Write W = r^q and W′ = r′^{q′}, with P = N/q and P′ = N/q′, both ≤ N/2. On the complementary arc A (length ≥ 5N/6), W|A = W′|A has linear periods P and P′.
- **Case P = P′.** Each residue class mod P has N/P ≥ 2 points spaced P apart. An arc of length |D| < N − P contains fewer than N/P of them, so every class meets A. Both words are constant on classes, so W = W′.
- **Case P ≠ P′.** P + P′ ≤ 5N/6 ≤ |A|. By Fine–Wilf, A has period g = gcd(P,P′). A contains a length-P window of W, so W is cyclically g-periodic; likewise W′. Every class mod g meets A, so W = W′. ∎

**Lemma 4 (clustering).** Fix ℓ and i ∈ {0} ∪ {2,3,…}. Let v = z[α,α+ℓ) and v′ = z[α′,α′+ℓ) with α < α′. Suppose both one-sided pumps fail at exponent i, and that α′ − α + max(i−1,0)·ℓ ≤ n_i/6. Then z[α, α′+ℓ) has period ℓ.

*Proof.* z_i(α) and z_i(α′) agree outside D = [α, α′ + max(i−1,0)ℓ). (Check directly: z_i(α) = z[0,α) v^{i−1} z[α,n).) By Lemma 4a they are equal.
- For i ≥ 2, cancelling the common prefix and suffix gives v^{i−1}Y = Y v′^{i−1} with Y = z[α,α′). So Y is a prefix of v^∞, and then so is Yv′ = z[α, α′+ℓ).
- For i = 0, z[α+ℓ, α′+ℓ) = z[α, α′). ∎

So, for fixed (ℓ, i) with small i, the failing windows of length ℓ all lie in one ℓ-periodic stretch. In a region with no factor of period ℓ and length ≥ 3ℓ, they lie within distance < 2ℓ of each other.

---

## 5. Run-skeleton rigidity and the partner principle

### 5.1 Labelled-sequence rigidity

**Theorem 5.** Let R ≥ 2 and h : ℤ_R → X (any set). Let S = {j}, or S = {j, j′} with R ≥ 3 and j′ ≠ j + R/2 (non-antipodal). Then **at most one** h′ that agrees with h off S has a proper period (some d | R with d < R and h′ ∈ P_d).

*Proof.* Suppose h′ ∈ P_d and h″ ∈ P_{d′} both agree with h off S.

**Case d = d′.** Each d-class has R/d ≥ 2 elements. It cannot lie inside S: for |S| = 1 it has more elements than S, and for |S| = 2 that would force the class to be {j, j+R/2}, the antipodal pair. So each class has an element off S, where h′ = h″. Since both are constant on classes, h′ = h″.

**Case d ≠ d′.** One of the two is ≤ R/3; say R/d ≥ 3. (For |S| = 1, R/d ≥ 2 suffices.) Let g = gcd(d,d′). We show h′ is constant on each coset C of gℤ_R.
- Build a graph on C. Edges m—m+d are always present. Edges m—m+d′ are present when m, m+d′ ∉ S.
- h′ is constant along both kinds of edge. Along d-edges, h′ ∈ P_d. Along a permitted d′-edge, h′(m) = h″(m) = h″(m+d′) = h′(m+d′).
- **Connectivity.** Contract the d-cosets inside C to c = d/g super-vertices. d′-steps move between super-vertices along a cycle, because d′/g is a unit mod c. Each link of the cycle carries R/d parallel edges (2R/d when c = 2). At most 2|S| ≤ 4 edges are blocked.
  - For c ≥ 3, disconnecting needs two fully blocked links, i.e. 2R/d ≤ 4. For c = 2 it needs 2R/d ≤ 4. Both fail when R/d ≥ 3.
  - For |S| = 1 at most 2 edges are blocked, and R/d ≥ 2 suffices.
- So h′ ∈ P_g ⊆ P_{d′}. Then h′ and h″ are both in P_{d′} and agree off S, and the case d = d′ (applied with d′) gives h′ = h″. ∎

**Antipodal pairs.** For an antipodal pair, d = R/2 can give a family of h′ (all with h′(j) = h′(j′)). The divisors d ≤ R/3 still give at most one further h′, by the argument above.

**Check.** `x1_block_rigidity.py`, exhaustive over k ∈ {0..3}^r, r ≤ 8, all site pairs (4.5M cases): no violation. Only the antipodal pairs are degenerate, exactly as stated.

### 5.2 The run skeleton

Fix π₀ ≥ 1.
- A *run* of a cyclic word W is a maximal cyclic interval of length ≥ 2·(its minimal period).
- The **skeleton** Sk(W) is the set of runs with minimal period ≤ π₀ and length ≥ 2π₀, ordered by their starts.
- Item m runs from start_m to start_{m+1}; its *gap word* is g_m = W[start_m, start_{m+1}). So W is the cyclic concatenation of the g_m.

Three facts used below:
- **(F1)** Distinct runs with minimal periods π and π′ overlap in fewer than π + π′ − gcd(π,π′) positions. Otherwise Fine–Wilf and primitivity of the roots force π = π′, and maximality merges them.
- **(F2)** Hence distinct skeleton runs have distinct starts.
- **(F3) W ∉ Q ⇔ (g_m) has a proper period.** (⇐) is immediate. (⇒): rotation by P = |r| preserves runs, so it shifts the skeleton by some index d. Here d ≢ 0, since P ≢ 0, and g_{m+d} = g_m.

**Lemma 5.1 (interior pumping touches one label).** Let σ ∈ Sk(z) have minimal period π and length λ ≥ 4π₀ + 2 + |v|. Pump a factor v with |v| = cπ, lying at distance ≥ 2π₀ + 1 from both ends of σ, to exponent i. (The extra |v| in the bound keeps the length ≥ 4π₀ + 2 after the deletion i = 0.) Then:
- Sk(z_i) = Sk(z) with σ replaced by its lengthened version σ^{(i)}.
- Only the gap word of σ changes: it becomes g_σ with i−1 copies of v inserted at a fixed place. This label family is injective in i (by length).
- The same holds for two distinct skeleton runs pumped simultaneously.

*Proof.* σ^{(i)} is π-periodic, and its maximality depends only on the letters just outside it, which are unchanged.
- Let E be σ's last 2π₀+1 letters, then the rest C of the cycle, then σ's first 2π₀+1 letters. These border words do not depend on i, because the pump is interior.
- By (F1), every other skeleton run of z or of z_i overlaps σ (resp. σ^{(i)}) in < 2π₀ positions. So it lies inside E together with its witnesses of maximality. Periodicity and maximality are therefore read off the same word E in z and in z_i.
- The internal runs of σ have minimal period < π and length < 2π ≤ 2π₀, so they are not in the skeleton.
- A skeleton run starting inside σ starts in its last 2π₀ positions, i.e. after the pump. So only the gap word of σ contains the pumped region.
- σ^{(i)} is never the whole cycle: that would make z_i, hence z, cyclically π-periodic. ∎

**Theorem 5\*.** Let σ ≠ σ′ ∈ Sk(z) satisfy the hypotheses of Lemma 5.1, with periods π and π′ and R = |Sk(z)|. Let z(m₁, m₂) be z with σ lengthened by m₁π and σ′ by m₂π′ (insertion or deletion at the chosen interior points). Let T = {(m₁,m₂) ≠ 0 : z(m₁,m₂) ∉ Q}.
- If R ≥ 3 and σ, σ′ are non-antipodal in the skeleton order (for example, consecutive), then |T| ≤ 1.
- For a single site, |{m ≠ 0 : z(m) ∉ Q}| ≤ 1 when R ≥ 2, and the set is empty when R = 1.

*Proof.* Combine (F3), Lemma 5.1 and Theorem 5 applied to the gap-word sequence. Injectivity of the label families turns "at most one h′" into "at most one point". ∎

**R = 2 with equal lengths (Lemma 5.2).** Let R = 2 and the pumps satisfy m₁π = m₂π′ = Δ ≠ 0. Then z(m₁,m₂) ∈ Q.

*Proof.* The only proper period is d = 1, so non-primitivity means g_σ(m₁) = g_{σ′}(m₂) =: W.
- The maximal π-periodic prefix of W contains σ^{(m₁)}, and the maximal π′-periodic prefix contains σ′^{(m₂)}. Both have length ≥ 4π₀ ≥ π + π′, so Fine–Wilf gives π = π′ with the same pattern.
- g_σ and g_{σ′} are obtained from W by deleting Δ ≡ 0 (mod π) letters inside this common periodic prefix. Such a deletion gives the same word whatever its offset, so g_σ = g_{σ′}.
- Then z = g_σ g_{σ′} is a square, a contradiction. ∎

### 5.3 The partner principle (Corollary 5.3)

Let σ and σ′ be consecutive skeleton runs of z, with σ before σ′ in the linear word, both of length ≥ Λ := (8+4s²)π₀² + 2. Let F be a factor of σ's interior (at distance ≥ 2π₀ + 2s²π₀² + 1 from its ends) of length 2s²π₀² + 1, with every position of F marked. Let M be the number of marks from the start of F to position 2π₀ + 1 + s²π₀² of σ′. Then there is a good colour-loop decomposition whose vwx contains ≤ M marks.

*Proof.*
- **R ≥ 3.** By Theorem 2(b), take two colour loops v and v′ in F with a common marked start and lengths cπ ≠ c′π. By Theorem 2(b) applied in σ′, take a colour loop x of length eπ′ in σ′'s interior. In copy space the pumps (v), (v,x), (v′,x) move along the lines (c,0), (c,e), (c′,e), which are pairwise non-parallel. By Theorem 5\*, the single bad point (if any) lies on at most one of these lines, so at least two of the three pumps are good for all i.
- **R = 2.** By Theorem 2(c) with step L = lcm(π,π′) ≤ π₀², take equal-length v ⊆ F and x ⊆ σ′. Lemma 5.2 makes them good.
- **R = 1** cannot occur, since σ and σ′ are distinct runs.
- The interior margins guarantee that Lemma 5.1 applies for all i, including i = 0. ∎

**What 5.3 kills.** Every negative design in which the marked pumps live inside runs of small period, with another such run reachable, fails. That includes counters mod m, block-change markers and walls, all of which only restrict loops inside runs (Theorem 2(d)). In particular:
- **A's family** z = a^k b a^{k+L} b (π₀ = 1, R = 2): the equal-length partner in run 2 wins, as A observed. This is now a theorem for all such shapes.
- **Every block word** ∏ a^{k_m} b in which a marked long a-run has a long a-run within window reach (B's §6.2 designs included).
- **Long runs with full marking** (Bar-Hillel): the adjacent long run is always within reach.

---

## 6. Necessary conditions on any counterexample family to OG(Q)

By Theorems 1–5\*, a family (for each p: z, D, χ) witnessing ¬CPL_s must satisfy all four of the following.

- **N1 (isolation).** Every densely marked deep-interior factor of a long small-period run is separated from the neighbouring skeleton runs by more than p marks (Corollary 5.3).
- **N2 (single-site rigidity, achievable).** Inside such an isolated run, every aligned pump has at most one bad copy number (Theorem 5\*). The prover can hit it for all available loop lengths at once with the factorial trick: target t\* = −lcm(1..sπ₀)·t. So isolated runs *can* be locally fully rigid. This is the only rigid configuration found.
- **N3 (fresh loops).** Every marked colour loop with a fresh conjugate must have a non-primitive deletion (Lemma U).
- **N4 (buffers).** The more than p marked positions around an isolated run must contain no long small-period runs. Otherwise those runs are partners (N1). All local pumps there must still fail. For a one-sided pump v in such a buffer:
  - once i ≥ i₀(v) := ⌈Λ/|v|⌉ + 1, vⁱ is a skeleton run of z_{i₀}. Theorem 5\* applied to the family {z_i : i ≥ i₀} gives **at most one bad exponent ≥ i₀**;
  - failures at the boundedly many exponents i < i₀ cluster (Lemma 4).

  So each buffer candidate is killed by a small exponent (only O(s·i₀) positions per (ℓ, i)) or by **its unique large exponent i\***.

In N4, the large-exponent kill means z_{i\*} = r^q, and the rotation sends the new run vⁱ to an *existing* run of z elsewhere with the same pattern and exact length. Different buffer candidates may use different (i\*, q), with q ranging over primes dividing n_{i\*}, and different target runs. The two-sided "three directions" trick of 5.3 does not apply in buffers: one-sided and two-sided pumps there create different skeletons (one new run versus two), so their copy spaces cannot be compared.

---

## 7. The exact gap

**Gap G (buffer rigidity).** For every s there is p such that the following holds. Let z be primitive with an s-colouring χ, let B be a factor of length p all of whose positions are marked, and suppose B contains no factor of period ≤ π₀(s) and length ≥ Λ(s). Then some colour-loop decomposition with vwx ⊆ B is good.

- **¬G ⇒ ¬OG(Q):** a counterexample to G with full marking is a counterexample to CPL_s, hence to OG(Q), which would refute context-freeness of Q.
- **G is necessary for OG(Q)** in the full-marking case.
- **G + §5 does not yet imply OG(Q).**
  - G does not cover sparse markings, where windows are long and Lemma U applies but deletions (i = 0) are unconstrained.
  - G does not cover the boundary zones between isolated runs and buffers.
  - I could not reduce sparse markings to dense ones.

**Strength: theorem-strength.** Under N4, defeating G means one primitive word that is, after one local edit per candidate, a q-th power for about p/s² different (edit, i\*, q) triples. The primes q range over divisors of the varying lengths n_{i\*}, so their number is unbounded in n, and n is chosen after p. Proving G requires showing that a word cannot carry that many simultaneous near-power structures with defects packed into one window. Fine–Wilf alone fails exactly at q = 2 versus q = 2 (two near-square structures with periods ≈ n/2): Lemma 4a needs |D| ≤ N/6, but the large-exponent edits have |D| ≈ (i\*−1)|v|, unbounded. This is the same "small exponents with varying length" core as B §6.4, and the same "unboundedly many primes" obstruction as E. No sub-lemma of lower strength isolates it.

**Direction of belief.** All evidence points to G and OG(Q) being **true**. If so, (b) holds and the closure + Ogden route is dead, but this is not proved.

---

## 8. Computational evidence

All in `r2_og/`; pumps checked for i ≤ 3n+6.

| script | what | result |
|---|---|---|
| `x1_block_rigidity.py` | Theorem 5 on k ∈ {0..3}^r, r ≤ 8 | 0 violations; degenerate only at antipodal pairs |
| `x2_fresh.py` | Lemma U, all primitive z with \|z\| ≤ 12 | 0 violations (69,279 fresh pumps at n = 12); 2,608 stale pumps fail |
| `x4_cbh.py` | full marking: least window W_min such that every s-colouring admits a good colour-loop pump | s = 1: W_min = 1 for every z, n ≤ 10. s = 2: W_min ≤ 3 for 4 ≤ n ≤ 14. s = 3: W_min ≤ 4 for 6 ≤ n ≤ 11. Worst cases are a^k b a^{k±1} b-type words. |
| `x5_ogden.py` | arbitrary markings, exact φ(z) = least failing Ogden constant − 1 | s = 1: φ = 0 for all z with n ≤ 12, so **plain Ogden holds with p = 1** on this range. s = 2 (all markings × all colourings): φ ≤ 3 for n ≤ 9, attained only by boundary-wall colourings 0 1…1 0 |
| `x6_anneal.py` | prover-side simulated annealing over colourings: factorial family (several markings), near-cubes, Thue–Morse prefixes, random words, n ≤ 26 | best prover value c ≤ 2 (s = 2) and c ≤ 3 (s = 3). No growth. |

Tiny n (n ≤ 3 for s = 2, n ≤ 5 for s = 3) are trivial exceptions: a colouring can forbid every loop except the whole word.

---

## 9. Summary of rigorous results

1. **Theorem 1:** OG(Q) ⇔ ∀s CPL_s (colour-loop Ogden for Q with arbitrary post-p colourings).
2. **Theorem 2:** the exact power of annotation. Walls and mod-m (m ≤ s) constraints are possible. Removing aligned loops, or synchronized partners of any fixed ratio, is impossible.
3. **Lemma 3** (large i) and **Lemma U** (fresh conjugates are safe for every i ≥ 1).
4. **Lemma 4** (clustering): small-exponent failures with equal (ℓ, i) lie in one ℓ-periodic stretch.
5. **Theorem 5 / 5\*** (run-skeleton rigidity): at most one bad length-change pair for consecutive long small-period runs (R ≥ 3); equal lengths are safe when R = 2.
6. **Corollary 5.3** (partner principle): every run-confined negative design with a reachable partner run fails.
7. **Gap G** (§7): theorem-strength; settles nothing by itself.
