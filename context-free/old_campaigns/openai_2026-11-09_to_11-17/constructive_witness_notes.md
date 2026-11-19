# Mismatch certificates: precise limitations

These results concern particular certificate formats, not the capabilities of arbitrary PDAs. They do not resolve whether the primitive-word language is context-free.

Positions in this note are numbered from 0 to n−1. For d dividing n, call the orbit of i under addition of d modulo n a d-fiber. A d-fiber containing both letters certifies failure of period d. A mismatch with endpoints i,j can refute d only when d divides j−i.

## Distinct maximal periods need distinct pairs

Let p and q be distinct prime divisors of n. Then lcm(n/p,n/q)=n. A pair 0≤i<j<n cannot have both n/p and n/q dividing j−i. Consequently a mismatch-pair certificate refuting every maximal proper divisor period requires at least ω(n) pairs, where ω counts distinct prime divisors. This does not prohibit an unbounded certificate recognized by a PDA.

## Unboundedly many anchor positions can be necessary

Fix r≥2. Choose distinct primes q,p1,…,pr with q≥r, and put n=q p1⋯pr. By the Chinese remainder theorem, positions i modulo n correspond bijectively to tuples

    (x0,x1,…,xr) in Z/qZ × Z/p1Z × … × Z/prZ.

Choose a surjection s:Z/qZ→{1,…,r}. Define w_i=b exactly when x_{s(x0)}=0; otherwise define w_i=a.

The word w is primitive. For each j≥1, addition of n/pj fixes every CRT coordinate other than xj and cycles through all values of xj. Choose x0 with s(x0)=j. This fiber contains both xj=0 and xj=1 and therefore both letters, so n/pj is not a period. Addition of n/q fixes all data coordinates x1,…,xr and cycles through all x0. Choose x1=0 and x2=1; since s is surjective, this fiber also contains both letters. Thus n/q is not a period. Any proper-divisor period d of n divides at least one maximal proper divisor n/p, and being d-periodic implies being n/p-periodic. All maximal proper divisor periods fail, proving primitivity.

For a fixed anchor i, let j=s(x0). Changing any data coordinate xk with k≠j leaves w_i unchanged. Hence the n/pk-fiber through i is monochromatic for every k≠j. A mismatch certificate anchored at i can refute at most one of the r data periods n/p1,…,n/pr. Therefore any set of anchors whose anchored mismatch pairs refute all those periods contains at least r anchors.

This refutes every scheme restricted to a fixed number of anchors. It does not bound the number of anchors usable by a PDA.

## Explicit length-30 example

Set q=2, p1=3, p2=5, and select p1 at even positions and p2 at odd positions. Then

    w = baaaabbaaaaabaabaabaaaaabbaaaa.

Equivalently, w_i=b iff (i even and 3 divides i) or (i odd and 5 divides i). Its maximal proper divisor periods 15,10,6 fail at the pairs (3,18), (0,10), and (5,11), respectively. Every even anchor has a monochromatic 6-fiber; every odd anchor has a monochromatic 10-fiber. No single anchor witnesses all three failures.

## Primitive-factor concatenation is insufficient

For every k≥2, u=a and v=(ba)^(k−1)b are primitive, but uv=(ab)^k. Primitivity of v follows because its letter counts k−1 and k are coprime; any proper power would have its exponent dividing both counts. The factors u,v are distinct and noncommuting, and their lengths are coprime. These additional checks therefore still accept proper powers of arbitrarily large exponent.

For every odd k≥3, splitting (ab)^k into equal-length factors gives two distinct primitive factors: both are alternating words of odd length k and have coprime letter counts (k−1)/2 and (k+1)/2. Thus equal-length, distinct primitive factors are insufficient as well.

## Binary-to-arbitrary-alphabet transfer

For an alphabet {c1,…,ck}, define h(ci)=ab^i. This is an injective morphism with uniquely readable blocks, each starting with a and containing no further a. If h(w)=u^r for r≥2, then u begins with a. Every boundary between successive copies of u is therefore a block boundary. Thus u=h(v) for a nonempty word v, and injectivity yields w=v^r. Conversely a source power maps to a power. Empty words map to the empty word. Consequently h^−1(Q_{a,b})=Q_{c1,…,ck}, including source words of length one. Closure under inverse morphism would transfer a binary affirmative answer to every finite alphabet.

## Noncrossing certificates: exact restricted counterexample

For a word of length n, choose for each prime p dividing n an opposite-letter pair (i,j), 0≤i<j<n, with n/p dividing j−i. Edges are noncrossing if no two satisfy i<k<j<l or k<i<l<j. Shared endpoints are allowed.

If the eligibility rule is strengthened to j−i=n/p, not merely divisibility, the primitive word 110100 (rename 0,1 to a,b) has no noncrossing certificate. At distance 3 its only mismatch is (1,4); at distance 2 its only mismatches are (0,2) and (3,5), and both cross (1,4). Under the original eligibility rule, (0,4) is an eligible period-2 mismatch and does not cross (1,4). Thus modular wraparound/multiples cannot be discarded in this construction.

## Finite evidence for unrestricted noncrossing certificates

`noncrossing_witnesses.py` exhaustively checked lengths 6,10,12,14,15,18 and found certificates for every primitive word. Complement symmetry was used to fix the first bit. Random checks found no counterexample among 20,000 words of length 30, 2,000 each of lengths 42 and 60, and 100 of length 210.

`noncrossing_sat.py` performs a CEGIS proof for one fixed length. It requires a Boolean word to fail every maximal divisor period. Whenever a model admits a noncrossing certificate, it adds the clause that at least one edge of that specific certificate must have equal endpoint bits. Every clause is valid for the sought counterexample. Z3 returned UNSAT at n=6,30,42,60 after 9,498,1079,2186 clauses, respectively. At n=210 it timed out after 60 seconds and 16,636 clauses. These finite results neither prove the conjecture for general n nor constitute a PDA construction.

The length-30 multiplexer has the nested certificate (prime,edge)

    (2,(3,18)), (3,(0,20)), (5,(3,15)).

## Nesting does not itself implement variable divisibility

The auxiliary language D={a^d b^(kd): d≥1, k≥1} is not context-free. Its Parikh image is S={(d,kd): d≥1,k≥1}. Here is an elementary proof that S is not semilinear. Suppose S were a finite union of linear sets, all with nonnegative integer period vectors. Let B exceed the second coordinate of every vertical positive period vector (0,b) in this finite representation. Choose d>B. The vertical fiber at first coordinate d is infinite. In a linear component, coefficients of generators with positive first coordinate are bounded on this fiber. Thus some component meeting the fiber must contain a positive vertical generator (0,b). Starting from a point (d,y) in that component gives both (d,y) and (d,y+b) in S, forcing d to divide b. This contradicts 0<b<d. Parikh's theorem now excludes context-freeness of D.

Therefore a generic subroutine that explicitly represents arbitrary candidate divisor d and total length kd in two unary fields is already beyond context-free power. This only blocks that encoding: it is not a lower bound against a different certificate system or against an arbitrary PDA for Q. The noncrossing-certificate conjecture, even if true, still needs a specific finite mechanism for identifying the required divisor periods and checking all of them.
