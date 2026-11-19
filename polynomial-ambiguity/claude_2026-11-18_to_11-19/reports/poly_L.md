# poly_L: global pumping + loop collision (Wich-criterion lever) — status: BLOCKED (obstruction PROVED)

Working hypothesis (LITERATURE, Wich 2005, unverified here): reduced cycle-free G exp-ambiguous iff some A
has two distinct trees A =>+ uAv with equal (u,v).

## Lemma O (PROVED). For coprime-defect data the lever is vacuous.
For r,s >= 0 (not both 0), c != 0 let L_{r,s,c} = { w : r|w|_a - s|w|_b = c }.
(1) L_{r,s,c} is a DCFL (counter value r#a - s#b, sign and |value| <= max(r,s,|c|) in the state,
    rest on stack; accept iff value = c), hence has an unambiguous CFG.
(2) gcd(|w|_a,|w|_b) divides c; for c = ±1 every w in L_{r,s,±1} is primitive (w = z^k => k | gcd).
(3) So U = finite union of L_{r_i,s_i,±1} is a finitely ambiguous (<= #pieces) CF sublanguage of Q.
Example: L_{1,1,1} = D_b·a·B (B = balanced words), unambiguous, contains (a^n b^n)^p a, (ab)^p a, x^p y
for all |x|_a=|x|_b, |y|_a=|y|_b+1, all p.

## Consequence (exact obstruction)
Any argument whose inputs are: L(G) ⊆ Q, a test family W ⊆ L(G), Ogden/pumping on W (contexts with
u^i z v^i in Q), Lyndon–Schützenberger on pumped words — and W ⊆ U for some U as in (3) — is satisfied by
the finitely ambiguous grammar of U (Ogden holds in every CFG; pumped words stay in U ⊆ Q; non-primitive
words such as (a^n b^n)^2, a^n b a^n b are automatically avoided since their letter counts have gcd >= 2).
Hence it cannot produce a Wich collision. Likewise any regular W-family (x^p y, x,y fixed) lies in a
regular R ⊆ Q (DFA grammar, unambiguous). Different Ogden markings give different contexts, but nothing
forces equal (u,v): collisions need a counting/commutation source.

## What a working lever must use
W must contain words with gcd(|w|_a,|w|_b) unbounded and Parikh vectors not on finitely many lines
r#a - s#b = ±1, where primitivity is not Parikh-certified — e.g. the slice (ab*)^n, n fixed, where the
collision in finitely-ambiguous/PROOF.md §3(c) comes from commuting b-insertions (two contexts, same
yield pair). That is exactly the slice method; global pumping adds nothing beyond it.
Caveat: the obstruction covers arguments localized on W; it does not exclude arguments using that
L(G) = Q globally (all of Q, incl. non-Parikh-certified words).
