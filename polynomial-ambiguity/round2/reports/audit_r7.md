# audit_r7.md — R8-B audit of r7_lemmaQ.md (Q0, Lemma R, Prop S) and r7_uncouple.md (U1–U3)

Scripts: `scripts/audit_r7_uncouple.py` (independent bitmask brute force, n ≤ 18, 3 s), `scripts/audit_r7_lemmaQ.py` (Q0 m = 10; |G⁻_n|).
Gating note (§9): neither report claims to close a named gap (both say OPEN); audited on request.

## 1. r7_lemmaQ.md — verdict: SURVIVES (with caveats). No fatal flaw found.
- **Q0** correct. Hand check: w = b x bʳ a^{m+1}; for k ≤ m+1, suffix_k = a^k and #a(prefix_k) ≤ k−1, so d_k < 0; for m+1 < k ≤ n/2 the suffix holds all m+1 a's and the prefix ≤ m. Script: all 2^10 words in G⁻ for r = 0, 2, 4. (Mapping to r6's (t, h) parameters not re-derived.)
- **Spine / uncoupled closure** correct: n odd ⇒ position N is a leaf, every tree has a root-to-leaf path; replacing hanging subtrees by any derivations gives a tree of x c_s y at *every* split, so X_s c_s Y_s ⊆ L (in L itself, not only in the nonterminals' languages). Caveat: the spine must record the child index at each step (for A → AA), otherwise X_s is not a product and step-1 distinctness fails; the text implies this but should say it.
- **Prop S step 1** correct: two splits a ≠ a′ of one word give two trees whose s-path ends at different leaves ⇒ distinct trees; unambiguity ⇒ Σ_a |X_a||Y_{n−1−a}| ≤ |G⁻_n|. Checked |G⁻_n| = C(n−1, n/2) ~ 2ⁿ n^{−1/2} (n ≤ 20: |G⁻_n|√n/2ⁿ → 0.394).
- **Step 2** sound *if* the citation holds: X_s(z) = ∏ L_{A_j}(z) counts words (unambiguity + Y_s ≠ ∅). Exponent: εN/p shifts each ≥ ½ the centred term ⇒ O_s(2ⁿ n^{−1/2}/n) = O_s(2ⁿ n^{−3/2}); n^{−3/2} (not n^{−1}, n^{−1/2}) is right.
- **Caveat (main).** Drmota–Lalley–Woods covers only strongly connected systems. L_{A_j} for a general grammar is a non-strongly-connected N-algebraic series; needed: all dominant singularities lie at ρ·(roots of unity) and each residue class has C_r ρ^{−m} m^{α_r} (or is eventually exponentially smaller). This is believed (Banderier–Drmota 2015, positive systems; induction over the SCC DAG with |g(z)| < g(|z|) off the period lattice), but the report cites it loosely. Label should stay "modulo cited asymptotics", not "written proof". If dominant singularities could be off the root-of-unity lattice, step 2 breaks (no regular variation) — no counterexample found or expected.
- **Lemma R**: KMT + Prékopa + evenness argument checks (φ concave, φ(−γ) = φ(γ) ⇒ max at 0). Fine as labelled.
- Non-uniformity (N_0, C_s, p in s) is acknowledged as G1; Prop S alone closes nothing.

## 2. r7_uncouple.md — verdict: SURVIVES (with caveats). No fatal flaw found.
Independent brute force n = 1..18 (all 2ⁿ words), **0 errors** on: D_b·P = P; |P_n| = C(n−1, ⌊(n−1)/2⌋); u^p ∈ P ⟺ u ∈ P (primitive root u); P = (D_b a)⁺ parse into exactly H blocks; P ∩ Q ⟺ block sequence primitive; rotations of w lying in P = exactly the H block-start positions; U2(i) L_A (r6 split definition) = P ∩ {h ≤ 0 on [0,⌈n/2⌉]}; U2(ii) L_B ⊆ Q; U2(iii) Rot L_A = Rot L_B (as conjugacy classes; e.g. 3920 classes at n = 18).
Proofs re-checked: U1 (h < H everywhere), U2(i) (s = τ−1 ≥ ⌈n/2⌉), U2(ii) (|u| ≤ n/2, h(|u|) = H/p > 0), U2(iii) (first argmax i* > ⌈n/2⌉; wrapped part h(j−n)+H−M ≤ 0). All correct.
Caveats: "D_b·P⁺ = P" in Verdict item 1 is a typo for D_b·P = P; U2(iv) and the one-vs-each non-CF claims are pumping *sketches*; the Parikh remark is a sketch; the U3 "φ-lift is circular" is an assessment, not a theorem.
