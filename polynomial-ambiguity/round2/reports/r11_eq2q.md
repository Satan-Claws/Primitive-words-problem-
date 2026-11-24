# R11-A: the equality form EQ-2q

EQ-2q asks whether some PCFL L satisfies L ∩ row_{2q} = Q ∩ row_{2q} for every prime q, where row_N = {w : #a(w) = N}.
Notation is as in `r10_2q.md`:
- γ(w) is the cyclic gap sequence.
- D = (b's in odd gaps) − (b's in even gaps).
- NonSq is the set of words not of the form uu. Not2P is the set of words whose γ is not cyclically 2-periodic.
- On row 2q, with q an odd prime, P_q denotes the q-th powers v^q with #a(v) = 2 and v primitive.

Script: `scripts/r11_eq2q_sorted.py`. Its output is in `scripts/r11_eq2q_sorted_out.txt`.

## 0. Summary

| item | status |
|---|---|
| EQ-2q (does a PCFL with equality on all rows 2q exist?) | **OPEN.** Neither direction was resolved. |
| Lemma S (exact D-sorted decomposition, all #b) | [written proof] + [computational: rows 4, 6, 10, 14, \|w\| ≤ 20, 0 failures] |
| **Theorem T.** No *regular* sorter works: (C₁ ∩ R₁) ∪ (C₂ ∩ R₂) ∪ R₃ with R_i regular fails on **every single** row 2q (q ≥ 3 odd), for any "blind" certificates C₁ ⊇ P_q and C₂ ⊇ Sq∩Not2P (for example NonSq and Not2P) | [written proof] + [computational check of the witnesses] |
| The b-pumping route to ¬EQ-2q: precise obstruction | [written analysis]. The route fails because the pump partner is uncontrolled (§3). No step uses the ambiguity bound, so any successful version would prove Q ∉ CFL. |
| Affirmative: a uniform CF or PCF L | Not found. The only exact construction known is the D-sorted one, and its pieces need two counters (§4). |

## 1. Lemma S (exact sorted decomposition)

**Lemma S.**
- For q an odd prime: Q ∩ row_{2q} = ({D ≠ 0} ∩ Not2P) ⊔ ({D = 0} ∩ NonSq), intersected with row_{2q}.
- For q = 2: Q ∩ row₄ = Not2P ∩ row₄.

*Proof.* On row 2q a non-primitive word w = v^d has d | 2q, so it is a square or lies in P_q. For q = 2 both cases are "γ is 2-periodic".

Now let q be odd.
- By Lemma D(i), squares have D = 0. So on {D ≠ 0}, primitivity is equivalent to Not2P, because 2-periodic words are P_q words or squares.
- By Lemma D(ii), P_q words have D ≠ 0. So on {D = 0}, primitivity is equivalent to NonSq.

∎ [computational: all words on rows 4, 6, 10, 14 with \|w\| ≤ 20 (20349, 116280, 352716 and 54264 words), 0 failures]

The sorter {D = 0} is a one-counter language. Each piece crosses it with an arch certificate, so the pieces are "two-counter" (r10 §3 items 1 and 3), and L_S is not known to be CF.

## 2. Theorem T: the sorter cannot be regular

**Theorem T.** Fix an odd q ≥ 3 and let R₁, R₂, R₃ be regular. Let C₁ be any language containing every P_q word, for example NonSq. Let C₂ be any language containing every square
in Not2P ∩ row_{2q}, for example Not2P. Then L = (C₁ ∩ R₁) ∪ (C₂ ∩ R₂) ∪ R₃ does **not** satisfy L ∩ row_{2q} = Q ∩ row_{2q}.
The conclusion also holds for finite unions of such pieces, since (C ∩ R) ∪ (C ∩ R′) = C ∩ (R ∪ R′).

*Proof.*

**Gap saturation.** Let N be at least the number of states of the three DFAs, and let M = N!. Take
w = a b^{γ₁} a b^{γ₂} ⋯ a b^{γ_{2q}} with every γ_k ≥ N, and fix one of the DFAs.
- On w's accepting run, each b-run repeats a state within its first N letters. This gives a loop b^t with 1 ≤ t ≤ N, so t | M.
- The loops sit at disjoint places on the path, so they can be iterated independently.
- Hence if w ∈ R_i, then R_i contains every word with gaps γ′ ≥ γ and γ′ ≡ γ (mod M), componentwise.

**The three words.**
- w has γ = (N, …, N, N+M). It is primitive: γ_q ≠ γ_{2q}, so γ is not q-periodic, and γ_{2q−2} ≠ γ_{2q}, so γ is not 2-periodic.
- p = (a b^{N+M} a b^{N+2M})^q. Its gaps dominate γ and are congruent to γ mod M. The word p ∈ P_q, and p ∉ Q.
- s has γ″ = N + M·[k ∈ {q, 2q}]. Its gaps dominate γ and are congruent to γ mod M. The word s = uu is a square, s ∉ Q, and s ∈ Not2P because γ″_q ≠ γ″_{q−2}.

**The contradiction.** The word w ∈ Q ∩ row_{2q} must lie in L. Check each piece:
- w ∈ R₃ would give p ∈ R₃ ⊆ L.
- w ∈ C₁ ∩ R₁ would give p ∈ R₁ ∩ C₁ ⊆ L.
- w ∈ C₂ ∩ R₂ would give s ∈ R₂ ∩ C₂ ⊆ L.

Every case puts a non-primitive word of row 2q into L. ∎ [computational: witnesses checked for q ∈ {3, 5, 7} and (N, M) ∈ {(1,1), (2,2), (3,6)}]

**Reading.**
- *Scope.* This is a restricted-class result, the row-2q analogue of Theorem S in `l6.md`. It holds row by row, so it is not about uniformity in q.
- *The argument uses only gap saturation.* So R_i may be any gap-saturated language, for example a regular language intersected with modular Parikh conditions.
- *The sorter must break saturation.* It has to separate squares from P_q words inside one residue class of gap vectors mod M. D does this: it is not saturated, and that is exactly Lemma D.
- *Consequence.* Any exact L built from the two blind certificates needs a counter-type sorter. Weightings of index-mod-k type are forced to be multiples of D (r10 §3 item 3).

## 3. Negative attempt: b-pumping on rows (exact obstruction)

The aim was to start from a primitive w near a square or near P_q and pump b-runs (keeping #a) until L must accept a square or a P_q word. The attempt stops at three points.

**P1. The partner can carry a's.** Ogden with marks in one gap gives a pump (v, x) with one side in the marked run. The other side is uncontrolled and may contain a's.
- The pumped words then leave row 2q.
- By Dirichlet they land on rows 2q′ only for k in an arithmetic progression, and only when #a(vx) is even and gcd(q, #a(vx)/2) = 1.
- On those rows the only constraint is that the pumped words be primitive, and pumped words are primitive for all but ≤ 2 values of k.
- Nothing is forced. The word-level NonSq grammar A_c A_d behaves exactly like this, because its pumps are mirror letter pairs of either letter.

**P2. Pure b-pumps change two gaps with an uncontrolled partner.** A pump vector is g = t·e_i + t′·e_j. Write φ_S(γ) = (γ_k − γ_{k+q})_{k<q} (squares are φ_S = 0) and φ_P(γ) = (γ_k − γ_{k+2})_k (2-periodic is φ_P = 0).
- w_k is non-primitive for at most one k per map. Such a k exists only if φ_S(w) ∈ ℚ·φ_S(g) or φ_P(w) ∈ ℚ·φ_P(g).
- The grammar picks g after w is fixed. If w has a single defect at gap i₀ and the partner satisfies j ≢ i₀ (mod q), every w_k has defects at i₀ and j, so it is primitive.
- So the prover cannot force a hit. This is exactly the mechanism that kills pumping proofs for Q itself (prompt §6, "Pumping on letter-count families").

**P3. Laminarity is real but not enough.** A *square-neutral* pump pairs gap i with gap i+q. Its subtree spans q consecutive gap boundaries.
- Two such spans in one derivation tree must be nested or disjoint, and equal-length spans inside 2q gaps can be neither unless they coincide.
- So [written proof] at most O(1) square-neutral pumps occur per tree. This makes "needs crossing arches" precise for one natural certificate (gap-level NonSq).
- But a correct grammar does not need neutral pumps. Non-neutral pumps with j ≢ i (mod q) are harmless by P2, so P3 yields no contradiction.

**Where the ambiguity bound would have to enter.** Nothing in P1–P3 uses ambiguity. A pumping or interchange contradiction for EQ-2q would therefore show that no CFL satisfies EQ-2q, hence Q ∉ CFL. That is a harder open problem, so it should be treated as suspect.
A proof of ¬EQ-2q for PCFLs must instead use tree counting:
- primitive words near both families must carry many certificate trees, because the D-sorter is unavailable to a grammar of bounded counter structure;
- and these trees must be shown not to merge.

We found no mechanism that does this. **Exact gap:** we have no lemma turning "the sorter must be non-saturated" (Theorem T) into a lower bound on amb(w).

## 4. Affirmative attempt

- **Exact but not shown CF.** L_S from Lemma S is exact on every row 2q [proof; computational to \|w\| ≤ 20]. Each piece intersects a one-counter sorter with an arch certificate, which is a crossing / two-counter shape, so it is not known to be CF. The band piece {#b even, 0 < |D| < #a} is the only part known to be CF (r10).
- **Ruled out.** Every regular-sorted variant is ruled out by Theorem T, on every row, for every choice of blind certificates.
- **Fixed q.** Q ∩ row_{2q} is CF for each fixed q, using gap-level arches with a fixed count of q−1 a's (KK-type; the citation is unverified, prompt §6). The difficulty is uniformity in q, because the a-count matching crosses the γ_i-versus-γ_{i+q} comparison (P3).
- **No candidate tested.** No uniform CF construction was found, so there is no candidate grammar to check exhaustively. Only Lemma S is checked (§1).

## Files
- `scripts/r11_eq2q_sorted.py` checks Lemma S on rows 4, 6, 10, 14 with \|w\| ≤ 20 and the witnesses of Theorem T. The output is in `scripts/r11_eq2q_sorted_out.txt`, with 0 failures.
