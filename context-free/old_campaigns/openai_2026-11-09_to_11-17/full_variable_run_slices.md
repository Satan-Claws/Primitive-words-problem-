# Context-freeness of full variable run-pair slices with 2q pairs

**Restricted theorem.** For every fixed odd prime q, put n=2q. Then

Q_{a,b} intersect (a^+b^+)^n

is context-free. In particular this handles the full 12-independent-exponent slice with six a/b run pairs, and the 20-independent-exponent slice with ten pairs. This is a theorem about a fixed regular restriction, not a solution of context-freeness of Q.

A shorter general proof now appears in `weighted_projection_lift.md`: scalar context-freeness for any fixed m transfers to the full run-pair slice through omega(m)+1 inverse morphisms. The geometric proof below is retained as an independent alternate derivation for m=2q.

The proof uses the fully explicit finite stratified cover and direct CFG compiler in `finite_stratified_run_slices.md`. That earlier construction is for primitive scalar n-tuples. The new ingredient here covers primitive pair-tuples whose two scalar projections are both imprimitive with different prime exponents.

## 1. Scalar and paired periodicity

For x in N^n, let

S_2={x : x_i=x_{i+q} for all i},
S_q={x : x_i=x_{i+2} for all i},
P_n=N^n\(S_2 union S_q).

Indices in these definitions are cyclic modulo n. S_2 consists of tuples repeating twice; S_q consists of alternating tuples repeating q times.

For two scalar tuples alpha,beta in N^n, the paired tuple

((alpha_1,beta_1),...,(alpha_n,beta_n))

is primitive precisely when

(alpha,beta) is outside (S_2 x S_2) union (S_q x S_q).             (1)

This follows because the only prime divisors of n are 2 and q. Let W_n denote the set in (1), flattened in the coordinate order

(alpha_1,beta_1,alpha_2,beta_2,...,alpha_n,beta_n).

If alpha is in P_n, or beta is in P_n, the pair tuple is automatically primitive. If both scalar tuples are imprimitive but the pair tuple is primitive, exactly one of the following occurs:

(a) alpha in S_2\S_q and beta in S_q\S_2;
(b) beta in S_2\S_q and alpha in S_q\S_2.

To verify exhaustiveness, each projection belongs to S_2 union S_q. If they shared either subspace, the pair would be imprimitive. If a projection belonged to their intersection, it would share a subspace with every imprimitive second projection. Thus the only remaining possibility is opposite exclusive membership.

## 2. Lifting the primitive-projection families

The earlier scalar result gives an explicit finite stratified semilinear cover of P_n.

To describe the flattened tuples with alpha in P_n, map scalar coordinate i to flattened coordinate 2i-1 in every base and period, set all beta base coordinates to zero, and add all beta unit vectors as periods. The order-preserving embedding preserves the noncrossing property of scalar periods; singleton periods never introduce crossings. This yields a finite stratified cover of P_n x N^n in the flattened order.

The same construction, using flattened coordinates 2i and freely varying odd coordinates, covers N^n x P_n.

It remains to cover cases (a) and (b) by primitive supersets admitting finite stratified descriptions.

## 3. Mixed-period comparison families

For each j modulo n define

D_j={ (alpha,beta) : alpha_j!=alpha_{j+2} and beta_{j+2}!=beta_{j+q+2} },

E_j={ (alpha,beta) : beta_j!=beta_{j+2} and alpha_{j+3}!=alpha_{j+q+3} }.

Every D_j and E_j is contained in W_n. Its shift-2 inequality rejects membership in S_q x S_q; its shift-q inequality rejects membership in S_2 x S_2. This soundness holds for all tuples in each family, not just the special mixed-period cases.

Now take case (a). Since alpha is outside S_q, choose j with alpha_j!=alpha_{j+2}. Since beta is in S_q, it alternates two values u,v. Because q is odd, beta is in S_2 exactly when u=v. But beta is outside S_2, so u!=v and every antipodal pair beta_i,beta_{i+q} differs. In particular the second inequality of D_j holds. Hence every tuple of type (a) belongs to some D_j.

