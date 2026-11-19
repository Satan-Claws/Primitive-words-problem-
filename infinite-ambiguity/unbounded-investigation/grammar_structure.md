# Grammar structure investigation

Status: partial results and explicit barriers; no resolution of the context-freeness of Q.

## 1. A primitive-only CFG with full entropy and arbitrary branching

Let the height of a word be its number of a's minus its number of b's. Let D be the language of nonempty Dyck words: words of height zero whose prefixes have nonnegative height. Let P be the language of prime Dyck excursions: nonempty height-zero words whose nonempty proper prefixes have strictly positive height.

The following cycle-free grammar generates P:

```
S -> ab | a D b
D -> DD | a D b | ab
```

There are no empty productions or unit productions. Every parse tree of a fixed word is finite, and only finitely many such trees exist: every internal expansion either adds two terminals or splits into two nonempty yields.

**Lemma 1.** L(D)=D and L(S)=P.

Proof. Each production preserves the Dyck property. Conversely, a nonempty Dyck word either has a proper return to height zero, in which case it is a concatenation of two shorter nonempty Dyck words, or is an excursion. An excursion is either ab or a v b with v a nonempty Dyck word. Induction on length proves both assertions.

**Lemma 2.** P is a subset of Q.

Proof. Suppose w in P equals u^k for k>=2. Heights add, so 0=height(w)=k height(u), and height(u)=0. But u is a nonempty proper prefix of w, contrary to the strict positivity condition.

**Lemma 3.** For n>=1, P has C_(n-1) words of length 2n, where C_j=(1/(j+1)) binom(2j,j). Consequently its exponential growth rate is 2, while its density among words of length 2n tends to zero at order n^(-3/2).

Proof. Removing the first a and last b is a bijection from P at length 2n to Dyck words at length 2n-2. The reflection argument gives C_j: among binom(2j,j) balanced paths, reflection through the first visit to height -1 bijects the paths that cross below zero with paths having j+1 down-steps and j-1 up-steps, counted by binom(2j,j-1). Their difference is C_j. The elementary central binomial asymptotic gives C_j asymptotic to 4^j/(sqrt(pi) j^(3/2)).

**Lemma 4.** The word w_m=a(ab)^m b has at least C_(m-1) parse trees for m>=1.

Proof. For the D yield (ab)^m, choose an arbitrary ordered full binary tree with m leaves, put D->DD at each internal node and D->ab at each leaf. There are C_(m-1) such trees. These are distinct parse trees of the same yield. Wrapping them by S->aDb preserves distinctness. (Indeed these are all D parses of this yield, but the lower bound suffices.)

The nonterminal D is expansive: D=>DD. Parse trees have unbounded nesting depth and unbounded branching, and ambiguity grows exponentially on w_m. Also |w_m|_a=|w_m|_b=m+1, so the gcd of its letter counts can have arbitrarily many different prime factors, by choosing m+1 to be a primorial.

Thus none of the following proposed implications is valid:

* full entropy plus unbounded/exponential ambiguity implies a proper power;
* expansive recursion or unlimited branching in a useful nonterminal implies a proper power;
* primitive-only context-free languages must have bounded gcd of letter counts, or bounded number of distinct prime factors in that gcd.

These counterexamples do not supply a grammar for all Q. They identify exactly why a proposed argument must exploit completeness, positive density, or stronger uniformity conditions.

### Cyclic closure strengthens the count-wise barrier

Put C=Cyc(P), the set of all cyclic rotations of excursions. Context-free languages are closed under cyclic rotation; an elementary grammar proof is recorded in `slices_geometry_bounded_reduction.md`. Hence C is context-free and C is a subset of Q.

**Lemma 4a.** For n>=1,

    |C intersect {a,b}^{2n}| = 2n C_(n-1),
    |C intersect {a,b}^{2n}| / binom(2n,n) = n/(2n-1).

In particular C contains asymptotically one half of all balanced words, including along n with arbitrarily many distinct prime factors. Its unconditional length density is asymptotic to 1/(2 sqrt(pi n)).

