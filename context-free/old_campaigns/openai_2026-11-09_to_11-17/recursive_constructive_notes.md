# Recursive and conjugacy-based constructive candidates

These are exact characterizations and obstructions to particular implementations. They do not resolve the primitive-word context-freeness question.

## Distinct unbordered factors give a sound certificate

A nonempty word is unbordered when it has no nonempty proper prefix equal to a suffix. If u and v are nonempty unbordered words with u≠v, then uv is primitive.

Proof: suppose uv=r^k, where k≥2 and p=|r|. Every contiguous factor of this periodic word whose length exceeds p has a border of length its length minus p. Since u and v are unbordered, both have length at most p. Thus kp=|u|+|v|≤2p. It follows that k=2 and |u|=|v|=p, giving u=v=r, contrary to the hypothesis.

Conversely, every primitive word of length at least two is a rotation of a concatenation of two distinct nonempty unbordered words. Choose its lexicographically least rotation l. The standard Lyndon-word characterization says that l is Lyndon. Its standard factorization l=uv has u and v Lyndon with u<v. Lyndon words are unbordered, and u<v implies u≠v. Thus, writing U for the nonempty unbordered words,

    Q = Σ ∪ cyc({uv : u,v∈U and u≠v}).

Here cyc denotes all cyclic shifts. The equality handles ε explicitly: ε belongs to neither side. It also handles all length-one words via Σ. The standard Lyndon facts used are: a primitive necklace has a unique lexicographically least Lyndon representative; Lyndon words are unbordered; and every Lyndon word of length at least two admits standard factorization into Lyndon words u<v.

This is a genuine necessary-and-sufficient certificate up to rotation. To turn it into a CFG still requires a finite mechanism that checks unborderedness of the children and their inequality. The statement alone is not such a mechanism.

## An exact recursive Lyndon characterization

Fix a total order on Σ and the induced usual lexicographic order, with a proper prefix smaller than the word containing it. Consider binary trees whose leaves are letters and whose internal nodes concatenate their left and right yields. Impose at each internal node the condition that its left yield is lexicographically smaller than its right yield.

The resulting root yields are exactly the Lyndon words. The forward implication is induction using the standard theorem that u,v Lyndon and u<v imply uv Lyndon. The reverse implication recursively uses standard Lyndon factorization. Rotating these yields and adding no empty yield gives exactly Q.

The comparison here concerns complete subtree yields; it is not a finite nonterminal annotation. A generic one-stack implementation of the proposed comparison is impossible, as the next lemma shows.

## The separated lexicographic comparison relation is not context-free

