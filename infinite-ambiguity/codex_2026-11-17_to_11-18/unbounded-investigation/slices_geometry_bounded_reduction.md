# General bounded slices reduce to fixed block slices

Status: written proof, pending independent audit. This is a conditional barrier and does not settle the primitive-word problem or the Kászonyi–Katsura problem. No novelty claim.

Let Q_A denote primitive words over a finite alphabet A. Put

K_m = Q_{a,b} intersect (ab*)^m, m>=1.

## Theorem

If K_m is context-free for every fixed m, then Q_A intersect R is context-free for every bounded regular language R over every finite alphabet A.

The converse follows by choosing R=(ab*)^m. Thus the two statements are equivalent.

Here bounded means that R is contained in u1*...uk* for some fixed words u1,...,uk. It is enough to prove the theorem for the containing product and then intersect with R. In fact the proof also treats expressions

B = x0 y1^{E1} x1 ... yr^{Er} xr,

where all x_i,y_i are fixed and each E_i is an ultimately periodic subset of N.

### Elementary one-block equality lemma

For primitive nonempty y,z and fixed words alpha,beta,gamma,delta, equality

alpha y^e beta = gamma z^f delta

has, for sufficiently large e,f, either no solutions or exactly all solutions of e-f=c for a fixed integer c.

Proof. The long periodic interiors overlap in arbitrarily large length. Once their overlap has length at least |y|+|z|, Fine–Wilf implies their common overlap has period gcd(|y|,|z|). As it contains a conjugate of each primitive word, |y|=|z|=p. The length equality fixes e-f=c. Inserting or deleting p letters inside the overlap simultaneously increments or decrements both exponents and preserves equality. Thus one sufficiently large solution yields every sufficiently large solution on that line. QED.

For finitely many families U_i(e)=alpha_i y_i^e beta_i, increase a common threshold so that this description holds for every pair. Define i~j when equality is possible above threshold. This is an equivalence relation: reflexivity and symmetry are immediate, and composing two offset equations at sufficiently large exponents proves transitivity. Their offsets satisfy the cocycle identity. Consequently there are integers s_i and finite labels t_i such that, for all sufficiently large exponents,

U_i(e)=U_j(f) iff t_i=t_j and e+s_i=f+s_j.       (1)

### Canonical cut lemma for a rigid bounded expression

Suppose the primitive words y_i are nonempty, regard the displayed expression y1^{e1}x1...yr^{er}xr cyclically, and suppose no adjacent long periodic blocks merge across their gap. Then, for all e_i above a fixed threshold, there are fixed words alpha_i,beta_i and a fixed c>=0 such that the word is a conjugate of

U_1(e_1)...U_r(e_r),  U_i(e)=alpha_i y_i^{e-c} beta_i,

and it is nonprimitive iff the tuple (U_1(e_1),...,U_r(e_r)) is invariant under a nonidentity cyclic shift of its r coordinates.

Here “merge” has the precise meaning that x_i y_(i+1)^c is a prefix of y_i^omega, for c=1+max_j |y_j|. In that case y_i=ps, x_i=y_i^q p and y_(i+1)=sp, and

y_i^e x_i y_(i+1)^f = y_i^{e+f+q}p.           (2)

A full proof of this canonical cut lemma is present in context-free/reports/closure.md, Lemma I, steps (d)–(f). The relevant argument is also supplied below, so this theorem does not depend merely on that report's claimed conclusion.

For each long periodic block B_i=y_i^{e_i}, extend it maximally in both directions while preserving period p_i=|y_i|. Because neither neighboring seam merges, each extension length a_i to the left and b_i to the right is bounded by a constant independent of all sufficiently large exponents. In fact a_i,b_i are then fixed: inspect only the neighboring fixed gap and c copies of the neighboring primitive word. Let R_i be this maximal periodic arc and t_i its start. Choosing the common threshold large makes every R_i shorter than the whole circular word by at least two letters, makes its starts distinct and in the original cyclic order, and makes each B_i longer than every fixed extension bound.

Any nonidentity rotation fixing the word sends R_i to another R_j. To see this, its image J is a long periodic arc with primitive period p_i. A sufficiently long subarc of J lies inside some B_j: otherwise J could meet at most the end of one B_j, a fixed gap, and the beginning of the next, and one of those intersections has length at least twice the maximum period length. Fine–Wilf on that intersection gives p_i=p_j. The union of J and B_j is periodic with this same period, since their overlap has at least a full period. It cannot wrap all the way around the word, because a periodic arc of length n-1 containing B_j would contradict the bounded maximal extension defining R_j. Hence J is contained in R_j. Applying the inverse rotation yields the reverse inclusion, so J=R_j. The rotation preserves the cyclic order of the distinct starts t_i, hence permutes these starts by one fixed nonzero index shift.

