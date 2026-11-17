# Candidate background literature (task 8)

AI-assisted (Claude, 13 November 2026). **Candidate list only. Nothing here is cited in the manuscript yet.** Every entry is pending the authors' reading.

For each entry, "Verified" says what was checked:

- citation metadata against Crossref or the arXiv record (on 13 November 2026), or
- the full text itself, which was read only for Uuk et al., Bieringer et al. and the Butler Review.

No claim about a paper's content is made beyond what was checked.

## 1. Circular reporting and source evaluation in intelligence analysis

**1.1** D. Irwin and D. R. Mandel, "Improving information evaluation for intelligence production," *Intelligence and National Security*, vol. 34, no. 4, pp. 503–525, 2019. doi:10.1080/02684527.2019.1569343.

- *Verified:* Crossref metadata and the abstract (Semantic Scholar record, 13 Nov 2026). The full text is closed access, and the publisher's site showed a bot-verification page, which was not bypassed.
- *What the abstract says:* the authors argue that information-evaluation methods "mask rather than effectively guide subjectivity". They propose context-sensitive guidelines, including numeric probability estimates, collaboration between collector and analyst, and periodic re-evaluation.
- *Why it matters:* a critique of the NATO information-evaluation system (source reliability and information credibility, the "Admiralty Code"). In that system, credibility rises with corroboration, and our study asks exactly when corroboration is genuine.
- *Not verified:* the abstract does not mention circular reporting or the independence of corroborating sources. Whether the full text does is unknown. Cite it for information evaluation in general, not for circular reporting, unless an author reads the full text.

**1.2** M. O. Kelly, D. V. Budescu, M. K. Dhami and D. R. Mandel, "The effect of source reliability and information credibility on judgments of information quality in intelligence analysis," *Judgment and Decision Making*, vol. 20, 2025. doi:10.1017/jdm.2025.10007.

- *Verified:* Crossref metadata.
- *Why it matters:* experimental evidence that analysts weight source reliability over information credibility. It is relevant to how readers may over-weight a reputable organization's account of another organization's systems.

**1.3** R. J. Heuer, Jr., *Psychology of Intelligence Analysis*. Washington, DC: Center for the Study of Intelligence, CIA, 1999. https://www.cia.gov/resources/csi/static/Pyschology-of-Intelligence-Analysis.pdf

- *Verified:* the publisher's PDF exists at that address.
- *Why it matters:* the standard reference on biases in evaluating evidence (Chapter 10). A search did not show that it treats circular reporting directly.

**1.4** NATO Science and Technology Organization, *Assessment and Communication of Uncertainty in Intelligence to Support Decision-Making*, Technical Report STO-TR-SAS-114.

- *Verified:* only that the report exists at sto.nato.int (search result). Year, editors and contents were not checked.
- *Why it matters:* NATO's own review of information-evaluation practice.

**1.5** Lord Butler of Brockwell (Chairman), *Review of Intelligence on Weapons of Mass Destruction: Report of a Committee of Privy Counsellors*, HC 898. London: The Stationery Office, 14 July 2004.

- *Verified:* the full text (216 pages) was read on 13 Nov 2026, from a copy hosted by Statewatch: https://statewatch.org/wp-content/uploads/2026/04/butler-report.pdf (SHA-256 `1a1008379ed9…`). Its title page reads "HC 898 … Ordered by the House of Commons to be printed 14th July 2004". The GOV.UK file `wmdreview.pdf` is a different document: the government's implementation response, Cm 6492.
- *What it says (PDF page numbers):*
  - Chapter 1 (p. 25): "Corroboration is always important but seldom simple". Reports from different sources "may not necessarily confirm one another" when "both [are] merely based on the same thing".
  - Para. 29 (p. 23): validating a reporting chain "requires both care and time".
  - p. 102: one new report "was complementary to rather than confirming" earlier reports.
  - The report does **not** use the term "circular reporting" (scripted search of the full text).
