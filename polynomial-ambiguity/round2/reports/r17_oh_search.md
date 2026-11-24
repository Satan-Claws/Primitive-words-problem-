# r17_oh_search.md — R17b-D: counterexample search, one-sided heavy case of T8_unamb

Status: **no counterexample** [computational]. Every family tried is killed exactly, either by ambiguity or by a G⁻
exit (an explicit word is given for each). This includes the one-tape (q_V = 0) heavy models added to scope by
audit_r17 C3. The last survivors fail through one mechanism, the **trailing light run**: B is driven below −C, the
MS⁺(b) floor, while A stays put. That is consistent with MS⁺(b) and indicates which constraint a proof should use.

Scripts (all in `scripts/`):
- `r17_oh_search_engine.py`: exact word sets, exact parse counts, float DP (c_n = #parses·2^{−n}), G⁻ test.
- `r17_oh_search_families.py` → `_out.txt`, `_surv.pkl`, `_top.json`: the family enumeration (stages 1–2).
- `r17_oh_search_recheck.py` → `r17_oh_search_recheck16_out.txt`, `r17_oh_search_recheck20_out.txt`: stage 3.
- `r17_oh_search_deep.py` → `_deep_out.txt`: the stage-3 survivors to |x| = 23, every pad (b^i, a^j) with i, j ≤ 4,
  and growth by DP to n = 800.
- `r17_oh_search_margin.py` → `_margin_out.txt`, `_margin_onetape_out.txt`: the required-pad statistic (exact for
  n ≤ 21, exactly-uniform samples for n ≤ 400).

## 1. Families [design]
- **Heavy U-block, β₀ = 1/4.** D⁻ → ε | b D⁻ a D⁻ (or D⁺ → ε | a D⁺ b D⁺), and Y → ε | (3 letters interleaved with
  D, Y, Y).
  - Y is a stacked critical nonlinear SCC: at z = ½, Y = 1 + Y²/4.
  - Checked by DP: the coefficients of Y are ~n^{−5/4}, and those of the pair SCC are ~n^{−3/4}.
  - There are 960 variants: 8 letter triples, 2 choices of D, and all orders of the 3 letters and 3 nonterminals.
  - Every Y contains (ba)^m-type flat words, so every Y block is U-level.
- **Pair SCC.** X → u_i X v_i | w.
  - Each u_i = αHβ (H = Y), or u_i is letters only. Each v_i is letters only, so the V side is light.
  - Weights satisfy Σ 2^{−|letters|}·2^{#H} = 1 **exactly**, so the SCC is critical.
  - Token sets: all sets of ≤ 2 tokens (|αβγ| ≤ 3), plus 3-token sets in which every token has ≤ 2 letters. That gives
    1962 sets: 1796 with q_V > 0 and **166 one-tape** sets (q_V = 0).
  - Centre w ∈ {ε, a, b, ab, ba}.
- **Outer pads.** S → b^i X a^j with i, j ≤ 3 (≤ 4 in the deep check). Exact domination: for |p| = i and |q| = j,
  d_k(pxq) ≥ d_k(bⁱ x aʲ), so these pads are the most favourable of their lengths. For symmetric pads there is an exact
  identity: bʲxaʲ ∈ G⁻ ⟺ M(x) := max_{k≤|x|/2} d_k(x) < j. A family is a counterexample only if sup M < ∞.

## 2. Funnel [computational, exact]
| stage | input | killed by ambiguity | killed by G⁻ exit | survive |
|---|---|---|---|---|
| 1: Y unambiguous to length 20 | 960 | 908 | — | 52 |
| 1b: single giant token, b⁶ y a⁶ ∈ G⁻ for \|y\| ≤ 20 (heuristic necessary filter) | 52 | — | 30 | 22 (all D⁻) |
| 2: X unambiguous to \|x\| ≤ 13; some pad (i, j ≤ 3) with no exit | 22·1962·5 = 215,820 | 210,182 | 4,805 | 833 (397 one-tape) |
| 3: the same to \|x\| ≤ 16 | 833 | 247 | 456 | 130 |
| 3: the same to \|x\| ≤ 20 | 833 | 401 | 430 | **2** (both two-sided) |
| one-tape subset at \|x\| ≤ 20 | 397 | 99 | 298 | **0**; the last ones die at \|x\| = 20 |

Kill-length histogram at stage 3 (|x|): 14: 319, 15: 149, 16: 135, 17: 59, 18: 66, 19: 78, 20: 25.

## 3. The two deep survivors and why they die [computational]
The two survivors are:
- X → bYXa | bYXb | ba, with Y → ε | YbYbD⁻a;
- the same X with Y → ε | bYbD⁻aY.

What holds for both:
- Tokens (bY, a) and (bY, b): V is a free word of length r.
- Both are **unambiguous to |x| = 23**, exactly.
- DP: |X_n|·n/2ⁿ = 0.191, 0.207, 0.234, 0.271, 0.317 at n = 50, 100, 200, 400, 800. This grows like n^{≈0.2}, tending
  to n^{1/4}. So each would be a genuine counterexample if it lay in G⁻.

Why they die (`_deep_out.txt`):
- Every pad (bⁱ, aʲ) with i, j ≤ 4 has an explicit exit, except (4, 4), which first exits beyond |x| = 23.
- Symmetric pads die at |x| ≈ 13, 17, 21 for j = 1, 2, 3. For example, b³·bbbbbaabaabbbbbabbbbb·a³ ∉ G⁻ (exit at k = 13).
- Required pad M(x) (`_margin_out.txt`):
  - exact max over X_n of M = 0, 1, 2, 3 at n = 12, 13, 17, 21. That is +1 every 4 letters, so linear growth.
  - Uniform samples at n = 400: about 13% of words need a pad ≥ 4. The largest observed is M = 26 (witness length 400;
    b²⁶xa²⁶ ∉ G⁻).
- So **no fixed pad works**, and the violating words are a non-vanishing (growing) fraction.

The one-tape analogues X → bYX | a (or | ba), with Y ∈ {bYbD⁻aY, bD⁻bYaY}, behave the same way
(`_margin_onetape_out.txt`):
- exact max M = 0, 1, 2, 3 at n = 8, 12, 16, 20;
- about 10% of uniform n = 320 words need a pad ≥ 4, with max M = 15.

**Mechanism (all deep kills).** The extremal words are
- one-tape: bbbb·abbaaa·b^{2m}·a, i.e. one early Y-block, then a run of empty-Y tokens b b … b, then w;
- two-sided: the same, with V = b^r.

The trailing run of light tokens (whose U-word is just b), or a V-tape of b's, drives the suffix walk B(k) down
linearly. Meanwhile an early level Y-block holds A(k) near its value. This is exactly a violation of the MS⁺(b) floor
B ≥ −C. Criticality forces such down-pushing tokens:
- Σπ = 1 together with δ(t) = wt(u) − wt(v) ≤ 0 (the closure condition) leaves no room for every token to raise B.
- Any token that lowers the suffix walk can be repeated at the end.

[heuristic, not proved for general models]

## 4. Scope and honesty
- What was searched:
  - only Y-level (β₀ = 1/4) heavy blocks, with the specific Dyck base D^±;
  - token sets of bounded size, with short letter context;
  - k = 3 blocks (β₀ = 1/8) were **not** enumerated, for lack of time;
  - V-sides that are not single letters were not enumerated.
- Stage 1b is a heuristic filter: pads ≤ 6 on each side, for a single token. It may discard Y-blocks that could
  survive with a longer right context.
- What is proved here: unambiguity up to the stated length (parse count equals distinct-word count), and every kill,
  each with an explicit word. "Survivor" only ever means "no exit up to the checked length".
- Consistent with the prior searches (r9: 240k grammars, best Catalan; r10: all one-sided survivors die at n = 28).

## Status
| claim | label |
|---|---|
| 215,820 critical one-sided-heavy pair grammars (incl. 18,260 one-tape): all ambiguous or out of G⁻ by \|x\| ≤ 20, except 2 | computational, exact |
| The 2 deep survivors: unambiguous to 23, but required pad M grows linearly (exact to n = 21; M = 26 at n = 400) ⇒ not in G⁻ for any pad | computational, exact witnesses |
| One-tape heavy (q_V = 0): no survivor past \|x\| = 20; same mechanism | computational |
| Kill mechanism = trailing light run breaks B ≥ −C (MS⁺(b)) | heuristic; suggests the proof route |
| Counterexample to T8_unamb in the one-sided heavy case | **none found** |
