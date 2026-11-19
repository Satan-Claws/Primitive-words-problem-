# Closure investigation: exact results and limits

These are partial lemmas, not a resolution of context-freeness.

## Alphabet transfer

For an alphabet C={c_1,...,c_k}, define h(c_i)=ab^i. This is an injective morphism and preserves and reflects primitivity, including the empty-word convention.

A power w=v^r maps to h(w)=h(v)^r. Conversely, if h(w)=u^r with r>=2, then u begins with a and ends with b, because h(w) does. Consequently the boundaries between copies of u are codeword boundaries: every a starts one codeword, and the following b-run uniquely identifies its source symbol. All b-run lengths in u belong to {1,...,k}, so u=h(v) for a unique v and injectivity yields w=v^r. Also h(epsilon)=epsilon. Hence Q_C=h^{-1}(Q_{a,b}). Binary context-freeness would therefore transfer to every finite alphabet through inverse morphism; the reverse implication follows by regular intersection.

## Exact bounded-run characterization

Let R_m=(a^+b^+)^m and write w=a^{alpha_1}b^{beta_1}...a^{alpha_m}b^{beta_m}. Then w is a proper power iff the cyclically indexed tuple ((alpha_1,beta_1),...,(alpha_m,beta_m)) repeats p times for some prime p dividing m.

Indeed, any root of w starts with a and ends with b; its run-pair count divides m, and its exponent pairs repeat. Conversely repeated exponent pairs give the corresponding word power. Taking a prime divisor of any root exponent gives the claimed formulation.

If m is a prime power p^t, this slice is CF: choose a coordinate whose exponent differs from the coordinate shifted by 2m/p in the flattened 2m-vector. For each of the finitely many coordinate choices a one-stack automaton compares the two selected unary runs and ignores all other runs. Their finite union is exactly Q intersect R_m. For m=1 the entire slice is primitive. This argument does not extend by taking intersections when m has multiple prime divisors.

For scalar tuples x=(x_1,...,x_m) and words a^{x_1}b...a^{x_m}b, with x_i>=0, the analogous criterion uses scalar periodicity. Zero a-exponents are allowed because the b occurrences remain canonical separators. The matching lemma below concerns this scalar slice, not all 2m-dimensional run-pair slices.

## Safe noncrossing matching lemma for 2q scalar coordinates

Let n=2q with q an odd prime. For p in {2,q}, let S_p be the real vector subspace of p-fold repeated tuples, namely x_i=x_{i+n/p} with cyclic indices. For a noncrossing perfect matching M of positions 1,...,n in their linear/circular order, let V_M be spanned by e_i+e_j over matched pairs {i,j}.

**Lemma.** If x is outside S_2 union S_q, there is a noncrossing perfect matching M such that (x+V_M) is disjoint from both S_2 and S_q. In particular every independently chosen nonnegative equal increment of the matched coordinate pairs keeps the tuple primitive.

**Proof.** Put A(x)=sum_{i=1}^n (-1)^i x_i. Every edge of a noncrossing perfect matching joins opposite-parity positions, so A vanishes on V_M. Also A vanishes on S_2: period q is odd and the two copies cancel.

First suppose A(x) is nonzero. Then x+V_M misses S_2 for every M. Consider the two adjacent matchings

M_0={{1,2},{3,4},...,{n-1,n}},
M_1={{2,3},{4,5},...,{n,1}}.

The last edge of M_1 is an outer edge, so both matchings are noncrossing in linear order. Membership x in S_q+V_{M_0} means all differences x_{2j-1}-x_{2j} have a common value t. Membership x in S_q+V_{M_1} similarly means all x_{2j}-x_{2j+1} have a common value s, cyclically. If both memberships hold, summing all adjacent differences yields q(t+s)=0, hence s=-t; the coordinates therefore have period 2, contradicting x outside S_q. At least one matching excludes S_q as well.

Now suppose A(x)=0. Since x is outside S_2, choose i with x_i!=x_{i+q}. The edge {i,i+q} leaves q-1 positions on either side, both even. Pair adjacent positions on each side to extend it to a noncrossing perfect matching M. Every vector in S_2+V_M has equal coordinates i and i+q, so x is outside this sum.

