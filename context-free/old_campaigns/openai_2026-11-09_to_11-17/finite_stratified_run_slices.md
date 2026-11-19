# Finite stratified cover for primitive scalar tuples of length 2q

**Scope:** q is an odd prime. This establishes context-freeness only for the bounded binary slice consisting of primitive words with exactly 2q occurrences of b and ending in b. In particular it handles 6 and 10 scalar a-run coordinates. It does not establish context-freeness of all primitive words or of the unrestricted 4q-dimensional a/b-run-pair slice.

## 1. Definitions and the finite-cover identity

Put n=2q, with coordinate indices 1,...,n. Let e_i be the ith unit vector. All tuple coordinates are nonnegative integers. Define

- S_2 = {x : x_i=x_{i+q} for i=1,...,q}, the tuples repeating twice;
- S_q = {x : all odd coordinates equal and all even coordinates equal}, the tuples repeating q times;
- P_n = N^n \ (S_2 union S_q);
- A(x) = sum over odd i of x_i minus sum over even i of x_i.

Because the only prime divisors of n are 2 and q, P_n consists exactly of the primitive scalar tuples.

Every edge E={o,e} joining an odd position o and an even position e has normalized difference d_E=x_o-x_e and pair period g_E=e_o+e_e.

Consider the two noncrossing adjacent matchings

M_0={{1,2},{3,4},...,{n-1,n}},
M_1={{2,3},{4,5},...,{n,1}}.

For either such matching define

F_M={x : sum_{E in M} d_E != 0 and the values d_E are not all equal}.

For each antipodal edge E_i={i,i+q}, i=1,...,q, form a noncrossing perfect matching N_i by pairing consecutive positions within each of the two open cyclic arcs separated by E_i. Each arc has q-1 positions, an even number. For each other edge F of N_i define

C_{i,F}={x : d_{E_i} != 0 and d_F != d_{E_i}}.

Then the exact finite-cover identity is

P_n = F_{M_0} union F_{M_1} union (union over i=1,...,q and F in N_i\{E_i} of C_{i,F}).       (1)

**Soundness.** The sum of the normalized differences of any odd-even perfect matching is A(x). Every x in S_2 has A(x)=0 because q is odd. Every x in S_q has all normalized differences equal. Thus every F_M misses both S_2 and S_q. An antipodal difference is zero on S_2, while every pair of normalized differences agrees on S_q. Thus every C_{i,F} also misses both subspaces, independently of the value of A(x).

**Completeness when A(x)!=0.** If all differences for M_0 equal t and all differences for M_1 equal u, then their sums give qt=A(x)=qu, hence t=u. The neighboring difference equations then imply x_1=x_3=...=x_{n-1} and x_2=x_4=...=x_n. Such x belongs to S_q. Therefore, for x outside S_q, at least one of the two matchings has differences not all equal; since A(x)!=0, its F_M contains x.

**Completeness when A(x)=0.** For x outside S_2 choose an antipodal edge E_i with d_{E_i}!=0. If every difference in N_i equaled d_{E_i}, then A(x)=q*d_{E_i} would be nonzero. Consequently some F in N_i has a different difference, putting x in C_{i,F}.

It remains to give genuinely finite stratified linear-set descriptions of every family in (1). These are provided below. No unbounded collection of bases is used.

## 2. Stratification convention

For a finite base vector b and finite period set G in N^n, write

L(b;G)={b+sum_{g in G} k_g*g : every k_g is a nonnegative integer}.

A period set is stratified if each period has at most two nonzero coordinates and no two two-coordinate supports cross: there are no supports {i,k}, {j,l} with i<j<k<l. Singleton supports and shared endpoints never create crossings. Bases can have arbitrarily many nonzero coordinates; stratification constrains periods only.

Every period below is a unit vector or a sum of two distinct unit vectors. All indexing sets, graphs, sign choices, and positive-generator subsets are finite functions of n.

## 3. Finite cancellation lemma

Fix a finite ordered set J of positions, each assigned a sign sigma_j in {+1,-1}. Consider positive integer magnitudes r_j>=1 whose signed sum is nonzero.

The following finite scheme describes exactly these magnitude vectors by stratified linear sets.

1. Choose a surplus sign tau in {+1,-1}.
2. Choose a noncrossing graph G on J, with every edge joining opposite signs.
3. Choose a nonempty set U of vertices of sign tau. These supply singleton periods.
4. Let B consist of edge periods e_j+e_k for edges in G and unit periods e_j for j in U.
5. Choose a subset H of B such that (a) the supports of H cover every vertex of J, and (b) H contains at least one singleton period.
6. Output L(sum_{h in H}h; B).

There are finitely many choices. Every generated vector has every r_j>=1 because H covers J. Its signed sum has sign tau and is nonzero because every edge period has signed sum zero, every singleton has signed sum tau, and the base includes a singleton. Its periods are stratified by the noncrossing requirement.