- *Why it matters:* this is the clearest official statement of the principle behind our distinction. Agreement between reports is not confirmation when they rest on the same underlying observation. It is a strong primary citation for the "agreement is not independence" framing, and it does not depend on the term "circular reporting".

## 2. Inter-coder reliability

**2.1** J. Cohen, "A coefficient of agreement for nominal scales," *Educational and Psychological Measurement*, vol. 20, no. 1, pp. 37–46, 1960. doi:10.1177/001316446002000104.

- *Verified:* Crossref metadata.
- *Why it matters:* Cohen's kappa, computed by `blind_coding/agreement.py` for each pair of coders.

**2.2** K. Krippendorff, "Reliability in content analysis: Some common misconceptions and recommendations," *Human Communication Research*, vol. 30, no. 3, pp. 411–433, 2004. doi:10.1111/j.1468-2958.2004.tb00738.x.

- *Verified:* Crossref metadata.
- *Why it matters:* the argument for Krippendorff's alpha over kappa in content analysis. It also gives a reason to report alpha alongside kappa and AC1.

**2.3** A. F. Hayes and K. Krippendorff, "Answering the call for a standard reliability measure for coding data," *Communication Methods and Measures*, vol. 1, no. 1, pp. 77–89, 2007. doi:10.1080/19312450709336664.

- *Verified:* Crossref metadata.
- *Why it matters:* the standard citation for computing alpha. It applies to any number of coders and to missing data, which matters if a third coder or partial sheets are used.

**2.4** K. L. Gwet, "Computing inter-rater reliability and its variance in the presence of high agreement," *British Journal of Mathematical and Statistical Psychology*, vol. 61, no. 1, pp. 29–48, 2008. doi:10.1348/000711006X126600.

- *Verified:* bibliographic records found by search; Crossref returned an incomplete record.
- *Why it matters:* AC1, which stays stable when one category dominates. In our data "supports" is very frequent, which is exactly where kappa shows its known paradoxes, so AC1 should be reported next to kappa.

## 3. Uuk et al. (named by the authors)

R. Uuk, S. Koivula, L. Pacchiardi, R. Gipiškis, L. Caroli and K. Horton, "Assessing the Empirical Evidence for Loss of Control from Agentic General-Purpose AI," arXiv:2610.25241, 18 Oct. 2026 (before the 25 Oct. cutoff).

- *Verified:* arXiv record and full text (42 pages) downloaded and read for the summary below.

**Summary.** The paper evaluates 19 empirical studies across eight properties drawn from loss-of-control threat models, such as strategic deception, situational awareness and autonomous replication. It rates each study's construct, content and external validity, and it concludes that the evidence supports loss of control only as "weakly plausible". No study clears its thresholds for a judgment that a property is present.

**Why it matters.** It is a structured evidence-quality assessment in the same family as ours, but for capability studies rather than incident disclosures. Our study grades the *documentary* evidence that incidents happened as described; Uuk et al. grade the *experimental* evidence for underlying properties. The two are complementary, and the paper is a natural citation in Related Work, with a sentence on the difference in unit (study versus disclosure).

## 4. Bieringer et al.: re-read

L. Bieringer, S. McGregor, N. Nichols, K. Paeth, A. Paverd, J. Petit, J. Stängler, A. Wespi, A. Alahi and K. Grosse, "Practice-Informed, Practice-Ready: An AI security incident taxonomy," arXiv:2412.14855 (first version 19 Dec. 2024; the version read is the current arXiv version, online 26 Aug. 2026).

- *Verified:* full text (12 pages) re-read on 13 Nov. 2026.

### Exact overlaps

The fields are those of the paper's Table 2–4 incident information (I2) and implications (I3).

**D1 (access) and I2.4 "Access".** I2.4 asks "Which access was given to whom for model, inputs, training, test or evaluation data?"

