# T1: slice families with super-polynomial inherent ambiguity? (agent T1)

Notation: x ∈ ℕ^n exponent vector of a word in (ab*)^n; V_p := {x : x shift-(n/p) invariant}; W_n := Σ_{p|n} V_p
(codim φ(n), Fourier: drop only the order-n component). Primitive ⇔ x ∉ ∪_p V_p (devil F0).

## Proved
**P1 (off-W part is linear).** For any regular S ⊆ (ab*)^n: Q∩S = (S∖W_n) ∪ (Q∩S∩W_n), and S∖W_n has a
cycle-free grammar of ambiguity ≤ φ(n) (union over a basis L_1..L_φ of W_n^⊥ and signs of the DOC languages
{±L_i(x)>0}; each is deterministic hence unambiguous; a word is in ≤ φ(n) of them; ×DFA keeps counts).
So inh.amb(Q∩S) ≤ φ(n) + inh.amb(H) for any CF H with Q∩S∩W_n ⊆ H ⊆ Q∩S.
**Cor.** n = p^a: W_n = V_p, Q∩S = S∖W_n, inh.amb ≤ φ(n) < |w|. No prime-power slice beats linear.

**P2 (idea ii is circular).** S = (ab+abb)^* is a regular slice of (ab*)^* and Q∩S = h(Q), h(a)=ab, h(b)=abb
(prefix code, block factorisation unique, so primitivity is preserved both ways). Inverse homomorphism by a
bounded prefix code preserves tree counts up to a constant factor (buffer simulation is a bijection on runs).
Hence "every slice family has poly ambiguity" ⇔ the main target (Q has a poly-ambiguous grammar).
The impossibility direction of T1 is NOT separately provable; it IS the problem.

**P3 (idea iii is polynomial).** If a level multiplies witnesses by ≤ a and length by ≥ b, then
amb ≤ L^{log a / log b}. Nested R_m: a ≈ ⌈m/2⌉ (best known), b ≥ 4m−2, exponent < 1. Sub-linear.

**P4 (product mechanism, linear algebra; numerically checked n=36,72,100,180,900).** A "conjunctive" sub-
configuration needs subspaces E_k with E_k ⊆ ∩_{j≠k}V_j, E_k∩V_k = 0; then on ⊕E_k: primitive ⇔ all e_k ≠ 0.
Max choice: E_k = (g_k-periodic) ⊖ (n/rad(n)-periodic), g_k = n·p_k/rad(n); dim E_k = (n/rad n)(p_k−1);
the sum is direct. ∏_k dim E_k = (n/rad n)^{ω(n)} φ(rad n).
* squarefree n: ∏ = φ(n) < n — idea (i) with n primorial is capped at LINEAR.
* n = P_N² (P_N = primorial): ∏ ≥ P_N^{N} = n^{N/2} — super-polynomial in n.

## Best candidate (CONJECTURED)
S_N = (ab*)^{n_N}, n_N = P_N², base point x0 ∈ ∩_k V_k (P_N-periodic), perturbations in ⊕E_k, d_k = P_N(p_k−1).
Conjecture: inh.amb(Q∩S_N) ≥ ∏_k (d_k+1)/2^N ≥ n^{N/2}/2^N. Upper-bound grammar: none known
(KK-open for N ≥ 4; naive DNF "one mismatch chord per prime" has ≤ ∏ 2·codim V_k ≤ (2n)^N pieces but is not
laminar, devil B2). Off-W part: φ(n) (P1).
Gaps (exact):
G1 multiplicative ply lemma: covers of ∏_k(ℝ^{d_k}∖0) by cones avoiding {e_k=0}; separation gives each open
   piece ⊆ ∏ half-spaces (proved), averaging gives ply ≥ |𝓗|/2^N (proved), but |𝓗| ≥ ∏(d_k+1) is FALSE
   in general (d=(2,2): 8 < 9 cover); need |𝓗| ≥ c^N ∏ d_k. Checked consistent only for d=(2,2) (ply 3).
G2 Lemma X analogue: residue classes mod P_N have size P_N > 2, so 4.1-interleaving no longer forces
   dim ≥ n−1 (nested class pieces allowed); without it lower-dim laminar faces may cover with ply 1.
G3 length control: §5 witnesses have |w| ~ N!·t (grammar-dependent), and under poly ambiguity PROOF §3(e)
   fails (dependent periods allowed) → needs T2 partition-function version.