Proof. Every excursion is primitive, so its 2n rotations are distinct. No two different excursions are conjugate: the initial position of an excursion is the unique location of the minimum of the cyclic prefix-height path. A different rotation starts at a positive height and reaches the old zero height before completing its circuit, so it has a negative proper prefix and cannot be an excursion. The conjugacy classes of different members of P are therefore disjoint, giving the first formula. Since C_(n-1)=binom(2n-2,n-1)/n, cancellation gives the second formula. The density asymptotic follows from the central binomial estimate.

Thus even the following stronger claim is false: every CFL contained in Q must occupy a vanishing fraction of each letter-count layer as the gcd of the counts, or its number of prime factors, goes to infinity. The balanced layer supports a fixed positive fraction here. This does not contradict a possible zero-density theorem for primitive-only CFLs under uniform independent letters: that unrestricted density still tends to zero.

## 2. A balanced regular slice retaining the entire problem

Define h(a)=ab and h(b)=aabb, and R=(ab|aabb)*. Both codewords are prime Dyck excursions. Every word in R has a unique decomposition into these excursions: the boundaries are exactly the visits to height zero.

**Lemma 5.** For every w in {a,b}*, h(w) is primitive if and only if w is primitive. The empty word is nonprimitive on both sides.

Proof. If w=v^k for k>=2, h(w)=h(v)^k, so the forward implication follows by contraposition. Conversely let h(w)=u^k, k>=2. The total height is zero, so height(u)=0. The end of each copy of u is a return to height zero and hence an excursion boundary. Therefore u is a concatenation of whole codewords ab and aabb. The unique excursion decomposition gives u=h(v) for a nonempty v, and injectivity of this code gives w=v^k.

In particular Q intersect R=h(Q). This yields the exact equivalence

    Q is context-free iff Q intersect R is context-free.

The forward direction uses intersection with the regular language R. The reverse direction uses inverse homomorphism by h, since h^{-1}(Q intersect R)=Q. Both closure directions are valid.

This is a reduction, not a resolution: a boundedness assumption on letter imbalance, or restricting all words to equal numbers of a's and b's, does not simplify the problem. R is not block-bounded: it has arbitrarily many codewords in arbitrary order. Also one must not replace the regular R by the entire Dyck language and assert closure under that intersection.

## 3. Current route registry

| Mechanism | Exact proposed goal | Established result | Obstacle / falsifier | Reopening condition |
|---|---|---|---|---|
| Recursive branching | Force a power from an expansive useful nonterminal plus many accepted words | Lemmas 1-4 | The displayed primitive-only grammar is expansive, full entropy, and exponentially ambiguous | A condition using completeness or actual positive density, rather than entropy |
| Arithmetic complexity of trees | Bound prime divisors of letter-count gcd in primitive-only CFGs | No such bound exists | w_m from Lemma 4 has gcd m+1, arbitrary | A word-order invariant not determined by counts |
| Balanced restriction | Prove non-context-freeness after restricting to balanced words | Exact primitive-preserving code, Lemma 5 | Balanced regular code R already retains the entire original problem | A genuinely smaller slice with a new structural theorem |
| Ordinary and simultaneous interchange | Extract incompatible independent substitutions at one fixed length | Existing repository has small rectangle and multicut covers | The previously proved covers already satisfy these necessary conditions | Uniform interaction of the same nonterminal across different lengths |
| Prime layers | Prove any CFG accepting every nonunary word at every sufficiently large prime length contains a power | No proof | Parikh projection alone loses order; a+b+ already realizes every positive count vector while staying primitive | A uniform parse-tree theorem exploiting all permutations at prime lengths |

All proofs in this file are written mathematical arguments, not Lean formalizations. No novelty claim is made.

## 4. Prime layers: a complete obstruction for commutative CFLs

A language is commutative if membership depends only on its letter counts.

**Lemma 6.** If a commutative context-free language L is contained in Q, then there is a constant C such that, at every length n, L has at most C different letter-count vectors. Consequently |L intersect {a,b}^n|=O(2^n/sqrt(n)). This rate is sharp.

Proof. By Parikh's theorem, the count vectors form a finite union of linear sets c+N p_1+...+N p_r. Every nonzero vector (i,j) in this image has gcd(i,j)=1: if d=gcd(i,j)>=2, commutativity would put (a^(i/d)b^(j/d))^d into L. This includes the evident unary cases.