Conversely, take any positive r with nonzero signed sum. While positive mass remains at both signs, choose two positions of opposite signs that are adjacent among the currently positive positions. Transfer the minimum of their masses to the corresponding edge, then delete every position whose remaining mass becomes zero. Every transfer has a positive integer amount. At least one active position disappears per step, so the procedure terminates. The remaining mass is at positions of a single sign, necessarily the sign of the original nonzero sum; assign it to singleton periods.

The resulting edge supports are noncrossing. At the time an edge is created, no currently positive vertex lies strictly between its endpoints. A later edge therefore cannot have exactly one endpoint strictly between them: those interior positions have already become inactive and never reactivate. Earlier edges satisfy the same property inductively. Shared endpoints are permitted.

Let G and U be the supports that actually occur. Every vertex initially had positive mass and therefore lies on an edge or singleton with positive coefficient. All occurring coefficients are positive integers; take H to be all these occurring generators (or any covering subset containing a singleton). Subtracting one copy of each member of H leaves nonnegative coefficients, proving membership in an enumerated linear set.

The lemma also works when all signs are the same: G is empty and U=J supplies all mass. If J is empty there are no admissible vectors, so output no sets.

## 4. Finite stratified description of F_M

Here M is M_0 or M_1, so all its edges are adjacent in cyclic order; in linear order the only possible nonconsecutive edge is the outer edge {1,n}. Such matching edges cannot cross any edge between arbitrary remaining positions, except potentially by sharing endpoints, which is allowed.

Split into the finitely many exact sign patterns sigma_E in {-1,0,+1} of the differences d_E. For every nonzero sigma_E, let a_E be the odd endpoint if sigma_E=+1 and the even endpoint if sigma_E=-1. Then uniquely

x = sum_{E in M} z_E*g_E + sum_{sigma_E!=0} r_E*e_{a_E},

where z_E>=0 and r_E>=1. For a zero sign the two endpoint coordinates both equal z_E. For a nonzero sign, z_E is the smaller endpoint coordinate and r_E is their absolute difference.

### 4a. Sign patterns other than all +, all -, or all 0

For such a pattern, any tuple of these exact signs has differences not all equal: there is either a zero alongside a nonzero value or there are both positive and negative values. Thus only the condition sum sigma_E*r_E!=0 remains.

Apply the finite cancellation scheme of Section 3 to the nonzero differences, ordering their selected positions a_E by their actual order in 1,...,n. Lift each residual unit vector to e_{a_E} and each residual edge to e_{a_E}+e_{a_F}. Add all matching periods g_E to the period set of every resulting linear set. Keep the lifted base unchanged.

The cancellation scheme ensures the strict signs and the nonzero sum. All residual edges are noncrossing, and none crosses an adjacent/outer matching edge. Thus every resulting period set is stratified. This finite collection describes exactly this sign-pattern part of F_M.

### 4b. All signs + or all signs -

Here the sum of differences is automatically nonzero. The magnitudes r_E are all positive and must not all be equal. Choose an ordered pair of distinct matching edges I,J and enforce r_I<r_J. This finite union covers precisely the unequal magnitude vectors.

For each ordered pair I,J use the base

b = sum_{E in M} e_{a_E} + e_{a_J}

and periods

- every matching period g_E;
- the comparison period e_{a_I}+e_{a_J};
- the unit period e_{a_J};
- the unit periods e_{a_E} for E other than I,J.

The resulting magnitudes satisfy r_I=1+t, r_J=2+t+u, with t,u>=0, while every other magnitude is independently positive. Conversely every positive pair r_I<r_J has this form. There is only one added two-coordinate comparison period. It cannot cross any adjacent/outer matching edge. All other added periods are singletons. Hence these linear sets are stratified.

### 4c. All signs zero

This contributes nothing because the sum of differences is zero.

Sections 4a-4c give a finite, explicit generator scheme for F_M.

## 5. Finite stratified description of C_{i,F}

Write E=E_i for the antipodal pair and F for the chosen second edge. The pairs E and F are disjoint and noncrossing. Let g_E and g_F be their pair periods. All coordinates outside E union F are arbitrary: add their unit vectors as periods to every linear set below.

Choose sigma in {+1,-1}, the nonzero sign of d_E. Let a be the endpoint of E carrying the excess: odd for sigma=+1 and even for sigma=-1.

There are three cases for d_F.

**Case 1: d_F=0.** Use base e_a and periods g_E,g_F,e_a, together with all outside unit vectors. This gives d_E=sigma*(1+t) and d_F=0.

**Case 2: d_F has sign -sigma.** Let c be the endpoint of F carrying that excess. Use base e_a+e_c and periods g_E,g_F,e_a,e_c, together with outside unit vectors. The two differences are nonzero of opposite signs.

**Case 3: d_F has sign sigma.** Let c be its excess endpoint. Their positive magnitudes must differ. Choose which magnitude is larger; let h be the excess endpoint of the larger one, so h is either a or c. Use base

b=e_a+e_c+e_h

and periods g_E,g_F,e_a+e_c,e_h, together with outside unit vectors. The smaller magnitude is 1+t and the larger is 2+t+u.

