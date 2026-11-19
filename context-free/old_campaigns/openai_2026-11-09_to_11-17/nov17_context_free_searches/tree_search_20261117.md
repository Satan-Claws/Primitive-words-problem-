# Uniform derivation-tree route, 17 November 2026

This working note does not resolve context-freeness of primitive words.

## Initial defect experiment (already present in earlier notes)

For m>=2, r,n>=2 and r!=n, the word a^r b (a^n b)^(m-1) is primitive. Increasing the first two a-run lengths by the same integer t>=-1 preserves primitivity: their lengths remain distinct, and every length different from n occurs exactly once (for m=2 the two lengths simply differ). A proper power would repeat every run length occurrence. Under Ogden marking concentrated in the first run, choose the last marked a for one pump and the first a of the next run for the other; the pumped interval has just one marked position. This is not a new result: closure_notes.md already contains the escape.

## New route: finite period-weight palette for a fixed grammar

Potential invariant: for a single fixed CFG G, all fixed-run restrictions

    L(G) intersect a* b a* b ... a* b   (m copies of a*b)

have stratified semilinear descriptions using period vectors supported on at most two coordinates, whose nonzero entries come from a finite grammar-dependent palette independent of m. The bases and number of components may depend on m.

Mechanism under examination: put G in epsilon-free CNF (treat possible epsilon separately; Q excludes it). Mark the b-producing leaves. The minimal subtree joining these leaves has at most m-1 branching vertices. Between branching vertices, every off-skeleton subtree produces only a's. Such unary nonterminal languages are regular, with ultimately periodic length sets depending only on G. A skeleton chain is a path through a finite graph of nonterminals. Each edge emits a unary language on its left or right. Simple directed cycles have bounded length. Their minimal unary realizations provide bounded two-coordinate period weights; unary repetition within their side branches supplies singleton periods. A chain's two sides affect at most the two boundary a-runs of its b-containing yield. Different chains occupy nested or disjoint spans, suggesting stratification.

Outstanding proof obligation: explicitly decompose each path language with unary-set edge weights into finitely many linear sets while maintaining noncrossing support globally and controlling edge-label choices. A standard semilinear Parikh theorem alone does not establish the uniform palette unless its construction and grammar dependence are tracked. A second, currently entirely missing, ingredient would show that no fixed finite palette suffices for all primitive-run tuple complements. Merely restating that desired obstruction is not progress to a resolution.

## Proved uniform skeleton lemma

**Lemma.** Fix a context-free language L over {a,b}. There are effectively obtainable constants C,K>=1 and a finite set F subset N^2 such that, for every m>=1, the exponent set

    E_m = {(x_1,...,x_m) in N^m : a^{x_1}b ... a^{x_m}b is in L}

is a union of at most K^m linear sets. Every such component has a base with coordinate sum at most C m and at most C m period vectors. Each period is either u e_i or u e_i+v e_j with (u,v) drawn from a fixed finite palette obtained from F. The two-coordinate supports within one component are noncrossing: there are no supports {i,k},{j,l} with i<j<k<l. In particular every nonzero period entry is at most C after increasing C.

**Proof.** Remove epsilon and unit productions and use ordinary CNF for the nonempty part of L. This changes membership neither at the words under consideration nor at any positive m; no ambiguity-preservation assertion is needed. For each nonterminal A, the unary language L(A) intersect a* is context-free by regular intersection and regular because unary CFL length sets are semilinear. The latter follows from Parikh's theorem: in one dimension every linear set, and hence every semilinear set, is ultimately periodic. Fix a finite automaton for each of these finitely many unary languages.

Construct one finite automaton M over the two-letter alphabet {ell,r}. Its boundary states include all grammar nonterminals. For every CNF rule A->BC, add a path from A to B labeled by a word r^t for every t such that a^t is in L(C), using a copy of the fixed unary automaton for C. Similarly add paths from A to C labeled ell^t for t in the unary length set of B. Epsilon transitions into and out of these copied automata are allowed. Thus a path between nonterminal states specifies a derivation chain in which the continued child is the only child containing b, while all side children yield only a's. Conversely every such chain produces a path. The number of emitted ell symbols is the total a-output to the left of the bottom b-containing yield; the number of emitted r symbols is the total to its right. Reversal of the order of right side branches does not change their unary yield or its length.

For every ordered pair of nonterminals A,B, choose a finite semilinear representation of the Parikh image of the regular language of M-paths from A to B. There are finitely many endpoint pairs. Fix a constant B_0 bounding the coordinate sums of every base and every period in all these representations, the number of periods in any one linear component, and the number of components for any endpoint pair. Such a constant is effective from the fixed automaton. Empty paths are included when appropriate. Importantly, B_0 does not depend on m.

