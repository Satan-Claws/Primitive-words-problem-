# S4C: cyclic-closure transversal reformulation (Session 4)

Status: **Theorem C PROVED** (exact ambiguity identity, checked by computer). **Reformulation (R) PROVED**, but it is
equivalent to the original question up to a factor n, so it gives no new leverage. **Affirmative (2): NOT FOUND.**
Every natural certificate either misses classes or is non-CF across ratios. **Negative (3):** the known lower bounds
transfer to every CF "transversal-ish" L. No new exponential obstruction.

Notation. Q = primitive words over {a,b}. [w] = conjugacy class. rot_j(w) = w[j:]w[:j].

## 1. Theorem C (exact ambiguity of the inverted-path cyclic closure)

Let G = (N, {a,b}, P, S) be in CNF with ε ∉ L(G). (Cycle-free G converts to CNF with amb preserved; this is step 1
of Theorem P in POLY_FINAL.md.) Define G′ with nonterminals N ∪ {[A] : A ∈ N} ∪ {S′} and these rules:
- B → A C in P gives [A] → C [B]; B → C A in P gives [A] → [B] C;
- [S] → ε;
- A → x in P (x a letter) gives S′ → x [A].

Here [A] ⇒* βα whenever S ⇒* αAβ ("outside of A, read from right to left around the cycle").

**Claim.** For every w with |w| = n ≥ 1, amb_{G′}(w) = Σ_{j=0}^{n−1} amb_G(rot_j(w)).

*Proof.* Take a derivation of w in G′: S′ → w_1[X_m], [X_m] → …, …, [X_0] → ε, with X_0 = S. The chain
[X_m], …, [X_0] together with the sibling subtrees determines a unique G-tree T. The path in T is
S = X_0 → … → X_m → w_1, and each sibling lies on the side recorded by the rule. The leaf w_1 sits at some position
j+1 of the yield r of T. The words generated agree: w = w_1 · (right siblings, bottom-up) · (left siblings,
top-down). This is rot_j(r), i.e. r = rot_{−j}(w).

Conversely, every pair (T, leaf) arises exactly once, because the root-to-leaf path in T is unique. So derivations
of w in G′ biject with pairs (j, T) where T is a G-tree of rot_{−j}(w). ∎

G′ has no unit rules. To remove the ε-rule, add [A] → C and [A] → C′ for each rule with [S] on the right-hand side.
This keeps the count, because [S] ⇒ ε uniquely. So G′ becomes a cycle-free ε-free CFG with the same amb.

*Check:* `scripts/poly/s4c_cyc.py` takes 40 random 3-nonterminal CNF grammars and all words of length ≤ 7. It
compared both sides on 10160 words and found 0 mismatches.

**Corollary C1.** Suppose L(G) ⊆ Q and G meets every primitive class. Then L(G′) = cyc(L(G)) = Q. Rotations of a
primitive w are pairwise distinct, so
  amb_{G′}(w) = Σ_{r ∈ [w] ∩ L(G)} amb_G(r) =: M_G([w])   (the "class mass").
There is no O(|w|) loss. That factor appears only for non-primitive words, and those are excluded here.

## 2. Reformulation (R)

Let f be non-decreasing. Q has a cycle-free CFG of ambiguity ≤ f(n) **if** some CFG G with L(G) ⊆ Q meets every
class with M_G([w]) ≤ f(|w|). **Only if** holds with M ≤ n·f(n): take G = G_Q, so M = Σ over the n rotations.

- Poly-ambiguity of Q is equivalent to "∃ G ⊆ Q meeting all classes with polynomial class mass".
- k-ambiguity of Q is implied by "class mass ≤ k".
- The thinness of L buys nothing for the polynomial question. Lower bounds on amb_{G′} are lower bounds on class
  mass (§4).

## 3. Affirmative attempts (all fail)

- **Lyndon words** are an exact transversal. Berstel–Boasson (Bull. EATCS 63, 1997) prove they are not CF
  (scout.md). Cyclic closure is CF (Oshiba 1972, Maslov 1973), so a CF transversal would make Q CF, and Q being CF
  is itself open. So any affirmative L in (2) must also settle the CF question. It is at least as hard as the
  original problem.
- **Unique-minimum certificate.** For coprime (p,q), let h = q#a − p#b on prefixes. Define
  L_{p,q} = {w : h(w) = 0, h(x) > 0 for every proper nonempty prefix x}. This set is ⊆ Q (a power u^k would have
  prefix u with h = 0). It is an unambiguous one-counter language, and it contains exactly one rotation of each
  class whose cyclic h-walk has a unique minimum (cycle lemma).
  - If gcd(#a,#b) = 1, all n cyclic h-values are distinct (y·Δa = x·Δb forces n | Δ). So every coprime class is hit
    exactly once.
  - If k = gcd ≥ 2, a class may have m ≥ 2 minima. It then factors cyclically into m primes of the code
    P_{p,q} = L_{p,q}, and it is primitive iff that necklace over the infinite alphabet P_{p,q} is primitive. This is
    an exact self-reduction: the hard classes are the primitive-necklace problem again, over a CF code. So it gives
    no progress.
  - The union over ratios fails as well. ∪_{p,q} L_{p,q} ∩ a*b*a*b* = {a^x b^y a^z b^t : xt > yz} (up to boundary
    cases). This is a multiplicative, non-semilinear condition, so the union is not CF.
- **Proportional-cut certificates** ("some or every cut x|y with Parikh(x) ∦ Parikh(w)"). The existential form holds
  for powers too. The universal form is the unique-minimum condition again: it misses classes such as [aabbab]
  (minimum attained twice) and is non-CF across ratios.
- **Letter-count conditions.** Lemma O, {r#a − s#b = ±1}, covers only coprime classes with one fixed (r,s).
  {gcd(#a,#b) = 1} is not CF (its Parikh image is not semilinear).

## 4. Negative transfer

Theorem P (POLY_FINAL.md) applies to the cycle-free grammar G′. Petersen (TCS 1996; scout.md) and the
Lean-checked non-finite-ambiguity result apply as well. So for **every** CFG G with L(G) ⊆ Q that meets all classes:
- the class mass M_G is unbounded;
- in fact max_{|w| ≤ n} M_G([w]) = Ω(√(log n / log log n)).

In particular, no CF language is a "bounded almost-transversal" of Q. That means bounded representatives per class
together with bounded ambiguity. This strengthens Berstel–Boasson in an ambiguity sense: any L ⊆ Q has either many
representatives or many trees.

This yields no exponential obstruction. Any superpolynomial bound on class mass is equivalent to the original
target, by (R).
