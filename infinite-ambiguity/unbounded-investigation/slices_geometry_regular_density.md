# Every regular primitive-only language omits a factor

Status: complete elementary proof, pending independent audit. Restricted to regular languages, not arbitrary CFGs. No novelty claim.

## Theorem

Let Sigma be a finite nonempty alphabet and let R be a regular language all of whose words are primitive. There exists a nonempty word v such that no member of R contains v as a contiguous factor.

### Proof

Choose a complete DFA recognizing R, with a finite nonempty state set S. Every word w induces a function T_w:S->S; its rank is |T_w(S)|. Choose a word v whose transformation has the smallest rank r among all word transformations. We may choose v nonempty: if the empty word realizes the minimum, every letter also does, since its rank is at most |S| and at least the minimum.

If a word w contains v as a factor, say w=xvy, its transformation has rank at most r, by composition of functions, and at least r by minimality. Thus it has rank exactly r. Its square transformation T_w^2 also has rank r by the same global minimality.

Put I=T_w(S). Since T_w(I) is contained in I and has the same size r, the restriction T_w|_I is a permutation of I. Let q>=1 be its order. For every state s, T_w(s) belongs to I, so

T_w^(q+1)(s)=T_w(s).

Consequently w^(q+1) induces the same transition function as w. If w were accepted, the nonempty proper power w^(q+1) would also be accepted, contradicting R being primitive-only. Hence no accepted w contains v. QED.

## Explicit growth bound

Let d=|Sigma|>=2 and ell=|v|. Partition a length-n word into floor(n/ell) disjoint blocks of length ell and a remaining suffix. Avoiding v as a factor implies in particular that none of those designated blocks equals v. Therefore

|R intersect Sigma^n| <= (d^ell-1)^floor(n/ell) d^(n mod ell)
                     = d^n (1-d^(-ell))^floor(n/ell).

The exponential growth rate is at most (d^ell-1)^(1/ell)<d. In particular every regular primitive-only language has exponentially vanishing density among all words.

The theorem is stronger than saying R misses some words: it excludes every word containing one fixed pattern. Thus no regular primitive-only language is factor-universal. The bound depends on R; there is no claim of one common gap below d for all such regular languages.

For a one-letter alphabet, the primitive language is finite and the conclusion is immediate as well.

## What the theorem does not prove

An arbitrary CFL has no finite transition monoid, so the proof does not extend to pushdown automata. The prime-Dyck-excursion grammar in grammar_structure.md is a concrete primitive-only CFL with full exponential growth rate 2, disproving such an extension. Nor can a countable increasing union of regular subsets be replaced by one regular language: the unique-factor hierarchy in construction.md eventually covers Q while each individual member satisfies this theorem.
