# newmech: multi-split linkage inside one derivation tree (split-localization + disjoint-node multiplicativity)

**Mechanism (one line).** Link *all* splits of a single tree through the inside/outside factorization
amb(uxv) ≥ out_A(u,v)·in_A(x), and its multi-node version (product over disjoint nodes); *not* in §6 because it is
neither a one-split rank bound, nor a slice cover, nor a count sandwich: it constrains where ambiguity can sit inside
every tree of every word, at fixed length over all letters (so it also sees the cross-ratio core P_cop).

Script: `round2/scripts/newmech_check.py` (12 random CNF grammars, |V| = 4, all words of length 3..9 with amb > 0:
8837 words, 0 failures of Lemma B and Lemma M) [computational].

Notation. G is CNF, cycle-free (CNF conversion keeps counts, §4.3). For a node v of a tree T let A_v be its label
and y_v its yield; in_A(x) = #A-trees with frontier x; out_A(u,v) = #one-hole S-trees with frontier u·A·v.

## 1. Lemma B (exact top-balanced identity) [written proof + computational]
For |w| = n ≥ 3 call a span *big* if its length is > 2n/3 and *in range* if its length lies in (n/3, 2n/3].
Big nodes of a tree form a root chain (two big spans overlap, so they are nested). The lowest chain node has
two children of length ≤ 2n/3 summing to > 2n/3, so one is in range; a sibling of a big child has length < n/3.
Select the left in-range child of the lowest chain node. Then every tree has exactly one selected node, and

  amb(w) = Σ_{(A,i,j) in range} out^top_{A,i,j}(w) · in_A(w[i,j)),

where out^top counts contexts whose hole-ancestors are all big and whose selection rule holds (this depends only on
positions). The sum has at most |V|·n² nonzero terms.
**Cor B (one-level linkage is worth only a polynomial).** For some single (A,i,j),
out^top·in ≥ amb(w)/(|V|n²). So superpolynomial ambiguity, if it exists, is already superpolynomial in **one**
split's inside factor or **one** split's context factor. Linking many splits at one level gains at most |V|n².

## 2. Lemma T (rectangle transfer) [written proof]
If S ⇒* uAv and A ⇒* x, then amb(u x v) ≥ out_A(u,v)·in_A(x), because distinct (context, inside) pairs give distinct
trees. So high inside ambiguity in_A(x) ≥ m transfers to the whole column {u'xv' : S ⇒* u'Av'} ⊆ Q, and high context
ambiguity transfers to the whole row {u x' v : x' ∈ L_A}. Within one interchange class (A, i, j) no two
(context, filler) pairs give the same word, so the Ogden–Ross–Winklmann interchange produces **no** multiplicity by
itself. This is the exact reason the interchange-with-multiplicities direction reduces to rectangles (§6, one split).

## 3. Lemma M (ambiguity skeleton) [written proof + computational]
Call a node v *locally ambiguous* if in_{A_v}(y_v) ≥ 2. For pairwise disjoint nodes v_1..v_r of one tree T,
replacing the subtree at each v_i independently gives distinct trees, so amb(w) ≥ Π_i in_{A_{v_i}}(y_{v_i}) ≥ 2^r.
Also in_parent ≥ in_child (fix the sibling subtree), so Amb(T) = {locally ambiguous nodes} is closed upward.
**Hence under amb ≤ C|w|^k, every tree of every word has an ambiguity skeleton Amb(T) that is a rooted subtree
with at most k·log₂|w| + log₂C leaves.** Everything hanging off it is uniquely parsed by its own nonterminal.
(The DP in the script computes the maximum antichain D over all trees and checks 2^D ≤ amb; max D seen = 4.)

**Sufficient criterion W (width forcing).** If for each (C,k) some w ∈ Q has a tree that is forced to contain
more than k·log₂|w| + log₂C disjoint locally ambiguous nodes, the negative resolution follows. This is per word,
uniform in C and k, and polynomial in |w|.

## 4. Status: collapses (two branches, both onto known blocks)
- **Width branch (criterion W).** Forcing a node to be locally ambiguous means forcing the inside language
  L_{A_v} ∩ Σ^{|y_v|} to be inherently ambiguous on y_v *relative to its contexts*. L_A is an arbitrary
  language: only L_A·contexts ⊆ Q is constrained. A primitivity defect inside a subword is washed out by the
  surrounding non-commuting material. This is exactly §6 "local defects do not survive" (`PA/poly_S4I.md`).
  [assessment]: no forcing of even 2 disjoint ambiguous nodes is available.
- **Path branch.** If width stays O(log n), superpolynomial ambiguity must accumulate along O(log n) root paths of
  nested alternatives. On (ab*)^n nested alternatives are exactly laminar ring choices, i.e. the Lemma 3P skeleton
  sum. That is the slice-ply problem of §4.3/§4.4 (S_N, TILE_k, G3**), not a new mechanism. [assessment]
- **Rotation linkage via G′** (`R2/cyclic.md` Thm C) collapses at once. amb_{G′} is invariant under all rotations.
  A cyclic block shift maps a laminar pair family to a laminar one, because line non-crossing equals circle
  non-crossing. So the G′ decomposition is a Z_n-symmetrised laminar cover of ply ≤ n·(ply of G): a factor-n change
  only. [written proof]
- **Wich normal form** (no C_exp ⇒ unique pumping tree per interface) restricted to a slice is Structure (c)
  (simple rings, unique side trees), already used in Lemma 3P. So the "DAG of SCCs" normal form adds nothing on
  slices, and every word beginning with a lies in the slice (ab*)^{#a}. [assessment]

## 5. Exact gap (the one statement that would make this mechanism live)
**W-forcing lemma (open).** There exist words w_n ∈ Q (|w_n| ≤ poly(n)) and disjoint intervals
I_1..I_r ⊆ [|w_n|], with r = ω(log n), such that for every cycle-free CNF G with L(G) = Q, some tree of w_n has,
for each t, a node v_t spanning I_t with in_{A_{v_t}}(w_n[I_t]) ≥ 2.
By Lemma M this implies the negative resolution. It is blocked as long as each L_A may be chosen unambiguous on
the given subword. A proof must show that "L_A·Ctx_A ⊆ Q, Ctx_A rich" forces A to be ambiguous on a prescribed
subword. No candidate family is known.
