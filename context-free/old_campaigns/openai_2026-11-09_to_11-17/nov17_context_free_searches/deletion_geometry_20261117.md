# Hamming separation and deletion: proved search lemmas

These statements do not resolve context-freeness of primitive words. They were derived in this session and independently audited by the closure agent.

## Exact minimum distance between nonprimitive words

Let N>=2 and let ell be the smallest prime divisor of N. Over any alphabet with at least two letters, the minimum Hamming distance between distinct nonprimitive words of length N is exactly ell.

Choose prime power exponents p,q of two such words: w is a p-th power and v a q-th power, with p,q prime divisors of N. If p=q, every difference in the length-N/p roots repeats p times, so distinct words have distance at least p>=ell.

If p!=q, put g=N/(pq), d=N/p=gq and e=N/q=gp. Form a bipartite graph with left vertices the residues modulo d and right vertices the residues modulo e. Each position i contributes an edge between its two residues. The Chinese remainder theorem decomposes this graph into g disjoint copies of K_(q,p), with one edge for every compatible residue pair. Label each left vertex by the corresponding letter of w and each right vertex by the corresponding letter of v. The Hamming distance is exactly the number of edges with unequal labels.

In any component with a mismatching edge, take the set of vertices bearing the label at one endpoint of that edge. This is a nonempty proper vertex set; every edge of its boundary is a mismatch. The edge connectivity of K_(q,p) is min(p,q): deleting fewer edges cannot disconnect it. For completeness, a cut with a left vertices and b right vertices on one side has size a(p-b)+b(q-a); its nontrivial minimum is min(p,q), attained by isolating a vertex of minimum degree. Thus the distance is at least min(p,q)>=ell.

The bound is attained by a^N and (b a^(N/ell-1))^ell. Both are nonprimitive and they differ at exactly ell positions. This includes prime N, when the second word is b^N.

## Quantitative deletion consequence

Let w have length n>=3 and r maximal linear runs. Deleting any one letter in the same run gives the same word. Let D_i be the word obtained by deleting a letter from run i, for i=1,...,r. These r words are distinct, and

    Hamming(D_i,D_j)=j-i  (i<j).

Indeed, between the two deletion positions the compared words differ precisely where two consecutive letters of w differ. There is one such boundary between each successive pair of runs and no other mismatches.

Put ell equal to the smallest prime divisor of n-1. If D_i and D_j are both nonprimitive, the previous theorem forces j-i>=ell. Consequently at most ceil(r/ell) of these r deletion outputs are nonprimitive, and at least

    r-ceil(r/ell)

are primitive. In particular every nonconstant word has a primitive one-letter deletion. For n=2 the same statement holds because deleting either letter leaves a single letter.

This is stronger than the initially tested assertion restricted to primitive input words. It also shows why deletion existence cannot distinguish primitive words: every nonconstant proper power has such a deletion as well.

## Erasure saturation

For any word v and any two different letters a,b, the words va and vb differ in exactly one position. If their length is at least two, the distance theorem says they cannot both be nonprimitive. If their length is one, both are primitive. Thus at least one of va,vb is primitive, and

    Q / Sigma = Sigma*.

The same argument works on the left and for an insertion at any chosen position. Therefore deleting a final letter from Q by a rational transduction gives the entire free monoid; this transduction cannot yield a non-context-free obstruction. No use is made of closure under complement or arbitrary intersection.

## Scope

The distance theorem concerns substitutions, and the deletion theorem concerns a rational operation that loses information. Neither supplies the grammar-dependent universal quantifiers needed for a pumping contradiction, nor a sound inverse insertion rule for a grammar.
