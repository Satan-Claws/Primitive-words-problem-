# Noncommutative regular submonoids retain the primitive-word problem

Status: written proof, pending independent audit. No resolution of the main problem; no novelty claim.

## A primitive-preserving code inside two noncommuting words

Let x,y be nonempty words satisfying xy!=yx. Then, for every sufficiently large integer k, the morphism

h(a)=x^k y,    h(b)=x^(k+1)y

preserves primitivity in both directions, including the convention that the empty word is not primitive.

### Proof

Write x=u^s, where u is primitive, s>=1, and put p=|u| and L=|y|. Since x and y do not commute, y is not a power of u. Indeed, if y were a power of u, it would commute with x. We will use only the condition y not in u*.

Consider any cyclic concatenation

W=u^(e_1)y u^(e_2)y ... u^(e_m)y             (1)

with all e_i sufficiently large. We prove that, for m>=2, W is primitive exactly when its exponent tuple (e_1,...,e_m) has no nonidentity cyclic shift preserving it.

Set A=L+p and choose a fixed threshold E so large that Ep>4A+4p; for example E=4L+8p+1 works. Let each e_i>=E. Write B_i for the designated u^(e_i) block.

Extend B_i to the left and right as far as possible while retaining period p, obtaining a maximal periodic arc R_i of the circular word. Both extension amounts are strictly less than A. To check the right-hand bound, if y followed by one full u agreed with the infinite repetition u^omega, then y would be a prefix u^q v, with v a proper prefix of u. The following u would agree with the cyclic shift of u by |v|. Primitivity of u forces |v|=0, and hence y=u^q, contrary to the assumption. Thus the periodic extension encounters a mismatch within the fixed gap y and the first p letters of the next block, before L+p letters. The left-hand argument is the reversal of the same argument. Since all neighboring blocks are longer than A, the extension lengths are fixed integers a,b independent of i, of m, and of all e_i.

In particular R_i has length e_i p+a+b and start t_i=s_i-a, where s_i is the start of B_i. These starts occur in distinct cyclic order, with successive distances e_i p+L. Also |R_i|<=n-2, where n=|W|: another designated block contributes at least Ep letters to the complement, whereas a+b<2A and Ep>4A+4p.

Suppose a nonidentity rotation fixes W. Let J be the image of R_i. It is a p-periodic arc with length at least Ep. This long arc intersects some B_j in at least p consecutive positions. Otherwise it cannot contain a whole designated block, and can meet at most a suffix of one block, one gap y, and a prefix of the next; both block intersections have length at most p-1, giving |J|<=L+2p-2<Ep, a contradiction.

Lift J and B_j to overlapping intervals at such an intersection. Since they have the same period p and overlap in at least p positions, their union has period p. This union cannot extend beyond R_j: any such extension would contradict the first mismatch defining one of its fixed maximal endpoints. Equivalently, if the union were to wrap around the whole word, a p-periodic arc of length n-1 containing B_j would contradict |R_j|<=n-2. Thus J is contained in R_j. Applying the inverse rotation, its image of R_j is a p-periodic arc containing R_i, hence contained in R_i by the same maximality. Therefore the rotation maps R_i exactly to R_j.

The rotation permutes all the R_i, preserves their cyclic order, and hence sends i to i+ell for one fixed ell modulo m. The shift ell cannot be zero: fixing the start t_i would make the rotation the identity modulo n. Equality of arc lengths implies e_i=e_(i+ell) for every i. Conversely, if the exponent tuple has such a shift symmetry, then (1) is a proper power: rotating by the sum of the first ell block lengths fixes W. This proves the claimed equivalence for m>=2.

For m=1, W=u^e y is primitive once ep>=2p+L. Otherwise write W=t^q, q>=2. Its prefix u^e has periods p and |t|, and ep>=p+|t|. Fine–Wilf gives period gcd(p,|t|). Since that gcd divides p and the prefix contains the primitive u, the gcd equals p. Hence p divides |t|; t is a prefix of u^omega of length divisible by p, so t is a power of u. Then the entire W is a power of u, forcing y in u*, a contradiction.

Choose k with sk>=E. For a binary word w of length m, h(w) has form (1), with e_i=sk or s(k+1) according as its i-th letter is a or b. These distinct exponent values encode its letters exactly. Thus, for m>=2, a nonidentity rotation fixes h(w) exactly when a nonidentity rotation fixes w. The m=1 case was just proved, and m=0 maps to the empty word. Equivalently, h(w) is primitive iff w is primitive. QED.

## Dichotomy for finitely generated submonoids

Let X be a finite set of words over any finite alphabet A, and let R=X*.

- If every pair of nonempty words in X commutes, all such words are powers of one common primitive word rho. Hence R is contained in rho*, and Q_A intersect R is either empty or {rho}.
- Otherwise choose noncommuting x,y in X, and let h be the code above. Its image is contained in R. Therefore

  h^(-1)(Q_A intersect R)=Q_{a,b}.

Consequently, for binary A, the slice Q intersect R is context-free if and only if Q is context-free. One direction is regular intersection, and the other is inverse homomorphism through h.

For general finite A with at least two letters, the same equivalence holds after encoding its finitely many letters into distinct words x^(k+j)y, j=0,...,|A|-1. The identical maximal-arc proof shows this finite-alphabet morphism preserves primitivity, so it reduces Q_A to the binary problem and conversely. One can alternatively restrict the stated dichotomy's CFL equivalence to binary A, where no alphabet-change argument is needed.

The commutative branch uses the elementary commuting-word fact: two commuting nonempty words are powers of the same primitive word. Apply it to any fixed nonempty member of X; uniqueness of its primitive root puts every other member in the same rho*.

## What this does and does not obstruct

Regular restrictions consisting of arbitrary concatenations of two noncommuting fixed blocks do not make the context-freeness problem easier. This includes many unbounded-run slices. However, arbitrary regular languages can have fixed prefixes or suffixes that themselves certify primitivity; they need not contain a hard submonoid. No dichotomy for arbitrary regular R is claimed.

## Necessity of allowing k to depend on x,y

The embedding fails for some small k. For any k>=1 take x=a and y=ba^k b. Then x and y do not commute, but h(a)=a^k ba^k b=(a^k b)^2 is nonprimitive. Thus no universal k independent of the two loop words can work for this particular code formula.

A finite check over all noncommuting binary x,y of lengths at most 3 and all nonempty binary inputs of length at most 7 found a failure at k=1: x=a,y=bab,input a,output abab. For k=2,...,6 it found none, with 43180 inputs checked for each k. This is evidence only; the proof above uses its explicit sufficient threshold.
