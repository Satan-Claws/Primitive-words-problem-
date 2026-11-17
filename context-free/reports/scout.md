# Scout report: what is known about "Q (primitive words over {a,b}) is not context-free"

Agent: scout. Date of search: 2026-11-15.

**I do not claim a proof in either direction.** This report maps the literature and adds a few
small observations, each marked PROVED (complete argument given here), CHECKED BY COMPUTER (script
named), CONJECTURED, or FROM LITERATURE (citation and confidence).

**Access caveat (read this first).** This session's network allowed web *search* only. Direct fetches
of cs.uwaterloo.ca (CoWiki), eiche.theoinf.tu-ilmenau.de (Leupold abstract), air.repo.nii.ac.jp (Sin'ya
survey), arXiv, Springer and every other host were blocked (DNS refused by the sandbox), and the
Consensus quota was used up. So every "FROM LITERATURE" item below rests on search-engine abstracts
and snippets, not on reading the full papers. Confidence labels:
- **HIGH**: several independent sources agree, or an abstract states it verbatim.
- **MED**: one source, or a fragmentary snippet.
- **LOW**: inferred, or the sources conflict.

Before anyone builds on a MED or LOW item, check it against the primary source.

---

## 1. Status: still open (as of Nov 2026)

| Claim | Source | Conf. |
|---|---|---|
| Conjecture first stated by Dömösi, Horváth, Ito: P. Dömösi, S. Horváth, M. Ito, "On the connection between formal languages and primitive words", Analele Univ. Oradea, Fasc. Mat. (1991) 59–67; follow-up "Formal languages and primitive words", Publ. Math. Debrecen 42(3–4) (1993) 315–321 (Zbl 0805.68093). | citing bibliographies; https://publi.math.unideb.hu/paper/82 | HIGH |
| Dömösi–Ito monograph *Context-Free Languages and Primitive Words* (World Scientific 2014/15, 506–520 pp.): "It is a well-known conjecture that the set of all primitive words Q over a non-trivial alphabet is not context-free: this conjecture is still open." | https://www.worldscientific.com/worldscibooks/10.1142/7265 | HIGH |
| Oct 2025 (STACS 2026): Amarilli, Monet, Raphaël, Salvati, "On the Complexity of Language Membership for Probabilistic Words", arXiv:2510.08127, calls Q "a language whose context-freeness is a long-standing open problem". | https://arxiv.org/abs/2510.08127 | HIGH |
| 2026 Acta Informatica paper on omega-order string sorting: "It is worth noting the longstanding conjecture that the language of primitive words is not context-free. To the best of our knowledge, this conjecture remains open." | https://link.springer.com/article/10.1007/s00236-026-00530-5 | HIGH |
| Prize Problem Ledger PPL 165 ("Shallit #7: Are primitive binary words context-free?"): £200 personal offer by J. Shallit, listed as open since 2014. | https://prizeproblems.org/problems/165/ | HIGH |
| Listed on A. Amarilli's open-questions page. | https://a3nm.net/work/research/questions/ | MED |
| Sin'ya surveys: "原始語の集合と文脈自由言語について" (On the set of primitive words and context-free languages), Research Reports of the Graduate School of Engineering Science, Akita Univ. 39 (2018) 15–22 (the riko39_15_22.pdf). Related talks: "A quantitative approach to the primitive words conjecture" (CLA 2020, video https://www.youtube.com/watch?v=5u7TBiUCnVk); "原始語予想 – a survey" (SLACS 2020), whose abstract promises an intuitive reason, from the viewpoint of density, why the conjecture is hard; "Asymptotic approximation in formal languages" (CLA 2023 slides https://cla.tcs.uj.edu.pl/pdfs/CLA_slides_Sinya.pdf). | J-GLOBAL record; SLACS2020 site | MED (contents not read) |

**Searches for 2023–2026 resolution claims found none.** The searches covered arXiv-indexed hits, "Dömösi–Horváth–Ito conjecture", "primitive words conjecture" and "primitive words not context-free proof".

