# An explicit finite stratified cover of primitive scalar 15-tuples

**Exact restricted result.** The set P_15 of primitive nonnegative integer tuples of length15 is a finite union of stratified linear sets. Consequently both Q intersect (a^*b)^15 and Q intersect (a^+b^+)^15 are context-free. The construction is for a fixed run count; it does not resolve context-freeness of Q.

## 1. Two periodic subspaces and eight linear witnesses

Index coordinates by k=0,...,14, with all subscripts below reduced modulo15. Let

U={x : x_k=x_{k+5} for every k},
V={x : x_k=x_{k+3} for every k}.

Thus U is the period5 subspace, corresponding to third powers, and V is the period3 subspace, corresponding to fifth powers. Since 3 and5 are the only prime divisors of15,

P_15=N^15\(U union V).

Identify positions by their residues (r,c) modulo5 and modulo3. The explicit CRT index is

k(r,c)=(6r+10c) mod15,

where 0<=r<5 and 0<=c<3. Write X_{r,c}=x_{k(r,c)}. The subspace U consists of arrays depending only on r; V consists of arrays depending only on c.

For each r in {1,2,3,4} and c in {1,2}, define the four-coordinate linear form

ell_{r,c}(x)=X_{r,c}-X_{r,0}-X_{0,c}+X_{0,0}.

There are eight such forms. Each has four distinct coordinates with coefficients +1,-1,-1,+1. It vanishes on both U and V, hence on U+V.

Conversely, if all eight forms vanish, set

u_r=X_{r,0},
v_c=X_{0,c}-X_{0,0}.

Then X_{r,c}=u_r+v_c for all r,c, including r=0 or c=0. Thus x belongs to U+V. The components u,v may have arbitrary real or integer signs; only their equality patterns are used.

Therefore

x outside U+V iff at least one ell_{r,c}(x) is nonzero.            (1)

Any nonzero form is already a certificate that x is outside both U and V, and therefore primitive.

## 2. Forty-five noncrossing two-inequality witnesses

For each j=0,...,14 and s in {4,5,6}, define

D_{j,s}={x in N^15 : x_j!=x_{j+3} and x_{j+s}!=x_{j+s+5}}.

Every D_{j,s} is contained in P_15: the first inequality rejects period3 and the second rejects period5.

The two comparison supports are disjoint and noncrossing. Relative to j around the coordinate circle, their endpoints occur at

0, 3, s, s+5,

with 0<3<s<s+5<=11<15. The endpoints thus do not alternate. This circular nonalternation is unchanged by the choice of linear cut, so the supports are noncrossing in the actual coordinate order0,...,14.

Now suppose x is primitive and belongs to U+V. Write

x_k=u_{k mod5}+v_{k mod3}.

Both u and v must be nonconstant. If u were constant, x would belong to V; if v were constant, x would belong to U.

Because addition by3 permutes all five residue classes modulo5, nonconstancy of u implies that some j satisfies

u_{j mod5}!=u_{j+3 mod5}.

The v terms agree at these two positions, so x_j!=x_{j+3}.

Because addition by5 is addition by2 modulo3 and cycles through all three residues, nonconstancy of v implies that v_t!=v_{t+5} for at least one residue t modulo3. The three choices j+4,j+5,j+6 represent every residue modulo3. Choose s in {4,5,6} so that j+s has such a residue. The u terms agree at positions j+s and j+s+5, so

x_{j+s}!=x_{j+s+5}.

Thus x belongs to D_{j,s}.

Combining this with (1) gives the exact finite-cover identity

P_15 = (union_{1<=r<=4,1<=c<=2} {x:ell_{r,c}(x)!=0})
       union (union_{0<=j<=14, s in {4,5,6}} D_{j,s}).           (2)

This equality is the key point: no restriction to U+V is applied as a language operation. The U+V split is used only to prove completeness of the finite union. Every component language in (2) is sound on its entire domain.

## 3. Explicit stratified generators for each nonzero linear form

The following finite scheme works for any linear form ell having coefficients +1 or -1 on a fixed support J and coefficient0 elsewhere. In the present application J has four positions, with two signs of each kind.

Let epsilon_i in {+1,-1} be the sign at i in J. Enumerate:

1. A surplus sign tau in {+1,-1}.
2. A noncrossing graph G on J whose edges join opposite signs.
3. A nonempty subset W of vertices in J of sign tau.
4. A distinguished vertex h in W.

For every such finite choice use base b=e_h and periods