If x were in S_q+V_M, write x=y+v with y in S_q and v in V_M. Since A(x)=A(v)=0, A(y)=0. A period-2 vector y alternates values c,d and A(y)=q(d-c), so c=d. Constant vectors lie in V_M, because summing all matching generators gives the all-ones vector. Thus x would belong to V_M, a subset of S_2+V_M, contradiction. Therefore x is outside S_q+V_M also. This proves the lemma.

## Precise limitations

- The matching lemma gives primitive affine families with stratified period generators through every primitive scalar tuple when m=6 or 10 (indeed 2q). It prevents a contradiction based solely on requiring a primitive tuple to admit a noncrossing simultaneous-growth direction.
- It does NOT prove that the entire primitive slice is a finite union of stratified linear sets. The needed bases depend on unbounded coordinate differences; a finite decomposition has not been supplied.
- It does NOT prove context-freeness of any composite-run slice, let alone Q.
- It does NOT address arbitrary pumping/Ogden decompositions, locality bounds, or all run-pair exponents.
- Rational transductions cannot silently duplicate separated unbounded exponents. For example the exact image {a^n b a^n b:n>=0} of a regular unary domain would be nonregular, so no rational transduction can have exactly that image; rational images of regular languages are regular.

An exact rational nullspace computation for n=6 independently checked all five Catalan matchings and all 32 choices of obstruction subspace. The mathematical proof above supersedes that finite check. Computation script: /tmp/closure_periods.py.

## Complete escape for one short defective run with defect-only marks

Fix m>=2, 1<=D<N, and

w=a^{N-D}b(a^N b)^{m-1}.

The word is primitive because its scalar a-run tuple has a unique short entry. The argument below applies to every choice of at least three distinguished positions confined to that short run, and to every set of excluded positions disjoint from the distinguished ones.

Assume at least one a-position in an ordinary run is not excluded. Let v consist of the penultimate distinguished a-position of the short run, and let x consist of one unexcluded a-position in an ordinary run. Write w=uvzxy with the intervening and exterior factors determined by these choices. Then:

- v and x each have length one and contain no excluded position;
- v is distinguished;
- u contains an earlier distinguished position, and z contains the final distinguished position, so the stronger side condition that u,v,z each contain a distinguished position holds;
- the full span vzx contains exactly two distinguished positions. Hence its distinguished count is at most K, and at most K^{s+1} for any excluded count s in the span, whenever K>=2.

Thus this decomposition satisfies both the usual Ogden location restrictions and the stronger Bader–Moura restrictions, regardless of how many excluded positions lie in the intervening factor z.

For pumping exponent t>=0, the modified a-run lengths are

N-D+t-1, N+t-1, N,...,N.

The first two values differ by the fixed nonzero D. If neither equals N, each has multiplicity one; if one equals N, the other has multiplicity one. Any tuple that repeats p>=2 times gives every coordinate value a multiplicity divisible by p. Therefore these tuples are primitive for every t>=0. The a-run lengths remain nonnegative even for t=0, and the b-separated scalar-tuple characterization also covers zero runs.

The only way to exclude this construction, while retaining marks solely in the defective run, is to exclude every a-position of every ordinary run. That gives e>=(m-1)N>=N, whereas d<=N-D<N. It is incompatible with the Bader–Moura global hypothesis d>K^{e+1} for K>=2; even a hypothetical linear condition d>K(e+1) would fail.

**Conclusion:** this entire one-short-defect / defect-only-marking approach cannot yield a contradiction from the stated pumping lemmas. Choosing D as an lcm of bounded pump lengths does not affect the escape: equal increments in two runs keep their discrepancy D forever.

The standard strong Bader–Moura form used here is stated in Berstel's author-hosted Handbook chapter, Theorem 2.4: https://www-igm.univ-mlv.fr/~berstel/Articles/1990HandbookCfl.pdf . Its global inequality is exponential, d>N^{1+e}; the local bound is r<=N^{1+s}. Some PDF search extracts flatten these superscripts and misleadingly display a linear inequality. Only ordinary theorem background was searched, not the primitive-word problem or its open status.
