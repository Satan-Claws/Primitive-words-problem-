# Primitive-word ambiguity: historical literature and manuscript positioning

## What is established, and is the proposed theorem already known?

### Takeaway
The verified literature establishes non-unambiguity of primitive words, not the proposed exclusion of every fixed finite ambiguity bound. This search found no existing statement of the latter theorem; this is evidence for positioning, not a certification of novelty.

### Cited Findings
- Holger Petersen (not Peterson), *The ambiguity of primitive words*, STACS 1994, LNCS 775, pp. 679–690, DOI 10.1007/3-540-57785-8_181, proves that primitive words and Lyndon words are not unambiguous context-free languages. The publisher abstract also discusses two-way deterministic pushdown recognition and related complexity results. Classification: same problem, different technique. [Publisher](https://link.springer.com/chapter/10.1007/3-540-57785-8_181)
- Petersen's journal version is *On the language of primitive words*, Theoretical Computer Science 161(1–2):141–156 (1996), DOI 10.1016/0304-3975(95)00098-4. The publisher expressly identifies STACS 1994 as its preliminary version. It is therefore misleading to describe the 1996 article as an independent subsequent proof. Classification: same problem, different technique. [Publisher](https://www.sciencedirect.com/science/article/pii/0304397595000984)
- Gerhard Lischke, *Primitive words and roots of words*, Acta Universitatis Sapientiae, Informatica 3(1):5–34 (2011), arXiv:1104.4427, gives a survey. Theorem 22 attributes non-unambiguity to Petersen; Theorem 24 attributes nonlinearity to Horváth. Classification: background. [Full text](https://arxiv.org/pdf/1104.4427)
- Pál Dömösi and Masami Ito, *Context-Free Languages and Primitive Words*, World Scientific (2014), has separate chapters on bounded languages, primitive-language properties, and Kászonyi–Katsura theory. Only catalogue/preview material was accessible; no claim here depends on an unseen theorem in this book. [Book preview](https://books.google.com/books?id=0Ba3CgAAQBAJ)
- The earlier Dömösi–Horváth–Ito work is *Formal languages and primitive words*, Publicationes Mathematicae Debrecen 42(3–4):315–321 (1993). Dömösi, Horváth, Ito, Kászonyi, and Katsura published *Formal languages consisting of primitive words*, FCT 1993, LNCS 710, pp.194–203. These bibliographic facts are confirmed by Petersen's publisher bibliography. [Petersen bibliography](https://link.springer.com/chapter/10.1007/3-540-57785-8_181)
- Dömösi's own 2011 talk abstract explains that the conjecture was posed in 1991, that primitive words satisfy strong iteration/interchange tests, and that various regular intersections are context-free. This supports explaining why the present argument proves increasing ambiguity of regular slices rather than trying to make one slice non-context-free. [Author abstract](https://www.fit.vut.cz/person/meduna/public/work/lib/exe/fetch.php?media=talks%3Aseminar%3A2011-07-07_domosi_talk_abstract.pdf)
- Antoine Amarilli, Mikaël Monet, Paul Raphaël, and Sylvain Salvati, *On the Complexity of Language Membership for Probabilistic Words*, STACS 2026, DOI 10.4230/LIPIcs.STACS.2026.5, still explicitly states that the CFL status of primitive words is unknown, while non-uCFL and non-linear-CFL status are known. Its new result concerns tractable probabilistic membership, not ambiguity lower bounds. Classification: same problem area, different question. [Full text](https://drops.dagstuhl.de/storage/00lipics/lipics-vol364-stacs2026/html/LIPIcs.STACS.2026.5/LIPIcs.STACS.2026.5.html)
- Alin Bostan, Arnaud Carayol, Florent Koechlin, and Cyril Nicaud, *Weakly-unambiguous Parikh automata and their link to holonomic series*, arXiv:2512.09823 (submitted 10 December 2025), studies weak unambiguity for Parikh automata. The accessible HTML contains no occurrence of “primitive.” Classification: background/adjacent techniques, not a directly competing primitive-word theorem. [Metadata](https://arxiv.org/abs/2512.09823), [Full text](https://arxiv.org/html/2512.09823v1)

### Inferences
- State the new theorem as “For every finite alphabet with at least two letters, its primitive words admit no context-free grammar with uniformly bounded ambiguity.” Equivalently, *if* this language is context-free, every grammar for it has unbounded ambiguity. Do not imply that its context-freeness has been disproved.
- The main historical comparison should be Petersen 1994/1996 → Koechlin 2022 → the proposed quantitative obstruction. Do not claim every subsequent paper worked toward finite ambiguity.

### Gaps
- Petersen's full 1994 and 1996 bodies were not retrieved; abstract, reference list, bibliographic metadata, and later descriptions were checked. Accordingly, a line-by-line claim of following Petersen's proof style would be unjustified.
- The full Dömösi–Ito monograph was not available. A final submission literature check should inspect its chapters 6, 8, and 10 and seek expert feedback.

## Which structural results are already known, and what is the exact comparison with Koechlin?

### Takeaway
The finite-ambiguity semilinear-cover criterion is established background. Keep the repository's self-contained structural proof if needed, but do not present the existence of such a cover as new.

### Cited Findings
- Seymour Ginsburg and Joseph S. Ullian, *Ambiguity in context free languages*, Journal of the ACM 13(1):62–89 (1966), DOI **10.1145/321312.321318**. The repository NOVELTY.md gives a different, incorrect DOI: 10.1145/321356.321366 belongs to Hibbard–Ullian's *The independence of inherent ambiguity from complementedness among context-free languages*. [JACM bibliography](https://projects.csail.mit.edu/jacm/References/ginsburgu1966%3A62.html), [DOI](https://doi.org/10.1145/321312.321318)
- Arnold L. Rosenberg, *A Note on Ambiguity of Context-Free Languages and Presentations of Semilinear Sets*, JACM 17(1):44–50 (1970), DOI 10.1145/321556.321561. Classification: background for finite-ambiguity covers. [Verified metadata](https://dblp1.uni-trier.de/rec/journals/jacm/Rosenberg70.html)
- Florent Koechlin, *New Analytic Techniques for Proving the Inherent Ambiguity of Context-Free Languages*, FSTTCS 2022, LIPIcs 250, 41:1–41:22, DOI 10.4230/LIPIcs.FSTTCS.2022.41. Proposition 17 reproves Petersen using the slice `a*b a*b a*b`, whose exponent condition is `n != m or m != p`. Theorem 21 treats interlacing but only excludes unambiguity. Its conclusion, p.41:16, states the finite-k characterization: a bounded CFL admits a k-ambiguous grammar iff its associated semilinear set is a finite union of stratified linear sets, each with linearly independent periods, with every intersection of more than k distinct members empty. It cites Ginsburg–Ullian and Rosenberg. The conclusion presents growing-degree lower bounds by generating series as future work. Classification: closest technique/background and same-problem predecessor. [Final publisher PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol250-fsttcs2022/LIPIcs.FSTTCS.2022.41/LIPIcs.FSTTCS.2022.41.pdf)

### Inferences
- The local proof's potentially new content is its scalable two-marker primitive-word slice, rank obstruction for noncrossing positive periods spanning the diagonal, and reduction of local cover multiplicity to a family of strict half-spaces. No corresponding quantitative theorem was found in the inspected sources.
- Repeated marker letters require care when importing a theorem about exponent presentations. A safe direct route is the repository's annotated-grammar argument. A safe alternative is to lift to a letter-bounded language with a distinct letter for each variable block, using an inverse letter homomorphism and intersection with the positional regular pattern; each word in the slice has exactly one positional lift, so tree counts can be preserved. Then apply the letter-bounded finite-k criterion. Fixed marker coordinates can be discarded only after checking their periods vanish.
- Merely saying “by Parikh's theorem” is insufficient: ordinary semilinearity does not provide stratification, independent periods, or bounded overlap. These are precisely the required interfaces.
- The established cover criterion only needs an overlap bound, whereas the local structure lemma claims equality with the grammar's precise tree-count function. Preserve that distinction when describing the stronger local representation.

### Gaps
- The original Ginsburg–Ullian and Rosenberg full papers were not accessible. The finite-k statement is verified through Koechlin's published full text, not their original theorem numbers. Do not invent those numbers.

## What exposition should the manuscript follow?

### Takeaway
Use a conventional formal-language theory presentation: explicit definitions, an early precise theorem, a sequence of short structural and geometric lemmas, and a final reduction back to primitive words. Separate verified historical comparison from stylistic inference.

### Cited Findings
- Petersen's abstract begins with the elementary definition of primitivity, states the impossibility theorem directly, and identifies the earlier deterministic bound it strengthens. [Publisher abstract](https://link.springer.com/chapter/10.1007/3-540-57785-8_181)
- Koechlin separates motivation, contributions, related work, preliminaries, general criteria, examples, and open questions; propositions clearly distinguish new arguments from named earlier results. [Full text](https://drops.dagstuhl.de/storage/00lipics/lipics-vol250-fsttcs2022/LIPIcs.FSTTCS.2022.41/LIPIcs.FSTTCS.2022.41.pdf)

### Inferences
- Recommended proof pipeline (our reconstruction): primitive-word regular slice → bounded multiplicity stratified cover → noncrossing rank lemma → half-space overlap lower bound → contradiction for arbitrary k.
- Give each interface before its proof: the slice produces off-diagonal exponent pairs; the cover lemma produces independent noncrossing periods and controlled overlap; the geometric theorem forces overlap at least ceil((M+1)/2). This makes the classical component independently replaceable by a citation.
- Define “finite ambiguity” as a uniform global bound; do not confuse it with finitely many parse trees for each individual word.
- Put the sharp quantitative slice statement in the introduction. State separately which parts are classical, which are proved for self-containment, and which are the claimed contribution. Acknowledge that no grammar construction or context-freeness resolution follows.
- Avoid reproducing informal audit language (“PROVED”, “CORRECT WITH FIXES”) in the manuscript. Replace it with ordinary mathematical statements and proof obligations; keep audit records in the reproducibility supplement.

### Gaps
- Exact Petersen proof prose and section organization remain uninspected. The stylistic recommendation is based on its verified abstract and accessible later literature, not a claimed full-text reading.
- Focused follow-up access attempts (19 November 2026): the [Springer chapter PDF](https://link.springer.com/content/pdf/10.1007/3-540-57785-8_181.pdf), [Springer preview](https://page-one.springer.com/pdf/preview/10.1007/3-540-57785-8_181), and [Elsevier PDF endpoint](https://www.sciencedirect.com/science/article/pii/0304397595000984/pdf) could not be fetched by the web tool. Author-name and Stuttgart institutional-repository searches did not locate an author-hosted version. [ResearchGate's chapter record](https://www.researchgate.net/publication/220995281_The_ambiguity_of_primitive_words) offers a request-full-text action, not an accessible uploaded manuscript; no request was sent. The accessible [Srivastava thesis, Robustness of Primitive and L-Primitive Words](https://www.iitg.ac.in/cseweb/thesis/MzQ0MzQwNDQGAA==) cites Petersen, but its extracted text has no “unambiguous” match, so it did not supply a replacement proof. These attempts do not change the full-text limitation.