No component can contain two linearly independent periods p,q. Otherwise choose a prime ell not dividing the nonzero integer det(p,q). Over the field with ell elements, the matrix with columns p,q is invertible. Hence there are residues lambda,mu with c+lambda p+mu q=(0,0) modulo ell. Choose nonnegative representatives and, if necessary, add positive multiples of ell to both coefficients. The resulting vector is nonzero, belongs to the linear component, and has both coordinates divisible by ell, a contradiction.

Thus all nonzero periods in a component are collinear. Their coordinate sums are positive, so a fixed length line i+j=n meets the affine line of that component in at most one point. A zero-period component is just a singleton and has the same property. The number C of components therefore bounds the number of count vectors at each length. Each count vector has at most binom(n,floor(n/2)) realizations, giving the density bound. Sharpness follows from the commutative context-free language with #b=#a+1: the two counts are coprime, so all its words are primitive, and at odd lengths its size is asymptotic to a positive constant times 2^n/sqrt(n).

**Corollary 6a.** No commutative CFL contained in Q contains every nonunary word at every sufficiently large prime length. Such a prime layer has p-1 different positive count vectors, contradicting Lemma 6.

This does not settle the prime-layer target for arbitrary CFGs. In that setting, one accepted count vector does not imply that a power with those counts is accepted. The excursion language in Section 1 illustrates that word order remains essential even on count vectors with very large gcd.

## 5. A uniform context-injectivity condition for subexponential ambiguity

For an epsilon-free CNF grammar, a return context at A is a finite derivation tree with root A, one unexpanded leaf marked A, and every other leaf terminal. Its yield is a terminal pair (u,v): inserting a tree of yield z at the hole gives uzv. Context composition replaces the hole of the first context by the second.

**Lemma 7.** Suppose A is useful and two distinct return contexts kappa_0,kappa_1 at A have the same terminal pair (u,v), with t=|u|+|v|>0. Then for some fixed n_0, the grammar has at least 2^N parse trees of one word of length n_0+Nt, for every N>=1.

Proof. Fix a complete A-tree T and an outer start-tree context containing A. Insert any of the 2^N sequences of the two contexts between the outer context and T. Every resulting word is x u^N z v^N y, with x,y,z fixed.

It remains to check that the trees are distinct, rather than merely the choices. In CNF each complete terminal derivation leaf has its usual terminal-production parent; equivalently suppress these unary terminal-production edges when counting the binary skeleton. A context with t terminal leaves and one hole then has t binary nodes and t+1 leaves. Its number of nodes other than the hole is 2t, independent of its shape. The distinguished-hole path describes a context as a sequence of frames; each frame consists of one binary node, a choice of child containing the hole, and the complete sibling tree. Frame node counts are positive and add under composition. Along this path, the boundaries between composed contexts can therefore be recovered uniquely whenever cumulative added-node count reaches 2t,4t,...,2Nt. Thus distinct choice sequences give distinct contexts.

After inserting T, its root span is fixed by the yields: it starts after x u^N and has length |z|. An epsilon-free CNF tree has at most one nonterminal node with that span, because proper descendants have strictly shorter positive yields, while incomparable nodes have disjoint spans. Hence equality of the completed trees would recover the same inserted T node, the same surrounding composite context, and the same choice sequence. There are therefore 2^N distinct complete parse trees, as claimed.

**Corollary 7a.** If maximum word ambiguity grows subexponentially with word length, then at every useful nonterminal A the map from nontrivial return tree contexts to terminal pairs (u,v) is injective.

This is a condition on arbitrary useful contexts, not only on those in a bounded regular slice. The bounded-slice first-return argument is obtained by composing two different first-return contexts in opposite orders: their left unary yields commute, as do their right unary yields, while the first-return decomposition distinguishes the two context trees.

The condition does not by itself exclude polynomial ambiguity or resolve Q. In particular each fixed NE_M slice from the finite-ambiguity proof already has a finite-ambiguous grammar; dependence of the same original grammar across growing M remains the missing ingredient.

### Published status of the context criterion

