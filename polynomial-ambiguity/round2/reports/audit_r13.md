# audit_r13 — adversarial audit of Theorem N (r9), Theorem N2 (r10), Lemmas F / M / A (r5, r6)

Auditor R13-B. Every check uses my own scripts. The candidates' scripts were not run or read.
- `scripts/audit_r13_grammars.py` rebuilds G_P, L_P2, G₂ and L** from the rules as written in the reports. It counts trees exactly in two ways: by layered derivation enumeration with big-int multiplicities, and by an independent per-word CYK-style memo DP. The second is used as a cross-check up to |w| ≤ 11.
- `scripts/audit_r13_extras.py` checks the semantic language definitions on every non-primitive word with |w| ≤ 40.
- `scripts/audit_r13_fold.py` checks the fold lemmas with numpy.

A mutation test (deleting `F a BS` from W2 of G_P) is caught immediately: 168 language failures at |w| ≤ 10, first counterexample `baa`. So the harness has teeth.

## Verdicts

| candidate | verdict |
|---|---|
| Theorem N (G_P, L_P) and L_P2 | **SURVIVES** |
| Theorem N2 (G₂, L**) | **SURVIVES** |
| Lemma F, Lemma M, Lemma A (+ G⁻ ⊆ Q, g=1 ⇒ unique argmax) | **SURVIVES** (cosmetic caveats) |

## 1. Theorem N (r9 §2)

**Re-derivation.**
- *Lemma 1.* The condition in Lemma 1 says that the cyclic sequence γ is constant. A constant γ = (k, …, k) means w is conjugate to (a b^k)^N.
- *W1.* W1 = Σ* a·b^x a b^y·a Σ* with x ≠ y. The K1 rule gives x > y and the K2 rule gives x < y.
- *W2.* Write x for the last internal gap y_{N−1}. The three cases are A·C (x = s+t+d), A·E (x = s+e with t = e+d, so s ≤ x < s+t) and F a b* (s = x+d > x). They are disjoint, and together they cover exactly x ≠ s+t.
- *Parse uniqueness in W2.* Z must end at the penultimate a, and s and t are forced by the leading and trailing b's.
- *W1 parses.* They are in bijection with the internal witness positions i.
- Hence amb = #{i ≤ N−2 : y_i ≠ y_{i+1}} + [y_{N−1} ≠ s+t] ≤ N−1.
- *Remaining pieces.* ONEA covers N = 1, and S → b covers the single word b. The words b^m with m ≥ 2, the word ε, and the words a^n with n ≥ 2 (which lie in N_a, root a) are correctly excluded.

**Two-letter version.**
- A word of N_a that is not a power of a contains no aa.
- In the "neither aa nor bb" region, the only roots with exactly one a, or with exactly one b, are ab and ba.
- The four regions are disjoint and regular, so tree counts add.