- This is access *to the AI system's components*, used to identify how an attacker entered the system.
- Our D1 is the *agent's* access to external systems: what connectivity the AI agent had, and by what route it left its environment.
- The overlap is only in the field name. Bieringer's taxonomy treats the AI system as the *target* of an attacker; our incidents have the AI agent as the *actor*.
- The closer analogue to our D1 route is I2.5 "Security measures": "What security measures where used? Where they circumvented and if yes how?". It records circumvented controls, which our D1 records as the route.

**D4 (detection and response) and I2.6 "Fail safe measures".** I2.6 asks whether fail-safe measures were in place, with examples such as rebooting the system or falling back on human intervention.

- This overlaps our D4 *intervention and stopping* element, but not detection.
- Bieringer has no field for who detected the incident or when. Our detection/cessation split (which organization noticed, and how the activity ended) is not represented.
- I2.5 (whether security measures were circumvented) also overlaps D4 where a monitoring control failed to stop a run.

**D5 (effects) and I3.2 "Resulting harm" and I3.3 "Security impact".**

- I3.2 lists harm categories: physical health, financial loss, physical objects, intangible property, infrastructure, natural environment, rights.
- I3.3 asks how the incident affected "the confidentiality, integrity, availability of the AI system".
- Our D5 codes effects on *third-party* systems through branches C (credentials not issued to the agent), N (non-public data) and P (persistent change), and it explicitly separates effects from harm. I3.2 is therefore an analogue of the harm question our D5 refuses to answer.
- I3.3 concerns the AI system's own CIA, not the systems the agent acted on.
- The closest match is between our N and P and confidentiality and integrity, but applied to a different object.

**D2 (authorization belief) and I2.7 "Attacker's Intent".** I2.7 records whether a person or entity purposely caused the incident. It is a loose analogue only: our D2 is the *agent's* attributed belief about permission, not a human attacker's intent.

**What the manuscript can say.** Bieringer et al. give reporting fields for incidents in which an AI system is attacked. Our incidents invert the roles. The fields that share names with our dimensions record different objects:

- access *to* the AI system, not *by* it;
- the AI system's CIA, not third parties';
- harm rather than effect.

Only fail-safe measures (I2.6) map closely onto part of our D4. The current manuscript sentence, that Bieringer's access, fail-safe and harm fields "overlap our D1, D4 and D5", overstates the match for D1 and D5. The authors should decide whether to replace it.

## 5. Draft Related Work text: PENDING AUTHOR READING (do not paste without reading the sources)

> **Source evaluation and corroboration.** Intelligence practice grades a report by the reliability of its source and the credibility of its information [Irwin and Mandel 2019]. Analysts tend to weight source reliability over information credibility [Kelly et al. 2025]. The UK review of pre-war intelligence on Iraq warned that reports from different sources "may not necessarily confirm one another" when both rest on the same observation [Butler 2004, ch. 1]. Our distinction between cross-organization agreement and independent corroboration applies this principle to public incident disclosures. We record, for every supporting passage, the record it is drawn from.
>
> **Evidence-quality assessments in AI safety.** Uuk et al. assess the empirical evidence for loss of control from agentic AI across 19 studies, grading construct, content and external validity, and find the evidence "weakly plausible" [Uuk et al. 2026]. We grade a different kind of evidence: what public disclosures establish about incidents that occurred, rather than what experiments establish about capabilities.
>
> **Incident taxonomies.** Bieringer et al. propose reporting fields for AI security incidents in which an AI system is the target [8]. Our units reverse the roles: the agent is the actor and third-party systems are affected. Their access (I2.4) and impact (I3.3) fields therefore describe a different object from our D1 and D5. Their fail-safe field (I2.6) corresponds to the intervention part of our D4, but not to its detection part.
>
> **Coding reliability.** We will report raw agreement, Cohen's kappa [Cohen 1960] and Gwet's AC1 [Gwet 2008], because a dominant category depresses kappa, and Krippendorff's alpha as a cross-check [Hayes and Krippendorff 2007; Krippendorff 2004].
