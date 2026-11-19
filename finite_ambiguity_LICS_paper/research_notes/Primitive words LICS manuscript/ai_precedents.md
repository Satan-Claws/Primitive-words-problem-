# AI-assisted theorem precedents and LICS 2027 requirements

Research date: 19 November 2026. This is a scoped search, not an exhaustive census. Disclosures below are authors' accounts, not independent verification of the mathematics.

## What do recent theory papers disclose about AI-assisted discovery?

### Takeaway
Two concrete recent theory manuscripts disclose AI-generated proofs prominently, but both are **STOC 2027 submissions, not accepted STOC papers** as of the research date. No qualifying accepted ICALP or LICS paper was verified in this search; neither AI-themed papers nor papers merely citing ICALP/STOC qualify as evidence of AI-assisted theorem discovery.

### Cited Findings
- Nima Anari and Farzam Ebrahimnejad, *Optimal e^{(gamma+o(1))n}-Approximation of the Permanent of Positive Semidefinite Matrices*, arXiv:2605.21946v1, 21 May 2026. Full-text abstract, introduction's Provenance paragraph, and Appendix A disclose GPT 5.5 Pro Extended. The first author supplied prior work and a target approximation; no mathematical hints or follow-up preceded the result. The second independently used about thirty exchanges and high-level guidance. Both checked the mathematics; Codex assembled/typeset the paper. Appendix A gives a narrative, **not verbatim prompts or a transcript**. The paper is organized as an ordinary theorem paper: introduction, related work, preliminaries, relaxation, guarantee, computation, discussion, provenance appendix. [Primary full text, especially Appendix A](https://arxiv.org/html/2605.21946v1).
- Anari–Ebrahimnejad is publicly listed as submission #530. This establishes submission, not acceptance. [Official STOC 2027 submission index](https://sigact-stoc.github.io/stoc2027/). STOC notification is 1 February 2027, so acceptance cannot be claimed as of 19 November 2026. [Official conference site](https://acm-stoc.org/stoc2027/).
- Maxime Flin, Mohsen Ghaffari, Magnús M. Halldórsson, Yannic Maus, Alexandre Nolin, *LOCAL LLL in poly(log log n) Rounds*, arXiv:2610.17133v1, 12 October 2026. A clearly labeled AI Statement immediately after the mathematical abstract credits GPT-6 Astra, GPT-6.1 Sol and Opus 5.5 with proving the result with essentially no human advice. Authors say they nearly completely rewrote the exposition, used further AI review/copyediting, and accept responsibility. The inspected HTML contains no exact prompts, chat logs, iteration counts, or formal proof artifact. Its body follows introduction, preliminaries, proof outline and proof, context/applications, references, appendix. [Primary full text](https://arxiv.org/html/2610.17133v1). Listed as STOC 2027 submission #475 in the [official submission index](https://sigact-stoc.github.io/stoc2027/).
- A genuinely published adjacent precedent is Bernardino Romera-Paredes et al., *Mathematical discoveries from program search with large language models*, Nature 625, 468–475 (2024), DOI 10.1038/s41586-023-06924-6, published online 14 December 2023. FunSearch combines an LLM, evolutionary program search, and an evaluator; it discovers improved cap-set constructions and bin-packing heuristics. Figures and supplementary material describe program skeletons, prompting/search mechanics, and discovered code. This is new mathematical construction discovery, not a free-form LLM proof of a general theorem and not a LICS/ICALP/STOC precedent. [Publisher paper](https://www.nature.com/articles/s41586-023-06924-6).

### Inferences
- The two directly relevant theory preprints show that a concise narrative of model, mathematical contribution, human guidance, and verification can accompany a conventional mathematical paper. Neither supplies every historical prompt in its inspected version. This is a statement about those examples, not a universal venue norm.
- For this project, keep the mathematical exposition self-contained and place a factual AI-use section before references, optionally with a provenance/artifact appendix. Exact prompts are useful supporting evidence when genuinely saved, but must not be reconstructed and called historical transcripts.

### Gaps
- The search did not verify an accepted ICALP/LICS/STOC theorem-discovery example. Report that limitation candidly; do not turn the STOC 2027 submissions into accepted papers. Web searches for these venues repeatedly returned AI research subjects, AI lab affiliations, and later preprints citing venue papers.
- The two STOC submission PDFs hosted on GitHub releases could not be fetched through the web tool; the complete arXiv HTML versions above were accessible. Consequently, descriptions refer to the identified arXiv v1 versions, not an asserted byte-identical submission PDF.
- No exact chat transcript was verified for these two cases. No claim is made that their mathematics has been independently audited in this task.

## What format and AI disclosure does current LICS require?

### Takeaway
Target LICS 2027, using LIPIcs rather than the earlier ACM SIGCONF submission format. The 2027 call explicitly requires substantive AI use to be disclosed in a well-marked heading at the end, before references.

### Cited Findings
- LICS 2027: Montréal, 21–24 June 2027; title/abstract deadline 14 January, paper deadline 21 January 2027 (AoE). Submission format is LIPIcs, maximum 22 pages excluding references; an appendix may be read at reviewers' discretion. Single-blind means names are included. The submitted version must appear on arXiv within one week of deadline. The opening should state problem, results, significance, related work and main ideas accessibly. [Official CFP](https://lics.siglog.org/lics27/cfp.php).
- That CFP permits LLM use and requires disclosure of substantive text, proof, code or idea generation; minor grammar/clarity edits to the authors' text are exempt. Its specified location is a well-marked end-of-paper heading before references. It does **not** explicitly demand exact prompts, full transcripts, token counts, or every iteration. [Official CFP, policy point 5](https://lics.siglog.org/lics27/cfp.php).
- LICS 2026 had required ACM SIGCONF for submission and subsequently announced LIPIcs for camera-ready. It is therefore inappropriate to reuse the 2026 submission format for the 2027 target. [2026 CFP](https://lics.siglog.org/lics26/cfp.php).
- Publisher author kit: `lipics-v2021.cls`, package tag v2021.1.3. Use the publisher's class and sample, not a manually imitated layout. [Official tagged author kit](https://github.com/dagstuhl-publishing/styles/tree/v2021.1.3/LIPIcs/authors); [publisher series/author instructions](https://www.dagstuhl.de/publishing/series/details/lipics).
- Dagstuhl requires type/purpose of substantive use and extent of human review/editorial control. Naming tool/version/date/free-or-paid status is optional under its general policy. Human authors retain responsibility and GenAI cannot be an author. The policy distinguishes reference formatting from impermissible reference generation; all citations must be verified against actual sources. [Publisher GenAI policy, sections 1–4](https://drops.dagstuhl.de/docs/gen-ai).

### Inferences
- Recommended LaTeX: `\documentclass[a4paper,UKenglish,cleveref,autoref]{lipics-v2021}` (omit anonymous). Use the official sample's bibliography conventions and leave unknown author identity/affiliation visibly unresolved rather than inventing them.
- Recommended heading: `\section*{Use of generative AI}` immediately before references. Include models/dates only if evidenced. An appendix can enumerate saved reports, actual prompts and proof-verification artifacts without making historical claims beyond the records.
- Human review and author responsibility are substantive author attestations: a drafting assistant must not assert that the human author already independently checked every lemma merely because AI audits exist.

### Gaps
- Author names, affiliations, ORCIDs, funding, review history and final artifact URL are not established by this research. Those are final author inputs, not reasons to delay a clearly labeled draft.

## What AI-process evidence does this repository actually preserve?

### Takeaway
The repository explicitly preserves reports but not agent transcripts. Its saved infinite-ambiguity prompt concerns a later, different campaign and must not be presented as the original finite-ambiguity discovery prompt.

### Cited Findings
- Root README states that agent transcripts were not saved, while agent reports were. It distinguishes the open context-free campaign from the finite-ambiguity result and links written proof, audits and Lean development. [Local README](../../../README.md).
- The saved `infinite-ambiguity-prompt.txt` already treats the no-finitely-ambiguous-CFG theorem as established and asks for work on infinitely ambiguous grammars. It prescribes parallel exploration and adversarial audits, but prescriptions do not prove that every step was executed. [Actual saved prompt](../../../infinite-ambiguity/codex_2026-11-17_to_11-18/infinite-ambiguity-prompt.txt).
- Available finite-ambiguity artifacts include `PROOF.md`, `INTUITIVE_PROOF.md`, `AUDIT_geometry.md`, `AUDIT_structure.md`, `NOVELTY.md`, `LEAN_BRIEF.md`, experimental scripts/output, and a Lean directory with toolchain/manifest. [Finite-ambiguity proof](../../../finitely-ambiguous/PROOF.md); [formalization README](../../../finitely-ambiguous/lean/README.md).

### Inferences
- Safe provisional disclosure: the development used AI assistance for mathematical exploration, drafting/auditing and formalization **to the extent confirmed by the artifact audit**; saved reports and formal source are available, complete agent transcripts are not. The final authors must supply or confirm exact model identities, dates, human mathematical contributions, and scope of independent review.
- Do not claim a one-shot proof, a specific model, exact interaction count, a fully autonomous discovery, or a complete reproducible chat history without additional evidence.
- Distinguish an AI adversarial review from human verification and distinguish Lean's checked theorem (including its definitions and assumptions) from claims of publication novelty. The proof-audit task must establish the exact formalization boundary.

### Gaps
- No complete original finite-ambiguity prompt/chat history was found in the filenames inspected. Saved later prompts cannot reconstruct that missing record.
- Bibliographic entries for the two theory examples should be `@misc`/arXiv preprints with their actual authors, titles and IDs, not `@inproceedings` entries inventing STOC 2027 acceptance. The Nature example can be an article; it is supporting methodology context, not necessary mathematical related work for primitive words.

### Author clarification received during drafting
- The user reports using **Claude Opus 5.5 in medium mode**. An initial one-shot attempt at the whole conjecture did not succeed; the user then decomposed the problem and directed the system toward prior results to build upon. These are author-reported historical details, not independently verified log evidence. No dates or number of exchanges were supplied. Source: user's clarification in this task on 19 November 2026 (the interaction date is not thereby established).
- This resembles the **guided interaction** described by Anari–Ebrahimnejad in Appendix A, rather than their other author's one-shot interaction. Their appendix explicitly distinguishes the two contributors' different levels of guidance. It supports describing human decomposition and selection of relevant mathematical tools openly; two examples do not establish how statistically typical this workflow is. [Anari–Ebrahimnejad, Appendix A](https://arxiv.org/html/2605.21946v1#A1).
- Suggested factual disclosure, subject to author approval of its scope: “We used Claude Opus 5.5 in medium mode during the development of the proof. An initial attempt to address the full conjecture in a single interaction was unsuccessful. The subsequent development was guided by the author, who decomposed the problem into subproblems and identified prior results on which the arguments should build. Complete interaction transcripts were not retained; the accompanying repository preserves research reports and proof artifacts.” Add the exact scope of human verification and responsibility once the author confirms it. Do not call this autonomous or one-shot discovery, and do not imply that an unsuccessful attempt concerned the broader context-freeness conjecture unless the author confirms that interpretation.
