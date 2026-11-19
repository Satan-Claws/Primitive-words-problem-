# Weighted scalar projections: exact transfer for fixed run counts

This lemma was proposed by the root agent and independently audited by the closure agent. It replaces the geometric mixed-period argument as the shortest proof of the full variable-run extension.

## 1. Finite weighted-projection identity

Fix m>=2 and let p_1,...,p_r be its distinct prime divisors, so r=omega(m). For each prime p dividing m, define the maximal periodic subspace

S_p={x in R^m : x_i=x_{i+m/p} for every cyclic index i}.

The primitive scalar tuple set is

P_m=N^m\(union_{p|m, p prime} S_p).

A paired tuple (alpha,beta) is primitive exactly when for every such p, alpha and beta do not both belong to S_p. Let W_m denote this paired-primitive set.

Then the following is an exact identity for nonnegative integer tuples:

(alpha,beta) in W_m
iff
there exists t in {0,1,...,r} such that alpha+t*beta is in P_m.          (1)

**Proof of right-to-left.** If alpha,beta both belonged to one S_p, then every linear combination alpha+t*beta would belong to it and would be imprimitive.

**Proof of left-to-right.** Fix a prime p dividing m. If two distinct real parameters t,u made both alpha+t*beta and alpha+u*beta belong to S_p, subtracting these vectors and dividing by t-u would imply beta in S_p; substituting back would imply alpha in S_p. This contradicts (alpha,beta) in W_m. Thus at most one parameter t can fail because of a particular S_p. Across r subspaces at most r parameters are bad. The r+1 distinct integers 0,...,r therefore contain a good one.

The proof uses only linear subspaces and the exact periodicity conditions. It assumes no genericity, bound on exponents, or uniqueness of the bad parameter across different primes.

## 2. CFL transfer through explicit inverse morphisms

Use distinct letters C_1,...,C_m and let

L_m={C_1^{x_1}...C_m^{x_m} : x in P_m}.

Suppose L_m is context-free. For each t=0,...,r use distinct letters A_1,B_1,...,A_m,B_m and define the morphism

h_t(A_i)=C_i,
h_t(B_i)=C_i^t.

When t=0 the B_i letters are erased, which is permitted in a morphism. Its inverse image h_t^{-1}(L_m) is context-free. Intersect with the regular language

A_1^+ B_1^+ A_2^+ B_2^+ ... A_m^+ B_m^+.

For input exponent tuple (alpha_1,beta_1,...,alpha_m,beta_m), the image under h_t is exactly

C_1^{alpha_1+t beta_1}...C_m^{alpha_m+t beta_m}.

Thus the finite union over t accepts precisely the positive paired tuples in W_m, by (1). Finally apply the morphism A_i->a and B_i->b. The result is exactly

Q_{a,b} intersect (a^+b^+)^m.

The last equality follows because positive alternating runs have unique exponent tuples, and any proper root starts in a, ends in b, and therefore repeats whole a/b run pairs. A proper word power has a prime power exponent dividing m, and corresponds exactly to simultaneous membership in one S_p.

Every operation above preserves context-freeness. There is no intersection with a nonregular language and no infinite union. For m=2q with q an odd prime, the previously constructed L_m is CF and only t=0,1,2 are needed.

## 3. Exact equivalence of the fixed scalar and full slices

For every fixed m>=2, the following are equivalent:

1. L_m is context-free.
2. Q intersect (a^*b)^m is context-free.
3. Q intersect (a^+b^+)^m is context-free.

To pass from (1) to (2), use the finite-state transducer that reads C_i in phase i and emits a, and on an epsilon transition emits b and advances to phase i+1. It handles zero coordinates and outputs exactly a^{x_1}b...a^{x_m}b.

To pass from (2) to (1), use the reverse phase-based rational transduction: in phase i consume a and output C_i; consume b, output epsilon, and advance to phase i+1. Require exactly m b transitions and end at phase m+1. Every word in (a^*b)^m has a unique such block parse.

The implication (1)->(3) is Section2.

For (3)->(2), first intersect the full slice with the regular restriction (a^+b)^m, forcing every b-run to have length1. The pair tuple is primitive exactly when its a-exponent tuple is primitive, since the b-exponent tuple is constant and hence has every candidate period. Then use a finite-state transducer that deletes the first a from each of the m positive a-runs and copies all remaining symbols. Its output has exponent tuple x obtained by subtracting the all-ones vector from the positive a-exponent tuple. Subtracting or adding the all-ones vector preserves every equality x_i=x_{i+d}, so preserves tuple primitivity. Conversely every nonnegative primitive scalar tuple x arises from the positive tuple x+(1,...,1), proving exact equality of the output with the scalar slice.

No assertion follows here about varying m without a uniform construction. In particular the finite family t=0,...,omega(m) depends on the fixed run count m.