Unrelated 2026 preprints that turned up:
- arXiv:2602.14722 (geometric criterion for CFL intersections). It does not mention Q.
- arXiv:2609.08571 (negative answer to Bucher's density problem for CFLs; the authors say most ideas came from an LLM). It does not resolve Q.

**Note on alphabet size (PROVED here, F1 in §5).** The conjecture is the same for every alphabet size k ≥ 2.

---

## 2. Kászonyi–Katsura theory: Q_n = Q ∩ (ab*)^n

**Exponent set (PROVED).** a b^{k1} a b^{k2} … a b^{kn} is a proper power iff the integer sequence
(k1,…,kn) is a proper power, i.e. invariant under the shift by n/p for some prime p | n.

Proof: if the word equals u^p, then u begins with a and contains n/p letters a, so
u = a b^{k1} … a b^{k_{n/p}} and the sequence has period n/p. The converse is immediate.

So E(Q_n) = {k ∈ ℕ^n : k is a primitive sequence} = ∩_{p | n} ∪_i {k_i ≠ k_{i+n/p}}.

By Ginsburg–Spanier, Q_n is CF iff E(Q_n) is a finite union of **stratified** linear sets. Stratified means:
- each period vector has at most 2 nonzero coordinates; and
- no two periods have "crossing" supports i < j < k < l.

**The difficulty.** When the intersection over primes is distributed, the ≠-pairs for different primes cross. Unlike the word case, pairs that share an index also hurt here, because exponents are unbounded. For example, {a^i b^j c^k : k > i, k > j} is not CF: pumping a^p b^p c^{p+1} fails for every decomposition (my quick argument, not written out formally).

| Claim | Source | Conf. |
|---|---|---|
| **Conjecture (Kászonyi–Katsura conjecture, KK).** Q_n is CF for every n ≥ 1. It originates in Dömösi–Horváth–Ito, Publ. Math. Debrecen 42 (1993). Kászonyi–Katsura 1997 abstract: "It was conjectured in [2] that intersecting Q with the bounded language L_n = (ab*)^n, we get a context-free language". Kászonyi DLT 2002: "It is conjectured in [3] that Q_n is context-free for all positive numbers n." | https://link.springer.com/chapter/10.1007/3-540-45005-X_31 ; Publ. Math. Debrecen 51 (1997) 1–11, doi 10.5486/PMD.1997.1707 | HIGH that this is a conjecture |
| Some search summaries say "Kászonyi–Katsura showed Q ∩ (ab*)^n is CF for all n". This appears to be a misparse of "it was conjectured by … that …". Do not use it. | — | LOW |
| **Proved: n = p^r and n = p^r q^s** (p ≠ q primes). Also for L = (a+b+)^n. Source: Dömösi, Horváth, Ito, Kászonyi, Katsura, "Formal languages consisting of primitive words", FCT'93, LNCS 710, 194–203 (OCR snippet: "Let a,b ∈ X, a ≠ b, n = p^r or n = p^r q^s … Let L = (ab*)^n or L = (a+b+)^n. Then Q ∩ L is a context-free language"). The paper poses as open whether the theorem holds for all n. | https://link.springer.com/chapter/10.1007/3-540-57163-9_15 | HIGH/MED |
| **Proved: n a product of three prime powers.** Source: Kászonyi–Katsura, "On the context-freeness of a class of primitive words", Publ. Math. Debrecen 51 (1997) 1–11, and/or "Some new results on the context-freeness of languages Q∩(ab*)^n", Publ. Math. Debrecen 54 Suppl. (1999) 885–894. Snippet: "The authors proved in [2] that the conjecture is true if n is a product of two prime-powers. The paper generalizes this to the case when n is a product of three prime-powers." The monograph has §10.6 "The Language Q ∩ (ab*)^n with Three Prime Divisors of n" (p. 332). §10.3 is titled "…with Some Restrictions on the Prime Divisors of n", so some three-prime results may carry side conditions. | ResearchGate snippet; B&N/WS table of contents | MED |
| **General n (ω(n) ≥ 4; smallest n = 210) appears OPEN.** The latest sources found (Kászonyi DLT 2002, DM 2002) still call it a conjecture. A 2010 Kászonyi paper, "Semiperiodic vectors and the context-freeness of Q_n = Q∩(ab*)^n", exists; its content was not found. | as above | MED |
| Algorithmic paper: Kászonyi–Katsura, "On an algorithm concerning the languages Q∩(ab*)^n", PU.M.A. 10(3) (1999) 313–322 (content not found). | repec listing | MED |
| **DLI-sets/languages.** Introduced "in connection with the problem of deciding the context-freeness of Q_n". Kászonyi, "A pumping lemma for DLI-languages", Discrete Math. 258 (2002) 105–122: it generalizes a lemma giving a **necessary and sufficient condition for a DLI-set to be stratified semilinear**, and proposes a decomposition of E(Q_n) into components that "are, by our conjecture, stratified semilinear sets". Kászonyi, "On the structure of graphic DLI-sets", DLT 2002, LNCS 2450 (2003) 349–356: a sufficient condition for stratified semilinearity; finding DLI-sets beyond the earlier "boxes" would help the general case. Open problems listed there: characterize graphic DLI-sets, and characterize stratified semilinear DLI-sets. The acronym "DLI" was not expanded in any snippet. My guess is sets cut out by ≠/linear-inequality constraints between pairs of coordinates; this guess is UNVERIFIED. | https://www.researchgate.net/publication/220188139 ; LNCS 2450 | MED |
| Monograph ch. 10 "Kászonyi–Katsura Theory" (p. 309): §10.1 DLI Languages; §10.2 Boxes and Differences (p. 320); §10.3 Q∩(ab*)^n with Some Restrictions on the Prime Divisors of n; §10.4 Semiboxes; §10.5 (two primes, title inferred); §10.6 Three Prime Divisors (p. 332); §10.7 Some Non-Context-Free and Context-Free Languages (p. 339); §10.8 Primitive Words and Disjunctive Languages (p. 340). Ch. 9 "Primitive Words in Languages" (p. 267); ch. 11 "Derivating Primitive Words" (p. 343, includes slender languages and small CFGs); ch. 13 "Context-Free Languages and Non-primitive Words"; §4.3 Dömösi–Ito–Katsura–Nehaniv Lemma (p. 98). | B&N / World Scientific table of contents | MED |
| **Arbitrary bounded languages Q ∩ w1*…wk*:** no general result found. Deciding stratifiability of a semilinear set is **Ginsburg's 1966 open problem**. Ibarra–Seki, TCS 2013, give partial results. It is coNP-complete for semilinear sets given as systems of linear inequalities (Leroux–Penelle–Sutre, ATVA 2014, LNCS 8837). An unverified preprint, arXiv:2610.27482, claims undecidability for given semilinear sets. E(Q_n) is a *union* of polyhedral cells, so LPS does not apply directly. | https://www.sciencedirect.com/science/article/pii/S0304397513005410 ; https://link.springer.com/chapter/10.1007/978-3-319-11936-6_19 | MED |

**Consequence for the team.**
- If KK fails for even one n, Q is not CF, since Q_n = Q ∩ regular.
- The experts conjecture KK is true and have proved it for n with at most 3 distinct prime factors. A disproof at n = 210 would therefore be a surprise.
- If KK is true, the (ab*)^n route is closed. The real problem then sits in the *uniformity over n* (see F2 in §5).

---

## 3. Iteration conditions that Q SATISFIES (barriers)

Standard statements, written from memory and cross-checked against the snippets. Throughout, L is a CFL with constant p.

- **Bar-Hillel.** Every z ∈ L with |z| ≥ p has z = uvwxy with |vwx| ≤ p, |vx| ≥ 1, and uv^iwx^iy ∈ L for all i ≥ 0.
- **Ogden.** If ≥ p positions of z are marked, then vx contains a marked position, vwx contains ≤ p marked positions, and pumping holds.
- **Bader–Moura** (JACM 29(2) (1982) 404–407). Suppose z has d distinguished and e excluded positions with d > p^{e+1}. Then:
  - vx contains ≥ 1 distinguished position and no excluded position;
  - if vwx contains r distinguished and s excluded positions, then r ≤ p^{s+1};
  - pumping holds for all i ≥ 0.
- **Interchange lemma** (Ogden–Ross–Winklmann, SIAM J. Comput. 14 (1985) 410–415). There is c such that for every n ≥ 2, every R ⊆ L ∩ Σ^n and every 2 ≤ m ≤ n, there is Z ⊆ R with |Z| ≥ |R|/(c n^2) and decompositions z_k = w_k x_k y_k such that:
  - all |w_k| are equal, all |y_k| are equal, and m ≥ |x_k| > m/2;
  - w_j x_k y_j ∈ L for all j, k.

| Claim | Source | Conf. |
|---|---|---|
| Q satisfies "the nonempty, strong variant of Bader and Moura's iteration condition". The abstract explains "strong": originally Bader and Moura defined a weaker condition. Since this is at least as strong as Bader–Moura, **Q satisfies Bader–Moura, hence Ogden's lemma (take e = 0), hence Bar-Hillel.** | DHIKK FCT'93, https://link.springer.com/chapter/10.1007/3-540-57163-9_15 | HIGH for the abstract; the exact quantifiers of "nonempty strong" were not verified |
| Q "is not linear context-free, not unambiguous, but fulfills all pumping lemmata and the interchange lemma". | Univ. Hamburg TGI project page "Structures of Formal Languages", https://www2.informatik.uni-hamburg.de/tgi/forschung/projekte/struktur_eng.html ; S. Horváth, M. Kudlek, "Primitive Words are Strongly Interchangeable but Nonlinear", FBI-Bericht 183/96 (Hamburg 1996); S. Horváth, "Strong interchangeability and nonlinearity of primitive words", Proc. AMiLP'95, Univ. Twente (1995) 173–178 | MED-HIGH |
| CoWiki (Shallit): "almost certainly the answer is no, but no one knows how to prove this"; the standard tools (pumping lemma, Ogden's lemma, interchange lemma) "do not work for this language". | https://cs.uwaterloo.ca/twiki/view/CoWiki/PrimitiveWordsContextFree (via search snippet) | MED |
| Sokolowski / Grant conditions: Hewett–Slutzki (Math. Systems Theory 21 (1988/89) 223–233) show the generalized Ogden (Bader–Moura) condition is stronger than Grant's extended Sokolowski condition. So Q satisfies Grant and Sokolowski *if* "stronger" means implication of conditions. | https://link.springer.com/article/10.1007/BF02088014 | LOW-MED |
| Parikh's condition (Ilie, TCS 202 (1998) 231–244) is orthogonal to all of the above. Its status for Q is **unknown** (not found). | https://www.sciencedirect.com/science/article/pii/S0304397597002624 | — |

**Barrier for "fooling sets" (PROVED from the interchange lemma for Q).**
- Call F ⊆ Q ∩ Σ^n a fooling set at scale m if, for any two distinct members and any aligned split with middle length in (m/2, m], some swap leaves Q.
- Interchange gives |F| < 2c n^2.
- So no superpolynomial (indeed, no ω(n^2)) fooling set exists.
- The coordinator's rectangle idea can only survive in its *fractional/distributional* form, which the interchange lemma does not cover.

---

## 4. Known negative results and subclass results

| Claim | Source | Conf. |
|---|---|---|
| Q is not regular; two simple proofs in Dömösi–Horváth, Bull. EATCS 87 (2005). | search snippets | HIGH |
| Q is not DCF: co-Q ∩ a⁺b⁺a⁺b⁺ = {a^i b^j a^i b^j} is not CF, and DCFL is closed under complement. | folklore (Lischke survey arXiv:1104.4427 §3) | HIGH |
| **Q is not linear**: Horváth (AMiLP'95), via a pumping lemma for linear languages (Lischke survey, Thm 24: "Q is not a linear language"). | https://arxiv.org/abs/1104.4427 | HIGH |
| **Q is not unambiguous CF**: H. Petersen, "The ambiguity of primitive words", STACS'94, LNCS 775, 679–690; journal version "On the language of primitive words", TCS 161 (1996) 141–156. The same holds for Lyndon words. Q and the Lyndon words are accepted by 2DPDAs and by constant-depth poly-size circuits. Koechlin (FSTTCS 2022, Prop. 17) gives a new proof. | https://link.springer.com/chapter/10.1007/3-540-57785-8_181 ; https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.FSTTCS.2022.41 | HIGH |
| Generating-function strength (PROVED here). Over {a,b}, Σ_n ψ(n) z^n = Σ_{d ≥ 1} μ(d)·2z^d/(1−2z^d). For squarefree d, the term d alone has simple poles at all z with z^d = 1/2 that are primitive under rotation; no other term has a pole there, because \|z^{d'}\| = 1/2 forces d' = d. So the meromorphic continuation to \|z\|<1 has **infinitely many poles**. The series is therefore not D-finite (holonomic), not just non-algebraic. Any formalism with D-finite counting series excludes Q. **This method says nothing about ambiguous CFLs.** | — | PROVED |
| **Slender intersections:** for slender regular (resp. CF) L, Q ∩ L is regular (resp. CF), and the non-primitive part of a slender CFL is CF. The briefing attributes this to "Horváth–Ito", but the source found is **Dömösi, Martín-Vide, Mitrana**, "Remarks on sublanguages consisting of primitive words of slender regular and context-free languages", Theory Is Forever, LNCS 3113 (2004) 60–67. | https://link.springer.com/chapter/10.1007/978-3-540-27812-2_6 | HIGH |
| Horváth–Ito, "Decidable and undecidable problems of primitive words, regular and context-free languages", J.UCS 5(9) (1999) 532–541: decidability of root/degree properties, e.g. whether root(L(G)) is regular. It is undecidable whether a CFG generates only, or all, primitive words (Hamburg page). | https://www.jucs.org/jucs_5_9/decidable_and_undecidable_problems/Horv_th_S.pdf | MED |
| Ito–Katsura, "Context-free languages consisting of non-primitive words", IJCM 40 (1991) 157–167: structure theorem for CFLs containing no primitive words. | https://www.tandfonline.com/doi/abs/10.1080/00207169108804010 | MED |
| Leupold, LATA 2010 (LNCS 6031, 403–413): Q is (strongly) unavoidable for non-linear CFLs, i.e. every non-linear CFL contains (infinitely many) primitive words. Extended in JALC 26 (2021) 91–107. | https://link.springer.com/chapter/10.1007/978-3-642-13089-2_34 | HIGH |
| Related languages proved non-CF, all by intersecting with a regular set and then pumping/Ogden: Lyndon words (Berstel–Boasson, Bull. EATCS 63 (1997) 139–140); abelian-primitive words (Domaratzki–Rampersad, arXiv:1006.4104); non-ins-robust primitive words (Srivastava–Kapoor, arXiv:1707.01010); unbordered words (Rampersad–Shallit–Wang, arXiv:1008.2440). Q = Cyc(Lyndon) and CFLs are closed under cyclic shift, so Lyndon CF ⇒ Q CF; the known implication runs the wrong way for us. | arXiv | HIGH |
| **Measure/density:** Sin'ya, "Asymptotic approximation by regular languages", SOFSEM 2021, LNCS 12607 (arXiv:2008.01413). Every regular language of positive density contains infinitely many non-primitive words; in fact there are z and p with z^{pn+1} ∈ R for all n. Hence Q is "REG-immeasurable in a strong sense". Koga, "Dense languages and non primitive words", Acta Cybernetica 25 (2022) 717–731: dense regular languages contain infinitely many non-primitive words, plus a generalization to a class Γ(TL) of dense languages (definition not retrieved). | https://arxiv.org/abs/2008.01413 ; https://cyber.bibl.u-szeged.hu/index.php/actcybern/article/view/4253 | HIGH |
| Amarilli–Monet–Raphaël–Salvati (STACS 2026): Q's probabilistic membership is tractable via circuits **with complementation**. They state they **do not know whether Q is poly-slicewise-unambiguous** (poly-size unambiguous CFGs per length), nor whether it has tractable circuits without complementation. | https://arxiv.org/abs/2510.08127 | HIGH |
| Not found anywhere: Q not finitely ambiguous; not one-counter; not metalinear or finite-index; not "poly-slicewise-unambiguous". All appear OPEN, and each would be a publishable intermediate step. | — | MED (absence of evidence) |

---

## 5. Equivalent reformulations and reductions

**F1 (PROVED; CHECKED BY COMPUTER in `scripts/scout/check_unv.py` [3]).** For every k ≥ 2: Q_k is CF ⟺ Q_2 is CF.
- Let h(c_i) = a b^i, an injective morphism.
- If h(w) = u^p with p ≥ 2, then u begins with a. By the exponent-set argument of §2, w = (c_{i1}…c_{i_{n/p}})^p.
- So h(w) is primitive ⟺ w is primitive, and Q_k = h^{-1}(Q_2). CFLs are closed under inverse morphisms.
- Conversely, Q_2 = Q_k ∩ {c1,c2}*.

**F2 (PROVED; CHECKED to length 14, `check_unv.py` [4]).** Q is CF ⟺ Q ∩ a{a,b}* is CF ⟺ Q ∩ (ab*)^+ = ⋃_{n≥1} Q_n is CF.
- Conjugates of primitive words are primitive.
- Every primitive word other than b contains an a, so it has a conjugate starting with a.
- Hence Q = Cyc(Q ∩ a{a,b}*) ∪ {b}. CFLs are closed under cyclic shift (Maslov 1973; Oshiba 1972; Hopcroft–Ullman exercise).
- Note a{a,b}* = (ab*)^+.

**Moral:** the conjecture says the infinite union ⋃_n Q_n is not CF, while KK says each Q_n is. **Any proof must exploit non-uniformity in n**: the factorization of the number of a's or the length.

**F3 (PROVED, standard Bar-Hillel product).** If Q has a CNF grammar of size g, then:
- Q ∩ Σ^n and Q_n have CFGs of size O(g n^3);
- each slice is a union of at most g·n^2 balanced rectangles inside Q.

So a superpolynomial lower bound on the CFG size of Q ∩ Σ^n, or of Q_n, would prove the conjecture. That is sufficient, not equivalent.

**F4 (PROVED).** Q ∩ Σ^n has an NFA with ≤ (n+1)(2n+2)^{ω(n)} states, i.e. n^{O(log n/log log n)} (quasi-polynomial).
- w is primitive ⟺ for every prime p | n there is i with w_i ≠ w_{i+n/p}.
- The NFA guesses one witness per prime and stores (position, letter) for each.

Consequences: slice lower bounds can be at most quasi-polynomial, and for n with bounded ω(n) the slices have poly-size NFAs. Hard lengths must have many distinct prime factors. This parallels §2, where KK is proved exactly for n with ≤ 3 primes.

**F5 (CONJECTURED; CHECKED BY COMPUTER).** Scripts: `scripts/scout/laminar_witness.py`, `laminar_sample.py`, `laminar_lowweight.py`.
- A *p-witness* is a pair (i, i + j·n/p) with 1 ≤ j < p and w_i ≠ w_{i+jn/p}.
- **Conjecture:** every primitive w ∈ {a,b}^n has one p-witness for each prime p | n, with no two pairs strictly crossing (a < c < b < d). Shared endpoints are allowed.
- Evidence, all with 0 failures:
  - exhaustive over all words for n ∈ {6, 12, 18};
  - all words with ≤ 6 (n=30), ≤ 5 (n=42), ≤ 4 (n=60), ≤ 3 (n=210) letters b;
  - 20000 random hard-count and near-periodic samples each for n ∈ {30, 42, 60, 66, 70, 90, 105, 210}.
- With j = 1 only, the statement is **false**: n=6, w=bbabaa (2/54 words at n=6; 20/4020 at n=12; 92 low-weight words at n=30).
- If the conjecture holds, a routine laminar-family grammar (sketch, NOT written out) gives Q ∩ Σ^n a CFG with n^{2+o(1)} productions. The nonterminals are (length, subset of primes, boundary letters), and 2^{ω(n)} = n^{o(1)}.
- Then slice-wise "size" lower bounds are hopeless. The only slice approach left needs **ω(n^2) rectangles vs the O(n^2) forced by a fixed grammar**: a delicate polynomial-scale discrepancy bound.

**F6 (FROM LITERATURE + PROVED).** Q = Cyc(Lyndon words). Lyndon not CF is known, but it does not transfer to Q.

**Sufficient strengthening (Sin'ya's "quantitative approach").** The statement "every CFL of positive upper density contains a non-primitive word" implies the conjecture, because Q has density 1 and contains no non-primitive word.
- Known for regular languages (Sin'ya 2021).
- Known for some dense classes (Koga 2022).
- Open for CFLs. No result even for unambiguous or linear CFLs was found.

**F7 (Shyr–Yu type facts, CHECKED BY COMPUTER, `check_unv.py` [1],[2]).**
- For uv ≠ vu, |u|,|v| ≤ 6, n ≤ 12: at most **one** n ≥ 1 makes u^n v non-primitive, and that n can be 1, 2, 3 or 4. Example: a²·baab = (aab)².
- For primitive p ≠ q (≤ 5 letters, exponents ≤ 8): p^i q^j is non-primitive for at most one (i,j). This matches Shyr–Yu, Soochow J. Math. 20(4) (1994), "p⁺q⁺ contains at most one non-primitive word". See also "On the Shyr–Yu theorem", TCS 2009, https://www.sciencedirect.com/science/article/pii/S0304397509004265.

---

## 6. What has been tried and why it fails

1. **Pumping, Ogden, Bader–Moura, interchange.** All are satisfied by Q (§3).
   - Reason: the non-primitive words are exponentially rare (≤ ω(n)·2^{n/2} of 2^n), and pumping a factor can create a power for at most one exponent (Shyr–Yu, F7). So a good factor to pump can always be chosen.
   - Any fooling-set argument is capped at O(n^2) (§3).
2. **Intersect with a regular set, then use Ginsburg/Parikh on a bounded language.**
   - Slender regular/CF intersections stay regular/CF (DMM 2004).
   - (ab*)^n and (a⁺b⁺)^n intersections are CF for n with ≤ 3 prime factors, and conjecturally for all n (KK).
   - Parikh images carry no information: primitivity is not commutative, and almost every Parikh vector has primitive representatives.
   - This route works for the Lyndon, abelian-primitive, unbordered and non-ins-robust languages because those have "local" crossing constraints. Q does not.
3. **Analytic/generating functions.** These settle unambiguity (Petersen) and even exclude D-finite classes (§4), but say nothing about ambiguous grammars.
4. **Density/measure (Sin'ya).** Q is REG-immeasurable. Extending "positive density ⇒ contains a power" from REG to CFL is open, and is a stronger statement than the conjecture.
5. **Complexity.** Q is in AC^0 and is accepted by a 2DPDA (Petersen), so complexity-class separations cannot help.
6. **Slice size / communication-style rectangles (coordinator's idea).**
   - The NFA bound is quasi-polynomial (F4), and conjecturally CFGs are polynomial (F5).
   - Exponential CFG lower bounds of Filmus type (Filmus, IPL 111 (2011) 895–898: permutations, squares {ww} of a given length) do not transfer.
   - Only an ω(n^2)-vs-O(n^2) rectangle-count separation remains.
   - Note the open question of Amarilli et al. on poly-slicewise-unambiguity of Q.

Leupold's 2013 Theorietag abstract was not fetchable. The talk "Primitive Words are Unavoidable" (slides at eiche.theoinf.tu-ilmenau.de/kuske/Theorietag2013/Folien/Fr-2-3-Leupold.pdf) presents the LATA 2010 unavoidability results. The CoWiki and Sin'ya PDFs were also not fetchable (network policy).

---

## Most promising concrete open sub-questions

1. **KK at n = 210 (or the first n with 4 distinct primes).** Is E(Q_210) stratified semilinear?
   - "No" ⇒ Q is not CF, immediately.
   - The experts expect "yes", so this is a long shot.
   - It is checkable in principle via Kászonyi's DLI pumping lemma, which is a necessary and sufficient condition.
2. **A uniformity argument for ⋃_n Q_n (F2).** Show that no single grammar handles all prime-factor patterns of n. Concretely, a lower bound on the CFG size of Q_n that is superpolynomial in n (F3) would do it.
3. **Intermediate classes.** Prove Q is not finitely ambiguous / one-counter / metalinear / poly-slicewise-unambiguous.
4. **Density.** Prove that every CFL (or every unambiguous or linear CFL) of positive density contains a non-primitive word.
5. **Settle F5.** If true, it kills slice-size lower bounds. If false, the counterexamples are exactly the structured "hard words" a rectangle argument needs.