Let

    C = {x#y : x,y∈{a,b}*, x<lex y}, with a<b.

Then C is not context-free. Intersect it with the regular language a^+b^+#a^+b^+ to get K. In K,

    a^i b^j # a^k b^l belongs iff i>k, or i=k and j<l.

Suppose K has pumping constant p≥1 and use

    w = a^p b^p # a^p b^(p+1).

For every allowed decomposition w=uvxyz, |vxy|≤p and |vy|>0:

1. If v or y contains #, pumping down removes the unique separator.
2. If v or y crosses an a/b boundary, pumping up makes the word leave a^+b^+#a^+b^+.
3. Otherwise each nonempty pumped piece lies within one homogeneous block. The length bound prevents the pumped pieces from meeting both a-blocks, or both b-blocks.
4. If the first a-block is changed, pumping down makes its exponent less than that of the second a-block (or removes it). The resulting word is not in K. If only the second a-block is changed, pumping up similarly makes its exponent greater than that of the first and leaves K. Changes to b-blocks cannot repair the strict inequality between a-exponents.
5. If no a-block is changed, exactly one b-block is changed. Pumping the first b-block up makes its exponent at least p+1, so it is no shorter than the second b-block. Pumping the second b-block down makes its exponent at most p, so it is no longer than the first. Either choice leaves K.

Every allowed decomposition therefore fails for pumping exponent 0 or 2. This contradicts the context-free pumping lemma. Since regular intersection preserves context-freeness, C is not context-free either.

Every word a^i b^j with i,j≥1 is itself Lyndon and unbordered. Consequently the same regular intersection proves that even the separated relation restricted to Lyndon children,

    {u#v : u,v are Lyndon and u<lex v},

is not context-free. This refutes the attempted compilation that supplies the ordered-child comparison as an independently recognized PDA subroutine.

In fact this also gives a direct proof that the language of Lyndon words is not context-free. Let e erase # and fix a,b. For positive i,j,k,l, the word a^i b^j a^k b^l is Lyndon exactly when i>k, or i=k and j<l. To check this, any minimum rotation must start at the beginning of one of the two a-runs: a rotation starting inside a run has fewer initial a's and is larger. Comparing the two candidate rotations gives exactly the stated inequalities. Thus e^−1(Lyndon) intersected with a^+b^+#a^+b^+ is precisely K. Context-freeness of Lyndon would contradict the proved non-context-freeness of K.

The recursive ordered-tree description therefore characterizes an intermediate language that itself cannot be generated by a CFG. This does not refute a PDA for Q: cyclic shift can turn a non-context-free language into a context-free language, and failure of this particular intermediate route supplies no converse closure principle.

## Weakening unborderedness to unequal endpoint letters is unsound

Consider a recursive certificate whose leaves are letters and whose internal yields must (i) start and end with different letters, and (ii) have two distinct certified children. It accepts the proper square aabaab=(aab)^2:

    ab = a · b
    aab = a · ab
    abaab = ab · aab
    aabaab = a · abaab.

Every displayed internal yield starts in a and ends in b, and every split has distinct children. Thus checking endpoints and distinct recursively certified children does not replace unborderedness.

## Independent audit of the analytic examples

The three-letter dense context-free example in analytic_obstruction.md is valid, including the empty word, coefficient formula, Stirling constant, and logarithmic singularity argument. Nonalgebraicity should be interpreted by subtracting the rational full-language series, so the smaller pole of that rational series causes no convergence-domain issue.

The separate four-letter lacunary example supplied by the root is also valid. With blocks x_i∈{a,b}^{2^i} separated and terminated by c, the missing language M has lengths N_k=2^(k+1)+k and coefficient 2^(2^(k+1)−1). Its complement over {a,b,c,d} is context-free: bad block syntax is regular; a bad initial block length is regular; and otherwise nondeterministically choose adjacent blocks and compare the next length with twice the preceding length using a stack. A failure of any condition is equivalent to nonmembership in M.

The normalized missing series M(t/2)=Σ_{k≥0}2^(−k−1)t^{N_k} has radius one, and N_(k+1)/N_k tends to two. The standard Hadamard gap theorem therefore gives the unit circle as a natural boundary. The original missing series has natural boundary |z|=1/2, and subtracting it from 1/(1−4z) retains that boundary under analytic continuation. Missing coefficients are O(2^n)=O(4^(n/2)). No assumption about unambiguous grammars is involved.

## Unique extremal runs and bounded factors miss an infinite primitive family

Fix integers K≥1 and t≥2, and define

    W_(K,t) = (a^K b^K)^t (a^K b^(K+1))^t.

Its length is t(4K+1). It is primitive. Indeed, any proper-power decomposition has every root boundary at a circular b-to-a transition, since the word begins in a and ends in b. Therefore it induces a proper-power decomposition of the cyclic sequence of run pairs. Encode (K,K) by A and (K,K+1) by B. That sequence is A^tB^t, which has exactly one cyclic A-to-B transition and one cyclic B-to-A transition. In a proper r-th power every such transition count would be divisible by r≥2. This is impossible.

Every a-run has length K, repeated 2t times. The minimum and maximum b-run lengths K and K+1 are each repeated t times. Thus there is no unique extremal run of either letter.

Moreover, every cyclic factor of length ℓ≤K that occurs in W_(K,t) has at least 2t occurrences. Such a factor crosses at most one run boundary, because all runs have length at least K. The monochromatic factor a^ℓ occurs 2t(K−ℓ+1) times; b^ℓ occurs t(2K+3−2ℓ) times. Every occurring mixed factor is a^i b^(ℓ−i) or b^i a^(ℓ−i), 1≤i<ℓ, and occurs once at each of the 2t corresponding boundaries. In particular, no cyclic factor of any length at most K is unique.

For t=2, length is 8K+2, so even a primitive word can have no unique factor throughout a range of lengths growing linearly with its total length. This defeats a bounded-window unique-factor or unique-extremal-run certificate. It does not exclude comparisons of unbounded factors.

## Repeated run extrema already contain the whole primitive-word question

Fix any K≥1 and define the binary-source morphism

    g_K(A)=a^K b^K,       g_K(B)=a^K b^(K+1).

This morphism preserves and reflects primitivity. Preservation of being a power is immediate. Conversely, if g_K(v)=u^r with r≥2, then u begins in a and ends in b. Its copy boundaries are b-to-a transitions, hence run-pair boundaries. The root u is therefore a concatenation of complete, uniquely decodable codewords, say u=g_K(s); injectivity gives v=s^r.

Let R be the regular language of source words containing at least two A's and at least two B's. The language Q_{A,B} outside R is regular: it consists precisely of the single letters, the words containing exactly one A, and the words containing exactly one B. (Words with at least two of one letter and zero of the other are proper powers.) Hence Q_{A,B} is context-free if and only if Q_{A,B}∩R is context-free.

Since g_K(R) is regular and g_K reflects primitivity,

    g_K^−1(Q_{a,b}∩g_K(R)) = Q_{A,B}∩R.

Consequently Q is context-free if and only if the restricted language Q_{a,b}∩g_K(R) is context-free: one direction is regular intersection, and the other is inverse morphism followed by union with the regular exceptional part. Every word in g_K(R) has all a-runs of one fixed length K, and its two possible b-run lengths K,K+1 each occur at least twice. Thus repeated extrema cannot be relegated to finitely many exceptions or a simpler subproblem merely by reducing to run lengths. This restricted case is already equivalent to the original context-freeness question.

No finite CFG or PDA for exact Q results from these certificates. The present route ends at either an intermediate language proved non-context-free (Lyndon words / separated ordered-child comparisons) or a run-encoded restriction equivalent to Q itself.

## Direct two-unbordered-factor language T

Write T={uv:u,v are nonempty unbordered words and u≠v}. The existential split does enlarge the class of unbordered words, but T is still a proper subset of Q. For example, aabaa is primitive (it contains exactly one b), yet none of its four splits works: a|abaa and aaba|a have a bordered longer factor; aa|baa and aab|aa contain the bordered factor aa. Likewise ababa is primitive and has no such split. The cyclic closure remains essential to the exact reduction.

Every unbordered word w of length at least two belongs to T; this has an elementary proof avoiding Lyndon machinery. Choose the longest proper unbordered prefix u and write w=uv. If v had a nonempty proper border z, then uz would be a proper prefix of w longer than u. A border B of uz with |B|≤|z| would also border w, because z is a suffix of w. A border B with |B|>|z| would give a border of u of length |B|−|z|, by comparing the portion of B preceding the terminal z. Both alternatives are impossible. Thus uz would be unbordered, contradicting maximality of u. Hence v is unbordered. The factors u,v are distinct because w is unbordered and therefore cannot be a square.

Two tempting weaker criteria fail on aabaa. Its longest unbordered prefix is aab and its longest unbordered suffix is baa, so the sum of their lengths is six, greater than the word length five; their overlap does not yield a valid split. It also has an unbordered prefix longer than half the word, yet is not in T.

Some bounded-run restrictions simplify exactly, but do not supply a uniform finite grammar. For positive exponents,

    a^i b^j a^k b^l ∈ T  iff  (i,j)≠(k,l).

If the two exponent pairs differ, the middle b-to-a split gives two distinct unbordered factors. If the pairs agree, the word is a square and cannot belong to T by the first lemma. This proves the formula without classifying every split: a single-letter end factor can sometimes work too. For example, ababbb=ababb·b, and ababb is unbordered. Similarly,

    a^i b^j a^k b^l a^m b^n ∈ T
      iff i>k or l>j or k>m or n>l.

For a split with both children of length at least two, unborderedness forces the first child to end in b and the second to start in a. Thus there are only two such b-to-a split boundaries. A four-run word a^r b^s a^t b^u is unbordered exactly when r>t or u>s: its only possible proper border begins in the final a-run and has the form a^r b^u, which exists precisely when r≤t and u≤s. Applying this criterion to the four-run child at the two split boundaries gives the displayed sufficient conditions. The children at these boundaries are automatically distinct, since one has two runs and the other four.

It remains to check splits with a single-letter child. If all four displayed inequalities fail, then i≤k≤m and n≤l≤j. For the split a·v, if i=1 then v begins and ends with b and is bordered. If i≥2, v has the nonempty proper border a^(i−1)b^n: the prefix is available because n≤j, and the suffix because i−1≤m. For the split u·b, if n=1 then u begins and ends with a and is bordered. If n≥2, u has the nonempty proper border a^i b^(n−1), using i≤m and n−1≤j. Hence these endpoint splits cannot add a word when all four inequalities fail. This completes both directions of the six-run formula. These slices are finite unions of elementary comparison languages and do not handle an unbounded number of runs.

Even primitivity together with unequal endpoint letters does not ensure membership in T. The word ababaab is primitive because its letter counts are 4 and 3, and it begins in a and ends in b. Its six splits all have a bordered child: the length-one initial split leaves babaab (border b); the length-two initial split leaves abaab (border ab); and the remaining initial factors aba, abab, ababa, ababaa have borders a, ab, a, a respectively.

The direct-T investigation has not produced either an explicit CFG for T or a proof that T is not context-free. It avoids the already refuted standalone lexicographic comparator, but its remaining unborderedness checks have not been replaced by a finite local certificate.

## Both adjacent difference compressions can destroy primitivity

For a cyclic tuple x=(x_0,…,x_29), let d_i=x_(i+1)−x_i, with indices modulo 30. Define

    A=(2,0,1)^5,       B=(−1,−2,0,−2,0)^3,
    d_(2j)=A_j,        d_(2j+1)=B_j   (0≤j<15).

The two sums are 15 and −15, so the differences sum to zero. Integrating from x_0=100 gives the positive cyclic tuple

    (100,102,101,101,99,100,100,102,100,100,
     100,101,100,102,100,100,100,101,99,101,
     101,101,100,101,99,101,101,101,99,100).

This tuple is primitive. If x had divisor period 10, then its differences would have period 10 and A would be invariant under cyclic shift 5, contradicted by A_0=2 and A_5=1. Period 6 similarly would make B invariant under shift 3, contradicted by B_0=−1 and B_3=−2. Period 15 would swap parity in d, but d_0=2 whereas d_15=B_7=0. These exclude every maximal proper divisor period of 30, hence every proper divisor period.

Nevertheless both adjacent perfect-matchings compress x to nonprimitive tuples: the oriented differences across pairs (x_(2j),x_(2j+1)) give A, while those across pairs (x_(2j+1),x_(2j+2)) give B. Both displayed tuples are proper powers. Moreover

    Σ_j x_(2j) − Σ_j x_(2j+1) = −Σ_j A_j = −15 ≠ 0.

Thus nonzero alternating sum does not repair the assertion that one of the two adjacent difference compressions of a primitive tuple must remain primitive. This is a finite exact counterexample, not a conclusion about arbitrary pushdown automata.
