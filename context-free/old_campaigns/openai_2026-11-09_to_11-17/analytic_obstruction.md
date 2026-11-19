# A limitation of density plus word-counting arguments

This is an obstruction to a proposed proof strategy, not a resolution of the
primitive-word problem.

Let the alphabet be `{a,b,c}` and define

\[
L=\{w:w\text{ is not a square}\}\cup
  \{w:|w|_a\ne|w|_b\}\cup
  \{w:|w|_b\ne|w|_c\}.
\]

Each component is context-free. For the first component use the classical
non-square construction allowed in the problem. For either count inequality,
a one-stack machine maintains the signed difference of the two letter counts:
on an opposite-sign letter it pops, on a same-sign letter it pushes, and it
ignores the third letter; accept precisely when the final difference is nonzero.
Finite union preserves context-freeness.

Its complement is exactly

\[
M=\{xx:|x|_a=|x|_b=|x|_c\}.
\]

Thus its word-counting series is

\[
L(z)=\frac1{1-3z}-\sum_{m\ge0}\frac{(3m)!}{(m!)^3}z^{6m}.
\]

Stirling's formula gives

\[
\frac{(3m)!}{(m!)^3}=\frac{\sqrt3}{2\pi m}\,27^m(1+O(m^{-1})).
\]

Writing `t=27z^6`, the second term has the behavior
`-(sqrt(3)/(2*pi))*log(1-t)+O(1)` as `t` increases to 1 from below.
The bounded remainder follows because the coefficient error is `O(m^-2)`.
An algebraic function has a convergent local Puiseux expansion at a finite
singularity and cannot have logarithmic divergence. Therefore this series,
and hence `L(z)`, is not algebraic.

Nevertheless `L` has density tending to one exponentially fast. Its missing
words number zero except in lengths divisible by 6, where the deficit is
`Theta(3^(n/2)/n)`.

Consequently, a criterion based only on context-freeness, density one with
exponentially few missing words, and nonalgebraicity would be false. This
example makes no assertion about every possible finer analytic invariant or
the ambiguity degree of a grammar for the primitive words.

## Natural boundaries are possible too

There is also a context-free language with exponentially few missing words
whose word-counting function has a natural boundary after analytic
continuation. Let `Sigma={a,b,c,d}` and let

\[
M_2=\{x_0c x_1c\cdots x_kc:k\ge0,\ x_i\in\{a,b\}^{2^i}\}.
\]

Its complement `L_2` is context-free by an explicit finite union of rejection
conditions:

1. The word is outside the regular syntax `((a|b)+c)+`.
2. Within that syntax, the first block does not have length one.
3. Within that syntax, some adjacent blocks have lengths `r,s` with `s!=2r`.

For the third condition a PDA guesses the adjacent pair, pushes two stack
markers per letter of the first block, and pops one per letter of the second.
It recognizes a surplus or deficit at the next separator, then consumes the
remaining regular block suffix. Regular intersection and finite union are
valid CFL operations. This argument does not use closure under complement
of an arbitrary CFL.

The only missing lengths are `N_k=2^(k+1)+k`, and

\[
M_2(z)=\sum_{k\ge0}2^{2^{k+1}-1}z^{N_k},\qquad
L_2(z)=\frac1{1-4z}-M_2(z).
\]

The missing counts are at most `2^n=|Sigma|^(n/2)`, so `L_2` has exponentially
convergent density one. The radius of convergence of `M_2` is `1/2`, since
`(2^(2^(k+1)-1))^(1/N_k)` tends to `2`. In the scaled series

\[
M_2(t/2)=\sum_{k\ge0}2^{-k-1}t^{N_k},
\]

the radius is one and `N_(k+1)/N_k` tends to two. The Hadamard gap theorem
(a power series with radius one and exponent ratios uniformly greater than
one has the unit circle as a natural boundary) therefore applies. Adding a
rational function cannot remove this boundary. This is a further obstruction
to a criterion using only density and the presence of infinitely many
singularities; it does not disprove every more specific analytic approach.
