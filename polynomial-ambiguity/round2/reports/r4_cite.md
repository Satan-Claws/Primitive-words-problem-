# R4-C: citation check (Kászonyi–Katsura, Dömösi–Horváth–Ito, Petersen, Dömösi–Ito book)

Scope: per prompt §8, I searched only for the named papers by author and title. I made no search for a solution.
Labels:
- **VERIFIED-PRIMARY**: I read the statement in the paper itself.
- **VERIFIED-REVIEW**: I read it in a zbMATH summary or review.
- **SECOND-HAND**: the statement is attributed to the paper by its own authors in a later paper; I did not see the original.
- **NOT FOUND**: I found no accessible text.

Notation: Q = primitive words, Q_n = Q ∩ (ab*)^n, E(Q_n) = exponent vectors (e_0..e_{n-1}) of a b^{e_0} ... a b^{e_{n-1}}.

## 1. Kászonyi–Katsura results on Q_n

| n covered | paper | label |
|---|---|---|
| n a prime power | FCT'93 (DHIKK) | SECOND-HAND (zbMATH summary of KK 1999 below) |
| n = p^a q^b (two distinct primes), incl. n = 6 | Dömösi, S. Horváth, Ito, Kászonyi, Katsura, "Formal languages consisting of primitive words", FCT'93, LNCS 710, 194–203 (Zbl 0794.68090) | SECOND-HAND. KK 1997 abstract: "We proved in [2] that the conjecture is true if n is a product of two prime-powers." The zbMATH review of KK 1997 agrees. Kászonyi 2010 p. 325: "Proving the context-freeness of Q6, Katsura Masashi introduced two special types of DLI-sets." The FCT'93 text and its zbMATH review are not accessible. |
| n = p^{f1} q^{f2} r^{f3}, with p, q, r distinct primes and f_i ≥ 1 | Kászonyi & Katsura, "On the context-freeness of a class of primitive words", Publ. Math. Debrecen 51 (1997) 1–11, doi 10.5486/PMD.1997.1707, Zbl 0886.68087 | **VERIFIED-PRIMARY**, Theorem 1 p. 6, verbatim below |
| n = ∏ p_i^{f_i} with Σ_i 1/p_i < 4/5 (any number of primes) | Kászonyi & Katsura, "Some new results on the context-freeness of languages Q ∩ (ab*)^n", Publ. Math. Debrecen 54 Suppl. (1999) 885–894 (AFL'96), Zbl 0981.68099 | **VERIFIED-REVIEW** (zbMATH summary). Also quoted verbatim as Theorem 1 in Kászonyi 2010 (VERIFIED-PRIMARY for the quotation). |
| E_1 ∩ E(Q_n) and E_k ∩ E(Q_n) are stratified semilinear for every n (k = number of distinct primes; E_α is a class in Kászonyi's classification). E_α for 2 ≤ α ≤ k−1 is only conjectured. | Kászonyi, "Semiperiodic vectors and the context-freeness of Q_n = Q ∩ (ab*)^n", Publ. Math. Debrecen 77 (2010) 313–330, Zbl 1274.68159 | **VERIFIED-PRIMARY** (Theorem 6 and the conjecture on p. 328). |
| Decomposition of E(Q_n) for arbitrary n into components that are conjectured to be stratified semilinear | Kászonyi & Katsura, "On an algorithm concerning the languages Q ∩ (ab*)^n", PU.M.A. 10(3) (1999) 313–322, Zbl 0954.20038 | VERIFIED-REVIEW (zbMATH summary) |

**KK 1997, Theorem 1, verbatim:** "Let a, b ∈ X a ≠ b and n = p^{f1} q^{f2} r^{f3}, where p, q and r are pairwise
different prime numbers, f1, f2, f3 ≥ 1. Let further L = (ab*)^n. Then Q ∩ L is a context-free language."

The proof gives an exact description, (2.2)/(2.3) on p. 6:
- E(Q ∩ L) = E(n) := ∪_{i=1..5} E(Π_i) if pq ≠ 6;
- E(Q ∩ L) = E(n) ∪ C if pq = 6.

The ingredients are:
- Π_i ranges over the five partitions of {p, q, r}.
- E(Π) is the union, over all pairwise non-nested placements of boxes B(ξ_j; π_j), of the sets {e : Δ(B(ξ_j; π_j), e) ≠ 0 for all j}.
- Δ is the signed alternating sum of e over the box B(ξ; π) = {ξ − Σ ε_i n/p_i}.
- C is an explicit extra family. It consists of three ≠ conditions on an n/6-chain and an n/r-pair.

The paper's conclusion (p. 10) says: "The proof of Theorem 1 has some ad hoc elements."

**KK 1999, zbMATH summary, verbatim:** "It is proved by [DHIKK, FCT'93] and by [Mateescu, Păun, Rozenberg, Salomaa, J.UCS 1 (1995)
790–810] that the statement is true if n is a prime power or if n is the product of two or of three prime powers. Here
we prove the validity of the assertion for all n of the form n = p_1^{f_1}…p_k^{f_k} where p_1,…,p_k are distict prime
numbers satisfying the inequality Σ 1/p_i < 4/5."

**Kászonyi 2010, Theorem 1, verbatim:** "(Kászonyi, Katsura [17]). Let n = p_1^{f_1}···p_k^{f_k} where p_1, …, p_k
are distinct prime numbers and f_1, …, f_k are positive integers. Assume that Σ_{i=1}^k 1/p_i < 4/5. Then the language
Q ∩ (ab*)^n is context-free." The same paper calls this "The sharpest result considering this conjecture".

**Net coverage (from the above):**
- Q_n is CF whenever n has ≤ 3 distinct prime factors. The 1- and 2-prime cases are SECOND-HAND; the 3-prime case is VERIFIED.
- Q_n is CF whenever Σ 1/p < 4/5 (VERIFIED-REVIEW).
- The smallest uncovered n is 210 = 2·3·5·7 (Σ = 247/210). This is consistent with RESULTS_INDEX.

**Corrections to repo text:**
- `context-free/reports/devil.md` §4 is substantively right: two prime powers, then three (1997), then Σ1/p < 4/5. However:
  - The 4/5 theorem is **KK 1999** (Publ. Math. Debrecen 54 Suppl.), not "Kászonyi 2010". The 2010 paper only quotes it.
  - "≤ 3 prime powers" means ≤ 3 **distinct primes**, with arbitrary exponents.
- `infinite-ambiguity/.../audit4.md` flags r6's use of n = 6 as a gap. It is now attested by three independent self-citations of the authors:
  - the KK 1997 abstract;
  - the zbMATH summary of KK 1999;
  - Kászonyi 2010 ("Proving the context-freeness of Q6, Katsura …").

  The primary FCT'93 text is still unseen.

## 2. Form of the constructions: grammars? uniform in n? ambiguity?

**Grammars.** The papers write no grammars (VERIFIED-PRIMARY for KK 1997 and Kászonyi 2010). Context-freeness goes through:
1. Ginsburg's theorem: a bounded language is CF iff its exponent set is stratified semilinear.
2. Lemma 1 / the Flip-Flop lemma: {e : Σ δ_i e_i ≠ 0} is stratified semilinear, and so is any intersection of such sets over pairwise non-crossing index sets. The sources are Kászonyi, PU.M.A. 6 (1995) 203–210, Zbl 0851.20059, and Holzer–Kászonyi, Publ. Math. Debrecen 54 Suppl. (1999) 877–884.

Kászonyi 2010 does speak of "constructions for grammars generating subclasses of Q_n" (p. 314), but only at the level of exponent sets.

**Per-n.** Each theorem is a statement about one fixed n, i.e. one bounded slice (ab*)^n. The proof is a schema in n (boxes, partitions of the prime set), but it yields a finite union whose number of pieces depends on n. No paper gives one grammar for infinitely many n, or a language covering Q ∩ ∪_n (ab*)^n. The 1997 proof needs a separate ad hoc family C when pq = 6.

**Ambiguity.** No statement about ambiguity appears in KK 1997 or Kászonyi 2010; I searched for "ambig" and the one hit is about notation. The pieces E(Π) are unions over overlapping choices of ξ.
- (My observation, not a cited claim.) As written, the decomposition is not disjoint, so it says nothing about bounded ambiguity.

## 3. Dömösi–Horváth–Ito conjecture, Petersen, Dömösi–Ito book

**DHI conjecture.** VERIFIED as quoted by the authors themselves, in Dömösi, S. Horváth, Ito, Katsura, "Some results on primitive words, palindromes and polyslender languages", Publ. Math. Debrecen 65 (2004) 13–28, p. 14:
> "Conjecture (P. Dömösi, S. Horváth, M. Ito, 1991 [4]). Q is not context-free."

- Their [4] is "On the connection between formal languages and primitive words", Proc. First Session on Scientific Communication, Univ. of Oradea, 1991, Analele Univ. Oradea, Fasc. Mat., 59–67. I did not see the original.
- The same p. 14 says: "Q is not unambiguous context-free (J.-P. Allouche [1], H. Petersen [25]), moreover, that it is not linear context-free and not bounded (S. Horváth [13])", and "it is easy to see that Q is deterministic context-sensitive".
- p. 15: "Q ∩ (ab*)^n has proved to be context-free for exponents n, belonging to wider and wider (infinite) classes of positive integers".
- Attribution of the (ab*)^n conjecture varies:
  - Kászonyi 2010 cites FCT'93;
  - the zbMATH summary of KK 1999 cites DHI, Publ. Math. Debrecen 42 (1993) 315–321;
  - the KK 1997 abstract cites FCT'93.

**Petersen.** The bibliographic data are VERIFIED (zbMATH Zbl 0872.68091):
- H. Petersen, "On the language of primitive words", Theoret. Comput. Sci. 161 (1996) 141–156, doi 10.1016/0304-3975(95)00098-4;
- conference version: "The ambiguity of primitive words", STACS'94, LNCS 775.

The statement "Q is not unambiguous CF" is SECOND-HAND. It is cited as above by DHIK 2004 and in KK 1997 ref. [7]. The repo's `finitely-ambiguous/NOVELTY.md` records that Koechlin (FSTTCS 2022, Prop. 17) re-proves it. I could not read the abstract: ScienceDirect returned 403 and the zbMATH review is licence-blocked.

**Dömösi–Ito book.** "Context-Free Languages and Primitive Words", World Scientific, doi 10.1142/7265, xii+506 pp.:
- zbMATH Zbl 1476.68003 gives 2015; retailers give 2014.
- Chapter list (Crossref): Ch. 6 "Bounded and Palindromic Languages" pp. 135–181; Ch. 8 "Some Properties of the Language of Primitive Words" 239–266; Ch. 9 "Primitive Words in Languages" 267–308; **Ch. 10 "Kászonyi–Katsura Theory" pp. 309–342** (doi 10.1142/9789814271677_0010); Ch. 13 "Context-Free Languages and Non-primitive Words" 413–421.
- Chapter contents: NOT FOUND (worldscientific.com 403; no preview reached).
- So any claim of the form "the book proves Q ∩ L is CF for every bounded / slender / linear L" is **unverified**. This includes the BRIEFING's "Horváth–Ito: Q ∩ (slender regular / slender CF) stays regular / CF" and anything about Q ∩ a*b*a*b*.
- I found no source stating "Q ∩ L is CF for every bounded L"; the KK papers present even the (ab*)^n case as a conjecture.

## Sources
- KK 1997 full text: https://publi.math.unideb.hu/paper/376/download/10_5486_PMD_1997_1707.pdf (landing page https://publi.math.unideb.hu/paper/376)
- Kászonyi 2010 full text: https://publi.math.unideb.hu/paper/1506/download/10_5486_PMD_2010_4680.pdf
- DHIK 2004: https://publi.math.unideb.hu/paper/956/download/10_5486_PMD_2004_2521.pdf
- Dömösi–G. Horváth–Ito 2004: https://publi.math.unideb.hu/paper/935/download/10_5486_PMD_2004_2775.pdf
- zbMATH Open API (https://api.zbmath.org/v1/document/_search): Zbl 0886.68087, 0981.68099, 0954.20038, 1274.68159, 0851.20059, 0981.68084, 0794.68090, 0872.68091, 1476.68003
- Crossref chapter list for the book: https://api.crossref.org/works?query.bibliographic=Context-free+languages+and+primitive+words&filter=prefix:10.1142
- FCT'93: https://link.springer.com/chapter/10.1007/3-540-57163-9_15 (paywalled; not read)