These cases are finite and cover exactly d_E!=0 and d_F!=d_E. In Case 3 the sole new comparison edge {a,c} shares an endpoint with E and an endpoint with F, so cannot cross either of them. E and F were noncrossing. No other two-coordinate periods occur. Therefore every displayed linear set is stratified.

## 6. Consequence for a bounded language; hypothesis audit

Combining the finite identity (1) with Sections 3-5 proves that P_{2q} is a finite union of linear sets with stratified period sets.

Use distinct letters c_1,...,c_n and the injective encoding

x |-> c_1^{x_1}...c_n^{x_n}.

The standard Ginsburg-Spanier characterization for **letter-bounded** languages states that the image of a stratified semilinear exponent set under this encoding is context-free (equivalently, its inverse image under exponent extraction is context-free). The distinct-letter hypothesis makes the exponent vector unique; no ambiguity of a general bounded-word presentation is being assumed away. See Ginsburg and Spanier, *Semigroups, Presburger Formulas, and Languages*, Pacific Journal of Mathematics 16(2) (1966), **Theorem 2.1, printed page 291**. Section 2 explicitly defines a 'language' to mean a context-free language and defines tau using distinct letters. Lemma 2.2 proves the constructive sufficiency used here; Lemma 2.1 supplies necessity. This is separate from the paper's Presburger/semilinear equivalence in Section 1. Publisher copy: https://msp.org/pjm/1966/16-2/pjm-v16-n2-p09-p.pdf . An accessible university copy is:

https://www.csa.iisc.ac.in/~deepakd/atc-common/ginsburg-spanier-PJM-1966.pdf

To convert to the desired binary slice, apply a finite-state transducer with states 1,...,n,n+1. In state i it reads c_i and emits a, remaining in i; it may take an epsilon-input transition emitting b and move from i to i+1. State n+1 is the only final state. No other transitions exist. On an ordered word c_1^{x_1}...c_n^{x_n}, its unique accepting output is

a^{x_1}b...a^{x_n}b.

Empty blocks are handled by the epsilon transitions. The input empty word would output b^n, but its exponent tuple is zero and is excluded from P_n, so it is not introduced. Rational transductions preserve CF languages, yielding context-freeness of

{a^{x_1}b...a^{x_n}b : x in P_n} = Q_{a,b} intersect (a^*b)^n.

The equality on the right uses exactly n occurrences of b. Any proper root of a word ending in b also ends in b, so its repeated copies cut at b-delimited block boundaries. Its exponent divides n. The argument covers x_i=0 as well as positive coordinates.

This result is confined to fixed n=2q; taking a union over unbounded q is not a CF-preserving finite union and is not claimed to solve the original problem.

## 7. Direct finite CFG compiler (no external theorem needed for sufficiency)

For completeness, all periods in this construction are unit vectors or sums of two distinct unit vectors. The following recursive compiler produces a CFG for each displayed linear set L(b;G), assuming G is stratified. Thus the use of Ginsburg-Spanier can be replaced by this elementary construction.

Maintain a contiguous interval of distinct terminal letters c_l,...,c_r, a base restricted to that interval, and a set of periods supported within it. Different recursive calls use disjoint nonterminal names. The returned start nonterminal generates exactly the ordered words with the specified base and periods.

1. **Only singleton periods remain.** For each i in the interval introduce A_i with production A_i -> c_i^{b_i}. If e_i is a period, also include A_i -> c_i A_i. Return a start symbol with production S -> A_l A_{l+1} ... A_r. Empty terminal powers denote epsilon.

2. **An outer pair is a period.** If e_l+e_r belongs to G, recursively compile T for the same interval and base with that period removed. Return a fresh S with productions

   S -> c_l S c_r,
   S -> T.

   The recursion adds exactly an arbitrary nonnegative multiple of the removed outer pair and preserves terminal order.

3. **Some pair remains, but there is no outer pair.** If some period joins l to a later coordinate, let k be its largest possible second endpoint. Otherwise put k=l+1. Because the outer pair is absent, l<k<r; the case of an interval of size two would already have been handled in Steps 1 or 2.

   Let G_left be the periods whose supports lie in [l,k], and let G_right=G\G_left. Every period of G_right lies in [k,r]. Indeed, an edge with endpoints i<k<j and l<i would cross the edge {l,k} when that edge exists, while an edge {l,j} with j>k contradicts maximality. If no pair from l exists, k=l+1 and the assertion follows directly.

   Give the left subproblem the original base on [l,k]. Give the right subproblem base zero at coordinate k and the original base on (k,r]. Compile their starts T_left and T_right recursively, and return S -> T_left T_right. The shared letter c_k forms one contiguous run when the two words concatenate; the base and period contributions add exactly.

Each recursive call reduces the number of periods in Step 2 or the interval length in Step 3, so the process terminates. Stratification passes to the subproblems. The three generation equalities just proved establish correctness by induction. The finite union of all resulting grammars is formed with one fresh start symbol having a production to each component start. This gives a fully explicit finite CFG generation scheme for the distinct-letter encoding of P_{2q}; the rational transducer in Section 6 then yields the binary bounded slice.