Now take a derivation tree for a word with exactly m occurrences of b. Retain its b-containing nodes. A retained node has either one or two retained children. Suppress all one-child stretches. What remains is an ordered full binary tree with m leaves, labeled by b-producing productions at the leaves and by productions with two b-containing children at the m-1 internal vertices. Include the possible one-child stretch from the original root down to the first essential node. There are exactly 2m-1 stretches if stretches of length zero are included, one entering each essential node. Each stretch has endpoint nonterminals and belongs to the fixed path relation just described.

Initially allow an (m+1)-coordinate run vector, including the a-run after the final b. A stretch whose bottom yield contains the consecutive b-leaves l through r contributes all its ell output to coordinate l and all its r output to coordinate r+1. Replacing each fixed chain relation by one of its linear components and summing all 2m-1 contributions therefore gives one linear set, exactly: all chain choices are independent once the essential tree, productions, endpoint labels, and chosen semilinear components are fixed. Its base norm and number of periods are at most B_0(2m-1). Its period entries belong to the finite palette of the fixed chain representations.

The leaf intervals attached to stretches form a laminar family. For disjoint consecutive intervals [l,r] and [s,t] with r<s, their boundary supports satisfy l<r+1<=s<t+1, allowing shared endpoints. For nested intervals, the corresponding boundary supports nest or share endpoints. Consequently two-coordinate period supports never cross. Singleton or zero periods do not affect this property; delete zero periods.

There are at most 4^{m-1} ordered full binary trees with m leaves. The finite choices of productions, endpoint nonterminals and semilinear components per essential node and stretch give at most D^{2m-1} additional choices for a constant D depending only on G. Increasing K bounds their product by K^m.

Finally enforce that the (m+1)st coordinate is zero. All bases and periods are nonnegative, so discard a component if its final base entry is positive; in each remaining component discard all periods whose final entry is positive. Project away the final coordinate. This procedure yields exactly E_m without splitting components and preserves all stated bounds and stratification. QED.

**Scope.** This is stronger than independently applying a bounded-language theorem for every m: it records uniform bounds inherited from one grammar. It does not prove that the primitive exponent sets violate any bound. Existing constructions using unit and equal-pair periods obey the finite-palette requirement. An obstruction must involve the entire uniform package (base size, number of components, shared palette, and possibly compatible grammar labels), or establish that one of these bounds fails for primitive tuples.

**Exact potential missing lemma.** For every constants C,K and finite period palette F, there exists m for which the primitive scalar tuple set

    P_m={x in N^m : a^{x_1}b...a^{x_m}b is primitive}

admits no stratified linear cover satisfying all bounds in the uniform skeleton lemma. No proof or counterexample to this missing lemma is currently supplied. It is stronger than necessary for ruling out a CFG and may be false; it must not be treated as equivalent to the original question.

## Why growing coefficients alone may not obstruct the uniform palette

Let m=product_{j=1}^r p_j^{e_j}, and identify the cyclic index set Z/mZ with the product of Z/p_j^{e_j}Z by CRT. The prime-period subspace S_{p_j} consists of functions constant along shifts by m/p_j; in the jth coordinate this means constant on each p_j-element fiber over reduction modulo p_j^{e_j-1}.

Choose in each factor two distinct points in the same such fiber, and form the tensor product of their signed differences. This gives a functional c on all m coordinates with exactly 2^r nonzero coefficients, each +1 or -1. For every j, pairing the two selected positions in factor j shows c annihilates S_{p_j}. Hence

    c dot x != 0  =>  x is outside every S_{p_j}.

The collection of these tensor differences spans the intersection of the orthogonal complements of the S_{p_j}. To see this, in each factor the elementary differences span the vectors with sum zero on each fiber; applying the standard tensor decomposition to these subspaces identifies the intersection with their tensor product. Consequently such a certificate exists exactly when x is outside sum_j S_{p_j}.

These certificates have bounded coefficients even when m has arbitrarily many distinct prime factors. Noncrossing cancellation for a signed sum can therefore use unit singleton/equal-pair generators; growing arithmetic coefficients are not necessary on this generic stratum. The difficult stratum consists of x in sum_j S_{p_j} but in no individual S_{p_j}. It is nonempty: at m=6, the tuple x_i=(i mod 2)+(i mod 3), indexed i=0,...,5, is the sum of a period-2 and a period-3 tuple and has no period 1,2,3. This observation supplies neither a uniform CFG nor a full finite-cover theorem.
