# audit6: audit of builder3.md (L*_ℓ, BGB, PAR, coverage)

Script: `scripts/audit6/a6.py`. It is independent of builder3's `cov.c` and works on cyclic block vectors, with B = 3 and ℓ ≤ 8.

## (1) Soundness: CONFIRMED (PROVED, re-derived by hand)
- **L\*_ℓ.**
  - If x = σ_d x, then D_{i+d} = x_i − x_{s−i−d} = x_i − x_{s−i} = D_i, so D is σ_d-invariant.
  - The two cases of the proof are correct.
    - Case ℓ | d: j+d ∈ {j, Rj} is excluded, because d ≢ 0 and t ≠ −t.
    - Case ℓ ∤ d: Rj ≡ j (mod ℓ), since 2f ≡ s. Then the class f+d carries both +t and −t.
  - No property of t other than t ≠ 0 is used.
- **BGB.** Under σ_{K/p}, the set {i : x_i > x_{s−i}} is a union of p-orbits, so p | mm. Also p | K, hence p | K − 2mm. The edge case K = 2mm gives gcd = mm, so the condition forces mm = 1, which is fine.
- **PAR.** This is trivial: u^p forces p to divide both letter counts.

## (2) CF: CONFIRMED (argument checked, no grammar written)
- **Any axis.** Every reflection of Z_K is a rotation of one of the two standard linear folds: through a block, or between blocks. The class labels i mod ℓ shift consistently because ℓ | K. Cyc preserves CF (Maslov 1973 / Oshiba 1972).
- **Any t.** The mismatched pair is the linear language {a^P b … a^Q b : P ≠ Q}. It is a single CF description; no union over t is needed.
- **Counters.** BGB and PAR need only counters capped at B and residues mod lcm(1..B).
- **Mismatch with the code.** The report says ℓ ≤ 8, but `cov.c` has LMAX = 6 by default (presumably set from the command line). This does not affect soundness.

## (3) Brute force: CONFIRMED (COMPUTER-CHECKED)
Every non-primitive word of length ≤ 30 (68,154 words) was tested. L\*, BGB and PAR accept none of them.

## (4) Coverage: PARTIAL
- **Checked.** Both n = 26 misses are primitive and balanced (13/13), and my L\*, BGB and PAR reject both.
- **Not checked.** I did not independently re-implement the full union. That would need D, GB, RD, RGB and the T-closure, and I ran out of time. So the claims of zero misses at n = 21, 23 and 25, and of exactly 2 misses at n = 26, remain UNVERIFIED by this audit.
- **Separate dependency.** The soundness of the T-closure rests on walk.md Lemmas 2–3, which are still under audit. The recursion in `cov.c` maps both non-trivial piece types to the single letter 1 (types 1 and 2 → 1), and that must match walk.md's Φ.

No counterexamples found.