The same argument with alpha,beta exchanged puts every tuple of type (b) in some E_j.

We have proved the exact finite cover

W_n = (P_n x N^n) union (N^n x P_n) union (union_j D_j) union (union_j E_j),             (2)

always using the flattened alternating coordinate order.

## 4. The two inequalities have noncrossing supports

Place the 2n=4q flattened coordinate positions on a circle in their ordinary order.

For D_j, measure clockwise offsets from the coordinate alpha_j. The first inequality joins offsets 0 and 4. The second joins offsets 5 and 2q+5. Since q>=3,

0 < 4 < 5 < 2q+5 <= 4q-1.

Thus the four endpoints occur as the two endpoints of one edge followed by the two endpoints of the other. They do not alternate on the circle, so the edges do not cross. Nonalternation is invariant under rotation of the cut from cyclic to linear order; therefore their supports are noncrossing in the actual flattened linear order as required by stratification.

For E_j, measure offsets from beta_j instead. The endpoints have exactly the same offsets 0,4,5,2q+5. The same conclusion applies.

The endpoints are distinct because the two edges use different coordinate axes. The limiting case q=3 gives offsets 0,4,5,11 in a circle of size12 and is valid.

## 5. Explicit finite generator scheme for two noncrossing inequalities

Let I={r,s} and J={t,u} be any disjoint, noncrossing two-coordinate supports in the flattened dimension 2n. Consider the set of vectors z satisfying z_r!=z_s and z_t!=z_u, with all other coordinates arbitrary.

Choose which endpoint h in I has the larger coordinate and which endpoint k in J has the larger coordinate. There are four choices. For each choose base

b=e_h+e_k

and period set

G={e_r+e_s, e_t+e_u, e_h, e_k} union {e_v : v outside I union J}.

The first pair of coordinates has minimum M>=0 and positive excess 1+R>=1 at h; the second pair similarly has minimum N>=0 and excess 1+S at k. Thus L(b;G) gives exactly this choice of signs of the two inequalities. Their four-way union gives exactly the full two-inequality set.

The only two-coordinate periods are the noncrossing pair supports I and J. All other periods are singletons. Therefore every such period set is stratified.

Apply this scheme to each D_j and E_j. Together with Section2 and the finite cover (2), it proves that W_n is a finite stratified semilinear set. The direct compiler in Section7 of `finite_stratified_run_slices.md` gives an explicit finite CFG scheme for its distinct-letter encoding.

## 6. Positive runs and the binary regular slice

Take distinct letters c_1,...,c_{2n} and the letter-bounded language of all flattened exponent vectors in W_n. The preceding construction and direct CFG compiler make it context-free.

Intersect it with the regular language

c_1^+ c_2^+ ... c_{2n}^+

to require all run lengths positive. Then apply the morphism

c_{2i-1} -> a,
c_{2i} -> b

for i=1,...,n. Context-free languages are closed under both operations.

Every output has exactly n alternating positive a/b run pairs, starts in a, and ends in b. Its positive exponent tuple is unique. If it is a proper power, its root starts in a and ends in b, so copies of the root concatenate at complete run-pair boundaries. The root exponent therefore divides n, and some prime p in {2,q} divides that exponent. Both scalar exponent tuples must then lie in S_p. Conversely simultaneous membership in S_p produces the corresponding pth word power.

Thus the morphism's output is exactly Q_{a,b} intersect (a^+b^+)^n, proving the restricted theorem with no missing zero-run or unary exceptions. The regular positive-run intersection is essential here: we do not infer word primitivity from arbitrary flattened zero-coordinate tuples.

## 7. Limits of the conclusion

The grammar scheme depends on the fixed run-pair count n=2q. There is no finite grammar construction here covering unbounded n or extra prime divisors, and no claim that an infinite union of the resulting languages is context-free. The theorem rules out a non-CF contradiction based on either the six-run-pair or ten-run-pair regular restriction.
