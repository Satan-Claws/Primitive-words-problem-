# Closure and sparse-language search, 17 November 2026

These are proved partial results and strategy obstructions, not a resolution of the primitive-word problem.

## 1. Reduction of fixed tuple length to its squarefree part

For m>=2 let P_m be the set of nonnegative integer m-tuples with no proper divisor period. Its distinct-letter encoding is

    L_m = {A_0^x_0 ... A_(m-1)^x_(m-1) : x in P_m}.

**Theorem.** Put s=rad(m), g=m/s, and r=omega(m). Then L_m is context-free if and only if L_s is context-free.

This is a statement about fixed m, with no uniform grammar in m.

**Forward construction from L_s.** Group the m entries into s consecutive g-dimensional blocks, X_j=(x_(gj),...,x_(gj+g-1)). For every prime p dividing m, the shift m/p equals g(s/p). Thus x has period m/p exactly when X_j=X_(j+s/p) for all cyclic j. A tuple is imprimitive exactly when it has one such prime-index period.

For each integer t in {0,...,r(g-1)}, define

    y_j(t) = sum_(h=0)^(g-1) t^h x_(gj+h),

using 0^0=1. If x is imprimitive, every y(t) has its corresponding period. Conversely suppose x is primitive. For each p, some j has X_j!=X_(j+s/p), so

    f_(p,j)(T) = sum_h T^h (x_(gj+h)-x_(g(j+s/p)+h))

is a nonzero polynomial of degree at most g-1. If y(t) has period s/p, then f_(p,j)(t)=0. A nonzero real polynomial of degree at most g-1 has at most g-1 distinct roots. At most r(g-1) parameters therefore produce an imprimitive y(t). Among the r(g-1)+1 displayed integers there is a good parameter. We have proved the exact equivalence

    x in P_m iff exists t in {0,...,r(g-1)} with y(t) in P_s.

Let C_0,...,C_(s-1) be the distinct letters of L_s. For each parameter define the morphism

    h_t(A_(gj+h)) = C_j^(t^h).

On the regular domain A_0*...A_(m-1)*, its output has exactly the exponent tuple y(t). Hence

    L_m = union_t [h_t^(-1)(L_s) intersect A_0*...A_(m-1)*].

Inverse morphism, regular intersection and finite union all preserve context-freeness. The construction permits erasing letters when t=0.

**Reverse implication.** Define k(C_j)=A_(gj). The image of a word in C_0*...C_(s-1)* has an m-tuple whose coordinate gj is the original j-th coordinate and whose other coordinates are zero. Since every candidate prime period m/p is a multiple of g, this tuple has period m/p exactly when the original tuple has period s/p. Therefore

    L_s = k^(-1)(L_m) intersect C_0*...C_(s-1)*.

This proves the converse using the same valid closure properties.

**Consequence.** The constructions already proved in `primitive_15_scalar_cover.md` and `finite_stratified_run_slices.md` for squarefree lengths with at most two prime factors extend to every fixed m with omega(m)<=2, including arbitrary prime powers in m. By `weighted_projection_lift.md`, both Q intersect (a*b)^m and Q intersect (a+b+)^m are context-free for all these m. Here a* and a+ in those expressions denote Kleene star and positive closure, respectively; the syntax is fixed-m concatenation.

**Remaining gap in this mechanism.** A construction for all squarefree s with at least three prime divisors is not supplied. Even such a construction for every fixed s would not supply one finite grammar for unbounded tuple lengths.

## 2. Every single-loop regular restriction has a regular primitive part

**Lemma.** Let A,B be fixed words, B nonempty. If n|B|>=|A|+2|B| and AB^n is a proper power, then AB=BA.

**Proof.** Write AB^n=T^k with k>=2 and d=|T|. Put a=|A| and b=|B|. Then d<=(a+nb)/2, and the assumed bound gives nb>=d+b. The suffix B^n has periods b and d. The Fine-Wilf theorem says that a word with periods b,d and length at least b+d-gcd(b,d) has period e=gcd(b,d). Its hypotheses hold here. Since e divides b, the word B is V^(b/e), where V is its prefix of length e.

Rotate AB^n to B^n A. A rotation of a k-th power is again a k-th power with root length d. Its first d letters lie inside B^n, since nb>=d. Those d letters equal V^(d/e), since e divides d. Consequently B^n A is a power of V. Its suffix A is also a power of V: both the entire length kd and the prefix length nb are multiples of e, so the suffix begins and ends at V boundaries. Therefore A and B commute.

**Corollary.** For fixed x,y,z, the language Q intersect xy*z is regular.

If y is empty, the restriction is a singleton. Otherwise rotating xy^n z gives zx y^n and preserves primitivity. Apply the lemma with A=zx and B=y. If A and B do not commute, all sufficiently large n give primitive words; the finitely many smaller cases can be individually included or excluded, producing a regular language. If A and B commute, the commuting-word theorem gives a common primitive root V with A=V^u, B=V^v, u>=0 and v>=1. Then A B^n is primitive exactly when u+nv=1. There is at most one such n, so the restricted primitive language is finite. Empty output remains excluded in all cases.

The same conclusion holds for a finite union of single-loop restrictions by finite union. Thus no reduction using only those sparse regular sets can yield a non-context-free slice. No assertion that arbitrary polynomial-growth regular restrictions are single-loop is made.

## 3. Full and erased Parikh images do not obstruct context-freeness