- e_i+e_j for every edge {i,j} of G;
- e_i for every i in W;
- e_i for every i outside J.

The resulting linear set is stratified: its only two-coordinate periods are the noncrossing graph edges. Every graph-edge period has ell-value0, every W singleton has ell-value tau, and the base has ell-value tau. Hence every generated tuple has a nonzero ell-value of sign tau.

Conversely, take x>=0 with ell(x)!=0. On the ordered support J, assign mass x_i to each coordinate and its given sign. As long as both signs have positive mass, choose two positions of opposite signs adjacent among the currently positive positions. Subtract the smaller mass from both and record that positive integer amount on their connecting edge. Delete coordinates whose mass becomes zero. The process terminates because every step removes at least one active coordinate.

The recorded edges are noncrossing. When an edge is recorded, no currently active coordinate lies strictly between its endpoints; a later edge therefore cannot have exactly one endpoint strictly inside it, since inactive coordinates never become active again. Shared endpoints cause no crossing.

At termination, all remaining mass has the sign of ell(x), and at least one coordinate retains positive mass. Let W consist of those remaining positions and let G consist of the recorded edges. Choose h in W; its remaining mass is at least1. Use one copy of e_h for the base and the rest for singleton periods. The edge coefficients reproduce all canceled mass, and the outside-J unit periods reproduce arbitrary outside coordinates. This expresses x in one of the enumerated linear sets.

Thus the finite scheme describes exactly {x>=0:ell(x)!=0}. The bases are individual unit vectors, not an unbounded collection of remainders.

## 4. Explicit stratified generators for each D_{j,s}

Let I={j,j+3} and K={j+s,j+s+5}; these are disjoint noncrossing supports. Choose which endpoint h in I is larger and which endpoint l in K is larger. There are four choices. For each use base

b=e_h+e_l

and periods

G={e_j+e_{j+3}, e_{j+s}+e_{j+s+5}, e_h, e_l}
  union {e_i : i outside I union K}.

Each compared pair has an arbitrary nonnegative minimum and a positive excess at its chosen larger endpoint. Hence the four linear sets describe exactly D_{j,s}. Their only two-coordinate periods are the two noncrossing comparison supports, so each period set is stratified.

Combining Sections3 and4 with the finite identity (2) gives a fully explicit finite stratified semilinear presentation of P_15.

## 5. Language consequences and scope

Apply the direct finite CFG compiler from Section7 of `finite_stratified_run_slices.md` to every displayed linear set, using distinct terminals C_0,...,C_14 in order. A fresh start symbol selects among the finitely many component grammars. This constructs the letter-bounded CFL

L_15={C_0^{x_0}...C_14^{x_14}:x in P_15}.

The fixed-phase rational transducer inserting one b after each block yields exactly Q intersect (a^*b)^15, including zero a-run lengths.

The general weighted-projection lemma in `weighted_projection_lift.md`, with omega(15)=2 and t in {0,1,2}, then yields context-freeness of the full independent-run slice Q intersect (a^+b^+)^15. It uses only inverse morphisms, regular intersection, finite union, and a final morphism.

No claim about a grammar uniform in the run count is made. This fixed-count construction prevents a non-CF contradiction based on the 15-run scalar or run-pair regular slice, but it does not answer the original question about Q.

## 6. Optional exact generalization: two distinct odd primes

The same argument works for n=pq where 3<=p<q are distinct odd primes. Use CRT coordinates modulo q and modulo p. Mixed rectangle differences vanish exactly on the sum of the period-q and period-p subspaces. Outside that sum, use nonzero rectangle forms as above.

Inside the sum, write x_k=u_{k mod q}+v_{k mod p}, with both components nonconstant. Choose a mismatch between j and j+p in the u component; this exists because gcd(p,q)=1. Choose the start i of a distance-q mismatch among the p consecutive positions j+p+1,...,j+2p, which cover every residue modulo p. Then the four endpoints have cyclic offsets

0, p, i-j, i-j+q,

and satisfy 0<p<i-j<i-j+q<=2p+q<pq. The last strict inequality holds for all distinct odd primes p<q: at the smallest pair (3,5) it reads11<15, and q(p-1)-2p increases thereafter. The supports are therefore disjoint and noncrossing. Finitely many such two-inequality families complete the cover.

Consequently P_{pq}, the scalar binary slice, and the full variable run-pair slice are CF for every fixed product of two distinct odd primes. Together with the earlier 2q construction and prime-power slices, this covers every squarefree run count having at most two prime factors, while remaining a fixed-count result.
