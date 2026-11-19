# Length congruences: exact reductions and a boundary

Status: elementary written proofs. No resolution of Q context-freeness.

## Every divisibility slice retains the entire problem

For each integer m>=1,

Q intersect {w : m divides |w|}

is context-free if and only if Q is context-free.

Proof. One direction is regular intersection. For the other, let d=3m and define the uniform code

h(a)=a b^(d-1),    h(b)=a^2 b^(d-2).

Both codewords have length d and consist of one positive a-run followed by one positive b-run. Every concatenation has its codeword boundaries exactly at its b-to-a transitions. If h(w)=u^k with k>=2, u begins in a and ends in b, so the root boundary is one of those transitions. Thus u consists of full codewords, and the repeated run-pair sequence forces w to be a proper power. Conversely a proper power w visibly maps to a proper power. The one-letter codewords are themselves primitive because each has exactly one cyclic a-run and one cyclic b-run. The empty word remains nonprimitive. Hence h preserves primitivity, and its output lengths are divisible by m. Taking inverse homomorphism proves the claim. QED.

The same proof works for any ultimately periodic length set containing all sufficiently large multiples of some positive integer: choose a suitable uniform length, apply the inverse homomorphism, and restore the finitely many excluded short primitive inputs.

## Congruence slices outside that homomorphic barrier

No morphism can map every binary primitive word into words whose lengths are not divisible by a fixed m>=2. The word a^m b^m is primitive: it has just one cyclic a-run, so a proper power is impossible. But under any morphism h its image has length m(|h(a)|+|h(b)|), divisible by m. This includes erasing morphisms as well.

In particular the odd-length primitive slice is not shown equivalent to all Q by the preceding universal homomorphic embedding. This does not exclude more general rational-transduction reductions, and does not establish that the odd-length slice is context-free or non-context-free. Its status remains unresolved in this investigation.