Over an alphabet with k>=2 letters, the Parikh image of Q consists exactly of (i) the k unit vectors and (ii) all nonnegative vectors with at least two positive coordinates.

For (ii), order the letters with positive coordinates and concatenate their nonempty unary blocks. This word is primitive: its first letter occurs in just its first block, and a proper power would have to have another occurrence of that letter after some different letter. Necessity is immediate because a unary word is primitive exactly at length one. This set is a finite union of linear sets and therefore semilinear.

If one or more coordinates are erased and at least one letter is retained, the projection is all of N^d: for any requested retained counts, append exactly one occurrence of an erased letter. The resulting word is primitive because a letter count equal to one precludes a proper power. This includes the all-zero projected tuple.

More generally, for a fresh marker # and the erasing morphism pi(#)=epsilon fixing the original alphabet, pi(Q_(Sigma union {#}))=Sigma*. The witness #w has a unique # and is primitive for every w. A transduction that merely erases an unconstrained marker therefore destroys the sought obstruction.

**Precise blocked gap.** These arguments do not show that Parikh(tau(Q)) is semilinear for every rational transduction tau. A successful Parikh route still needs one explicit rational transduction whose image has a proved nonsemilinear Parikh image. Restricting the input by arbitrary equality conditions is not a valid substitute for a finite-state transduction.

## 4. Audit of the supplied background syntax

The literal regular expression `ababa*b` does not describe three arbitrary a-runs. Its words are a b a b a^k b. For example `bbb` belongs to {(a^n b)^3:n>=0} but does not belong to that literal regular expression. The intended three-separator expression appears to be `(a*b)^3`.

For the intended expression, a proper power has exponent dividing the total number three of b's, hence exponent three, and the three a-run lengths must coincide. Thus the imprimitive slice is indeed {(a^n b)^3:n>=0}; the primitive slice is its unequal-triple counterpart. This correction does not imply anything about context-freeness of Q.

The alphabet-dependence warning is a prohibition on assuming a transfer, not an obstacle after proving it: `closure_notes.md` supplies the explicit primitivity-preserving/reflection morphism c_i -> a b^i. Binary context-freeness is therefore equivalent to context-freeness for every fixed finite alphabet with at least two letters.

## 5. Two adjacent fixed-word loops also have a regular primitive part

**Theorem.** For any fixed words u,v, the language Q intersect u*v* is regular, even when u and v each contain several letters and the restriction has unboundedly many letter runs.

If either fixed word is empty, this is a single-loop case. If u,v commute, they are powers of a common primitive root, and the restriction contains at most that one primitive root. Suppose they do not commute. The Lyndon-Schützenberger equation theorem states that x^i y^j=z^k for nonempty words x,y,z and integers i,j,k>=2 implies that x,y,z commute. Therefore every word u^i v^j with i,j>=2 is primitive. The remaining possibilities have i=0, i=1, j=0 or j=1, each a single-loop restriction covered in Section 2. Hence the complete primitive slice is the finite union of the regular language u^2u*v^2v* and four regular primitive single-loop slices. Possible overlap among these components is harmless.

The exact equation theorem hypotheses were checked against the Archive of Formal Proofs formalization, `Lyndon_Schutzenberger`, at https://isa-afp.org/browser_info/current/AFP/Combinatorics_Words/Lyndon_Schutzenberger.html . Only this ordinary background theorem was searched, not a solution or status of the primitive-language problem.

**Limit.** The proof does not apply to x u* y v* z with arbitrary fixed intervening words, nor to three noncommuting loops. It rules out a concrete family of sparse regular sets beyond bounded letter-run slices.

## 6. Finite sanity checks

A direct binary-word check used all A with length at most 4, all nonempty B with length at most 4, and 0<=n<=8. All 5,250 triples satisfying the lemma's length bound obeyed its implication. A seeded check tested 100 random tuples over {0,...,4} at each length m=2,...,60, giving 5,900 exact checks of the squarefree scalar-projection identity and no counterexample. These checks supplement the preceding proofs; they are not used to infer an unbounded statement.

## 7. Route registry and exact gaps

- **Fixed-dimensional closure reduction:** proved L_m CF iff L_rad(m) CF. Blocked for squarefree lengths with at least three primes; all fixed lengths would still require a separate uniform construction to resolve Q.
- **Sparse regular single-loop slices:** proved primitive restriction regular, with explicit finite exceptional prefix. This mechanism cannot give a non-CF slice.
- **Sparse regular adjacent two-loop slices:** proved primitive restriction regular. Arbitrary intervening constants and three or more loops are not covered by this proof.
- **Parikh image without regular control:** exact semilinear description; any proper coordinate projection is saturated. No obstruction remains here.
- **Marker-erasing transduction:** saturated image via the unique-marker certificate. Must add nontrivial regular control that prevents these primitive witnesses; no successful controlled image supplied.
- **General rational-transduction negative route:** still requires an explicit rational relation tau and a proof that tau(Q) is non-CF, or has a nonsemilinear Parikh image. Restating the existence of such tau is not progress toward that missing lemma.
- **Sparse counting:** proved that two concrete infinite regular families have regular primitive subsets; no regular restriction with a provably nonrational or obstructive count sequence has been found. An arbitrary context-free language may be infinitely ambiguous, so merely obtaining a transcendental ordinary word count would not suffice without a separately proved ambiguity or bounded-language consequence.