Cutting at the starts t_i gives the stated U_i. Their prefix and suffix pieces are fixed, because the extension amounts a_i are fixed; thus U_i(e)=alpha_i y_i^{e-c}beta_i after choosing c sufficiently large to absorb the fixed ends. A rotation symmetry of the original word therefore induces equality of these blocks under a nonzero index shift. Conversely such an equality of the block tuple gives a nonidentity rotation symmetry of their concatenation. A nonempty word is a proper power exactly when it has a nonidentity rotation symmetry, proving the lemma.

For r=1 with no merging seam, all sufficiently large words are primitive: if y^e x were a proper power, its root length would be at most half the word length, and Fine–Wilf on the long y-block would force the whole word to be a power of y, contrary to the nonmerging seam.

### Encoding the rigid case as K_r

Apply (1) to the canonical blocks, absorbing the fixed c into the offsets. Choose an integer M larger than the number of equivalence classes and use distinct labels t_i in {0,...,M-1}. Define

z_i=M(e_i+s_i)+t_i.

Increase the exponent threshold so that z_i>=0 and the one-block equality equivalences hold. Then

U_i(e_i)=U_j(e_j) iff z_i=z_j.

The canonical cut lemma now says that the original word is primitive iff (z_1,...,z_r) is a primitive tuple, iff

ab^{z_1} ... ab^{z_r} belongs to K_r.          (3)

For each coordinate, its allowed z_i form an ultimately periodic set: e_i is restricted to E_i above threshold and the encoding is affine. Thus the entire allowed input set in (3) is regular. Intersect K_r with this set.

There is a finite-state transducer mapping each such input to U_1(e_1)...U_r(e_r): its state records the block index, skips a fixed initial number of b's, and emits one y_i for each further group of M b's, with fixed alpha_i and beta_i at block boundaries. More explicitly, choose a starting exponent T for each coordinate; after z_i(T) initial b's it emits the fixed word alpha_i y_i^{T-c}, and each further M b's produces one y_i, followed by beta_i. Regular restrictions on the exponents were already imposed on the input. Rational transductions preserve context-freeness, so the resulting primitive-word language is CFL if K_r is CFL.

Taking cyclic shifts and intersecting with the original regular expression B recovers the desired rigid primitive slice. Every word produced is primitive, so this intersection cannot create false positives; every primitive member of B has its canonical conjugate in the constructed language, so completeness holds. CFLs are closed under cyclic shift and regular intersection.

### Reduction to the rigid case

Induct on the number r of variable blocks, maintaining ultimately periodic exponent restrictions.

Empty y_i are removed. If y_i=z_i^k with z_i primitive, replace its exponent set E_i by kE_i, which is ultimately periodic. Move the fixed prefix x0 to the end by conjugacy, and recover words using cyclic shifts followed by intersection with B as above.

A merging seam admits identity (2). The merged exponent set is E_i+E_(i+1)+q, which is ultimately periodic, since it is the length set of a concatenation of unary regular languages. This reduces the number of blocks. If the seam crosses the displayed boundary, rotate the cyclic expression first; cyclic shifts and intersection recover exactly the primitive members of the old B.

If r=1 and the seam merges with itself, the expression is a power of one fixed primitive word; its primitive part is finite. Otherwise partition into the cases where some exponent is below the threshold (finitely many fixed values, reducing r) and the remaining rigid case (handled above). The r=0 case is finite. This completes the induction and theorem. QED.

## Scope and unresolved point

This theorem reduces arbitrary bounded regular slices to the standard fixed-marker slices. It does not assert that all K_m are CFL. If that claim is not established for every m, a bounded-slice attack remains possible precisely through the unresolved fixed-block problem. It also says nothing about regular slices with unbounded independent block structure.

## Audit checklist still needed

- Check the canonical maximal-periodic-arc argument, including arcs meeting the displayed boundary.
- Check that “cyclic shifts followed by intersection with B” never claims closure under intersection with a nonregular language: B is a regular expression with unary regular exponent constraints.
- Check that merged unary exponent sums remain regular and impose no hidden correlation with surviving blocks.
- Check the offset equivalence classes and the direction of the rational-transduction closure.

## Elementary grammar proof of cyclic-shift closure

For completeness, the closure under cyclic shift used above needs no stronger theorem about Q. Convert a CFL grammar to binary form (with the usual harmless separate treatment of the empty word). Retain its original nonterminals. For each original nonterminal A, create H_A, intended to generate all strings vu such that S derives uAv with terminal u,v. Add H_S -> epsilon. For each production A -> BC add

H_B -> C H_A,    H_C -> H_A B.

A derivation of H_A follows an ancestor path from A back to S, generating the siblings on the appropriate sides. Induction on that path proves its intended context language exactly. Introduce a new start Z with Z -> S and, for every production A -> BC,

Z -> C H_A B.

Every output of the latter form is a rotation of uBCv derived from S. Conversely, every nontrivial cut between two adjacent terminal leaves in a derivation tree lies between the two children B,C of their lowest common ancestor; the rotated yield has precisely the form C(vu)B. Thus this grammar generates Cyc(L). The construction applies regardless of ambiguity.
