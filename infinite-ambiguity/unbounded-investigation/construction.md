# Construction effort and exact obstructions

Status: no CFG or PDA for all primitive binary words has been found. The results below are exact lemmas and checked candidate failures, not a solution. All statements concern nonempty words unless stated otherwise.

## 1. Lyndon representatives: an elementary obstruction

Fix a<b. Let L be the language of words strictly smaller than all their nonidentity cyclic rotations. Consider the regular language

R = a(aa)* b (aa)+ b (aa)+ b.

Then

L intersect R = {a^i b a^j b a^k b : i positive odd; j,k positive even; i>j and i>k}.

Proof of the identity. Rotations beginning in b are larger. Among rotations beginning in a given a-run, its first position gives the longest initial a-run and hence the least rotation from that run. The least of the three relevant rotations begins at the longest run. Parity ensures the first run cannot tie either of the other two. Thus the original word is strictly least exactly when its first run is longer than both later runs.

This language is not context-free. If its pumping length were N>=1, choose

w = a^(2N+1) b a^(2N) b a^(2N) b.

For any factorization w=uvxyz with |vxy|<=N and |vy|>=1, pumping a b changes the number of b's. Otherwise v,y lie within a-runs. Any odd change in any run exits the specified parities. Suppose all nonzero changes are even. The pump window cannot meet both the first and third a-runs, because the whole middle run lies between them. If the first run changes, pumping down shortens it by at least two while leaving the third run length 2N, violating i>k. If the first run does not change, pumping up lengthens a later run by at least two beyond the unchanged first run length 2N+1. Every allowed decomposition fails.

This proves only that this canonical transversal is not context-free. Choosing an arbitrary context-free family of primitive representatives would still suffice through cyclic closure, and that wider possibility is not excluded.