After the preceding argument was developed, the exact general phenomenon was checked in K. Wich, [Exponential ambiguity of context-free grammars](https://static.aminer.org/pdf/PDF/000/158/522/exponential_ambiguity_of_context_free_grammars.pdf), Definition 2.7 and Theorems 3.18, 4.3, 4.4. Wich permits nonterminal symbols in the context frontier, with explicit usefulness and non-erasing hypotheses. Ambiguous pumping contexts give exponential word ambiguity; absence gives a polynomial bound. Thus for cycle-free grammars there is no intermediate superpolynomial/subexponential ambiguity growth. Our terminal-context CNF lemma is an independently written special case, not a novelty claim. Wich's ambiguity function maximizes over words of length at most n.

## 6. Uniform bounds in bounded slices of a polynomially ambiguous grammar

Let G be a reduced epsilon-free CNF grammar with g nonterminals and polynomially bounded ambiguity. Intersect with (ab*)^m using its standard deterministic block counter. Every resulting tree has m leaves labelled a.

The structural proof in `finitely-ambiguous/PROOF.md`, Section 3(a)-(d), remains valid up to, but excluding, linear independence of the skeleton periods. Its contradictions in those parts construct exponentially many trees on linearly growing word lengths, so polynomial ambiguity is sufficient. Consequently recurrent annotated SCCs are rings with unique first-return contexts and fixed unary side trees. One may remove all complete ring turns to obtain finitely many skeletons; their period lists may be dependent.

**Lemma 8 (uniform bounds).** There is a constant C_G, independent of m, such that these skeletons can be chosen with base-word length and number of period occurrences at most C_G m. Every period has support of size at most two and every coordinate is at most B_G=g 2^g. The supports remain noncrossing, as in the original structure lemma.

Proof. On a recurrent annotated SCC, both block endpoints remain fixed. Hence there are at most g states in its ring, even though the entire product grammar is much larger. Each side subtree has exactly one complete tree over all its unary yields. A repeated original unary nonterminal in that tree would give a pumpable cycle and another tree, contrary to this uniqueness. It therefore has at most 2^g terminal leaves. A ring turn has at most g such side subtrees, proving the period bound.

For the base-word bound, retain from a skeleton only the root, the m a-leaves, and their connecting paths. There are at most m-1 binary branch nodes in this retained tree and at most 2m-1 paths between branch nodes, root, and marked leaves. Along the interior of each such path, every side subtree has only b leaves, so the two block endpoints remain unchanged. A ring-reduced path never repeats its annotated nonterminal: SCCs are visited only once in order, and each ring is traversed without completing a turn. Therefore it has at most g nonterminal occurrences. Every removed b-only subtree, after its own ring reduction, has root-to-leaf paths with at most g original nonterminal labels and hence at most 2^g leaves. This gives a bound of the form m+g(2m-1)2^g for the base yield, with a harmless increase of the constant for path endpoints. The skeleton is a binary tree of linear size in that yield, so its number of maximal ring-path occurrences is also O_G(m).

**Lemma 9 (kernel degree).** If one skeleton has r period occurrences and its period matrix has rank q, then along some infinite sequence of words the grammar has ambiguity Omega(n^(r-q)), where n is the word length. Thus a global bound O(n^d) forces r-q<=d for every skeleton in every bounded slice.

Proof. Put h=r-q and choose an integral basis z_1,...,z_h of the rational kernel. Start with the exponent vector N(1,...,1). There is a fixed positive epsilon such that every vector

    N(1,...,1)+sum_j t_j z_j,  |t_j|<=epsilon N,

has nonnegative coordinates. These are Omega(N^h) distinct integral exponent vectors, all with the same period sum. Each determines a different tree by skeleton uniqueness. Their common yield length is |c|+N sum_i |v_i|, linear in N because every period is nonzero. This proves the claim.

These bounds do not yet exclude polynomial ambiguity for Q. The NE_M slices already admit finite-ambiguity grammars for each M, and their known inherent ambiguity lower bound is only linear in M. Furthermore bounded entries alone do not make all lattice-clearing constants polynomial in M: determinants of sparse matrices may involve differences of long products of bounded integers. Any attempt to compare a lower bound such as M^(omega(M)) with n^d must first control the *word length* n of the certified witnesses; an exponential-in-M lower bound on necessary witness scale would defeat that comparison.