**Computation** (exact, |w| ≤ 20, all 2 097 151 words, 0 failures):
- the tree-count language equals L_P;
- amb ≤ max(1, #a−1);
- Q ⊆ L_P;
- every non-primitive word of L_P has #a composite;
- L_P2 computed from the 4 regions equals its definition, amb ≤ |w|, and every word of L_P2 ∖ Q has #a and #b both composite.

The semantic check on all non-primitive words with |w| ≤ 40 also passed: 2.1·10⁶ words of L_P ∖ Q, 0 failures.

**Caveat.** Corollary N1 ("L_P is inherently ambiguous") rests on Theorem U′, which r9 attributes to `pcop.md` §5. I did not audit U′ here.

## 2. Theorem N2 (r10 §1–2)

**Lemma 1 (distance 2).** With the internal equalities y_i = y_{i+2}, the odd-indexed gaps equal X and the even-indexed gaps equal Y. Since N is even, y_{N−1} = X automatically. The only wrap condition left is s+t = Y = y_{N−2}. This is correct.

**G₂.**
- K1 and K2 give a b^x a b* a b^y a with x ≠ y.
- In W2, x = y_{N−2}, and the three cases split it exactly as in G_P. Z runs to the antepenultimate a, so it is forced.
- On even rows, amb ≤ N−2.

**(c), re-derived.**
- *eo.* The exponent d is odd and d | gcd(#a, #b).
  - #a = 2q forces d = q and #a(v) = 2, so γ is 2-periodic. If w contains bb, L₂ rejects it (2q ≥ 4). If not, v = a b^x a b^y with x+y odd and x, y ≤ 1, so #b(v) = 1 and w ∈ N_b, which sw(L_P) rejects.
  - #b = p forces #b(v) = 1. Either w = b^p (with bb, rejected because L₂ needs ≥ 2 a's) or w has no bb and lies in N_b (rejected).
  - #a ∈ 2^ℕ is impossible, because d is odd.
- *oo.* This is L_P2, where both counts are odd composites.
- *ee.* Empty. Coprime words never lie in ee.

**Computation.**
- Exact tree counts for |w| ≤ 20 (all words), 0 failures: Cop ⊆ L**, amb ≤ |w|, no word of L** ∖ Q on a special row, and (d) on rows 2q with #b odd. G₂ matches L₂ on even rows, with amb ≤ max(1, #a−2).

**Caveat.** The shortest word of L** ∖ Q is (a³b³)³, of length 18. So the |w| ≤ 16 range quoted in r10 tests claim (c) only vacuously. My |w| ≤ 20 run tests it non-vacuously, and so does the semantic run on all non-primitive words with |w| ≤ 40 (13 242 words of L** ∖ Q, 0 on special rows). CYK spot checks of eo extras on row 12 (|w| = 21) agree with the semantic definition.

## 3. Lemmas F, M, A (r5 §1, r6)

**Re-derivation.**
- *Lemma F.* Set j = ⌊p/2⌋. Then j/p ∈ [1/3, 1/2] for every p ≥ 2: it is 1/2 at p = 2, 1/3 at p = 3, and at least 3/8 for p ≥ 4. Hence jm ∈ K_n, and at k = jm the prefix and the suffix both equal u^j.
- *Lemma M (⇒).* Take w = (a b^{m−1})^p. Every k ∉ mℤ has d_k = 1.
- *Lemma A.* Since T is n-periodic, n·d_k(v) = T(r+k) + T(r−k) − 2T(r). For 1 ≤ k ≤ n/2 and n ≥ 2, neither r+k nor r−k is ≡ r (mod n).
- *g = 1 ⇒ unique argmax.* Here g = gcd(#a, #b), the gcd used in r5 and r6. T(i) = T(j) forces n | (j−i)·#a. Since gcd(#a, n) = gcd(#a, #b) = 1, this gives n | (j−i).

**Computation** (`audit_r13_fold.py 24 20`, 0 failures):
- Lemma F: checked for all n ≤ 24 against every non-primitive word u^p.
- Lemma M: checked for **every** K ⊆ [1, ⌊n/2⌋] and every n ≤ 24. Soundness holds iff the criterion holds.
- Lemma A: checked on all words with n ≤ 20. The argmax rotation always has d_k ≤ 0, and d_k < 0 whenever the argmax is unique.
- G⁻ contains no non-primitive word (n ≤ 20).
- g = 1 never produces a tie (n ≤ 20). 183 912 tie words occur in total, all with g ≥ 2.

**Caveats (cosmetic).**
1. r6 writes d_k = T(r+k) + T(r−k) − 2T(r). The correct identity has the factor: n·d_k = T(r+k) + T(r−k) − 2T(r). Only the sign is used, so nothing breaks.
2. At n = 0, F_K and G⁻ vacuously contain ε, which is not in Q. Restrict to n ≥ 1, or use Σ⁺. For n = 1, K is empty, and F_K = {a, b} ⊆ Q.
3. Lemma M needs K ≠ ∅ when n is prime (m = 1). Its statement already implies this.

## Checklist (§9)

| item | finding |
|---|---|
| per-word vs total ambiguity | per-word, checked |
| aⁿ and length-1 words | checked |
| cycle-free / exact counting | unit rules are acyclic, and ε-rules occur only in ST and BS. Counts are exact big ints from two independent methods. |
| DFA products | used only as region filters, which preserves tree counts |
| computation as proof | each claim also has a written proof, re-derived above |