Independent audit: slices_geometry agent checked the identity, all pumping cases, parity, and quantifier order. The underlying non-context-freeness of Lyndon words is already known: Berstel and Boasson, [The language of Lyndon words is not context-free](https://igm.univ-mlv.fr/~berstel/Articles/1997-LyndonBEATCS.pdf). No novelty claim is made for this alternate elementary proof.

## 2. Two unbordered pieces: a sound composition rule

Lemma. If u,v are distinct nonempty unbordered words, then uv is primitive.

Proof. Suppose uv=t^r, r>=2, with d=|t|. Any factor of a d-periodic word of length greater than d has a nonempty border: its prefix and suffix of length |factor|-d coincide. Hence unborderedness gives |u|<=d and |v|<=d. Consequently rd=|uv|<=2d forces r=2 and |u|=|v|=d. The two consecutive d-length pieces of t^2 are equal, contrary to u!=v.

This cannot simply use arbitrary primitive pieces: u=a and v=bab are both primitive and distinct, but uv=abab is a square.

The language U of all unbordered words is itself not context-free. This is Theorem 7 of Rampersad, Shallit and Wang, [Inverse Star, Borders, and Palstars](https://arxiv.org/html/1008.2440), checked in its full primary-source statement and proof. Its pipeline is: intersect U with a four-block regular language -> derive an exact border-avoidance condition -> use an Ogden-marked factorial witness. The theorem's input is an alphabet of size at least two; its output is non-context-freeness of U. Thus a construction that first generates arbitrary U has not reduced the problem to a context-free ingredient. No conclusion about arbitrary representative sublanguages of U follows.

## 3. A complete regular approximation by unique cyclic factors

For w of length n, count occurrences of a factor cyclically by their start positions in Z/nZ. In particular repeated occurrences at different cyclic positions are counted separately.

Lemma. Every primitive word of length n>=2 has a cyclic factor of length floor(n/2) with exactly one occurrence.

Proof. Let p(k) be the number of distinct cyclic length-k factors, with p(0)=1. Prefix deletion gives p(k+1)>=p(k). If p(k+1)=p(k), every cyclic length-k factor has a unique right extension. Reading successive factors of w therefore follows a deterministic directed cycle: all visited states lie on one cycle, since the entire walk is closed, and all p(k) states are visited. Its period is p(k). The emitted word then has cyclic period p(k), which divides n. Primitivity forces p(k)=n. Consequently, whenever p(k)<n, one has p(k+1)>=p(k)+1. Inductively p(k)>=min(k+1,n). For k=floor(n/2), p(k)>n/2. If every factor occurred at least twice, the total n occurrences would be at least 2p(k)>n, impossible.

The bound is sharp for infinitely many n. For s>=0 put

w_s = a^(s+2) b a^s b, with n=2s+4.

This word is primitive: a proper power must have exponent two because it contains two b's, but a square would have equal cyclic a-gaps between the two b's, whereas s+2!=s. For k<=s+1, any length-k cyclic factor contains at most one b. Every b-containing factor occurs twice, once around each b, because both adjacent a-gaps have length at least k-1. The all-a factor occurs max(s+3-k,0)+max(s+1-k,0)>=2 times. At k=s+2, a^(s+2) occurs exactly once. Thus the shortest unique cyclic factor has length exactly n/2.

For fixed K>=1 define Q_K to consist of words having some cyclic factor of length at most K occurring exactly once. Then:

1. Q_K is regular. For each of finitely many patterns of length <=K, finite state records the first and last K-1 letters and counts occurrences up to two; the boundary-crossing occurrences can be evaluated when the input ends. Words shorter than K are a finite exceptional set handled separately.
2. Q_K is a subset of Q. In a proper r-th power, shifts by the root length partition occurrences of every cyclic factor into orbits of size r, so no factor has multiplicity one.
3. Q_K is increasing with K, and its union over K is Q, including the one-letter words.
4. No finite K suffices, by the sharp family above.

This gives an explicit, sound and complete increasing family of regular constructions. Turning variable-K uniqueness into one finite grammar remains missing. The union of an increasing family of regular languages need not be context-free, so this is not a closure argument for Q.

## 4. Mechanism registry

| Mechanism | Exact target | Established result | Missing step / status | Reopening condition |
|---|---|---|---|---|
| Canonical conjugacy representative | Generate all Lyndon words by CFG, then close cyclically | A three-marker parity slice is non-CFL | Refuted for this representative choice; no restriction on arbitrary transversals | A different explicitly context-free transversal with both inclusions |
| Recursive composition | Concatenate certified primitive pieces | Distinct unbordered pieces always work; arbitrary primitive pieces fail on a,bab | All unbordered words are non-CFL; useful proper sublanguages not yet enough | An enumerable CFG family of sound pieces covering a conjugate of every primitive word |
| Unique cyclic motif | Generate a word with one occurrence of a chosen cyclic factor | Q is union of explicit regular Q_K; K=floor(n/2) always enough and sharp | Fixed-K route refuted; variable-K recognition is currently equivalent to Q | A finite stack-checkable uniqueness certificate beyond literal arbitrary-pattern comparison |

## 5. Reproducible finite checks

`construction_checks.py` checks the three-marker Lyndon identity for exponents up to 10; the distinct-unbordered concatenation rule against all nonprimitive binary words through length 14; and the unique cyclic factor bound against all primitive binary words through length 14. These checks supplement, and do not replace, the proofs above.

Independent audit: slices_geometry checked the complete proofs of Sections 2 and 3, including the deterministic factor graph argument, cyclic occurrence counts, and the finite-exception detail needed for Q_K regularity. Both passed.

## 6. No fixed context preserves every primitive word

Lemma. For every x,y in {a,b}* with |xy|>0, there are infinitely many primitive words u for which xuy is a square.

Proof. Set c=yx, choose any integer M>|c|, and set z=b a^M b and u=z c z. Then

xuy = x z y x z y = (x z y)^2.

In the cyclic word u there are exactly two maximal a-runs of length M. They occur inside the two displayed copies of z; every a-run inside c has length less than M, and b's on both sides of each copy prevent merging with c or across the cyclic boundary. If u were an r-th power, r>=2, translation by its root length would partition the two length-M runs into orbits of size r. Thus r=2. A square with exactly two such runs places them at equal half-length separations. Here their start positions have cyclic separations |z|+|c| and |z|. They are unequal because |c|>0. Hence u is primitive. Increasing M gives infinitely many examples. QED.

Corollary. If a grammar has start language Q, then its start symbol S cannot derive x S y for terminal words x,y with |xy|>0. Otherwise substitution of the u above would derive the nonprimitive xuy.

This rules out a genuinely recursive start symbol with a terminal-progress return context, including a reduced strongly connected infinite grammar. It does **not** rule out arbitrary CFGs: a start symbol can be an acyclic dispatcher to several recursive components. It also shows why a direct recursive construction using a globally valid fixed wrapping operation cannot work, while leaving constructions with different restricted nonterminal languages open.

## 7. Weinbaum factorization route: what is and is not available

The checked primary source [Diekert, Harju and Nowotka, Weinbaum Factorizations of Primitive Words](https://users.utu.fi/harju/articles/Weinbaum.pdf), Theorem 1 and its full proof, provides a stronger existence theorem than a single unique factor. Its contract is: given a primitive word w and an occurring letter a, return a conjugate uv with both pieces uniquely positioned cyclically, with u starting and ending in a, and v starting and ending in another letter. Its proof pipeline is maximal gap selection -> marker compression -> induction on shorter words -> lifting the factorization. The maximality condition ensures synchronized replacement of all occurrences of a marker preserves unique positioning.

This route does not yet give a CFG. The proof uses a word-dependent alphabet of compressed markers and the same variable marker at every replaced occurrence. Replacing these global tests with unrestricted local productions has not been justified. The endpoint condition alone is unsound as a primitive certificate: the square aabaab factors as (aabaa)(b), with the required a/a and b/b endpoints. A complete CFG would still need to enforce the cyclic uniqueness or a different sound substitute; simply making the two endpoint-constrained factors independently is insufficient.

No claim is made that marker compression can never be implemented by a PDA. The missing step is an explicit finite grammar implementing a sound, complete synchronized compression certificate. Current evidence is an exact structural theorem and a counterexample to the endpoint-only relaxation.

## 8. Every commutative CFL contained in Q has density O(n^(-1/2))

A language is commutative here if membership depends only on the two letter counts: with each word it contains all permutations of that word. This is an exact restriction on a possible count-based construction, not a restriction satisfied by arbitrary CFGs.

Theorem. If L is a commutative context-free language over {a,b} and L is a subset of Q, then there is a constant C with

|L intersect {a,b}^n| <= C binomial(n, floor(n/2)) = O(2^n/sqrt(n)).

Proof. Every Parikh vector (i,j) of L has gcd(i,j)=1. Otherwise, letting g=gcd(i,j)>1, commutativity would put (a^(i/g)b^(j/g))^g in L. The zero vector is absent because L is contained in Q.

By Parikh's theorem its exponent set is a finite union of linear sets, each with a base vector c and finitely many nonnegative integer period vectors. A component cannot have two rationally independent periods v1,v2. Indeed, choose a prime p not dividing the nonzero determinant det(v1,v2). The columns v1,v2 form an invertible matrix over F_p, so there are nonnegative residues t1,t2<p with c+t1v1+t2v2=0 modulo p. This vector belongs to the component. If it is zero, replace t1 by t1+p, producing a nonzero vector still divisible by p. Either way there is an included nonzero vector with both coordinates divisible by p, a contradiction.

Thus every component has period span of dimension at most one. A rank-one component lies on an affine line whose direction has positive coordinate sum, because its nonzero periods are nonnegative. Its intersection with i+j=n therefore has at most one point. A rank-zero component is a singleton. If there are C components, there are at most C Parikh vectors at every length n. Each class has at most binomial(n,floor(n/2)) words. This proves the inequality, and the standard central-binomial estimate gives the asymptotic bound. QED.

The rate is sharp: L={w: |w|_a=|w|_b+1} is a deterministic one-counter language, is contained in Q by coprime letter counts, and has binomial(n,(n+1)/2) words at every odd length n. In particular a stronger conjecture that every primitive-only CFL has exponential growth rate strictly less than two is false.

This does not establish density zero for arbitrary CFL sublanguages of Q. The missing step would need to control order-sensitive derivations, and the example of the context-free language of nonsquares shows that density alone cannot exclude one fixed power exponent.
