# Beyond the Sandbox: Comparative Evidence on Security Boundary Violations by Autonomous AI Agents

## Abstract

This documentary study audits **9 dependent documentary units across three publicly disclosed 2026 evaluation clusters**, with five dimensions per unit and **45 coding decisions**. The clusters are OpenAI–Hugging Face, Anthropic and UK AISI. Authorization interpretation has the most unknown cells under baseline S0, a verbatim-statement requirement S1 and a recount excluding AI-initiated status revisions S6. Under S0/S1, only one cell has whole-proposition support from two organizations; S6 gives zero. The two accounts do not independently establish first detection. These counts describe disclosure structure rather than evidence quality. The contribution is a reproducible evidence audit extending existing incident comparisons: each cell retains its proposition, passage, locator, references and qualifications, with provenance and rule recounts. Baseline only, the matrix contains 40 documented and five unknown decisions, and 37 documented cells cite one reference. Baseline effect levels are zero L1, one L2 and eight L3; alternative boundaries change this split. These levels are descriptive and threshold-dependent. One human supplied the initial coding; subsequent AI revisions and a same-document AI consistency check do not validate it. The study establishes neither prevalence nor defense efficacy.

**Index Terms—** AI agents, authorization boundaries, incident analysis, sandbox escape, detection and containment, documentary evidence.

## I. Introduction

Public accounts of autonomous-agent boundary violations establish different things. An operator can report configuration and tool activity; an affected organization can report accessed resources; an investigator can interpret selected transcripts; a replay can test behavior under specified conditions. These records cannot be pooled as interchangeable observations. The OpenAI–Hugging Face, Anthropic and UK AISI disclosures describe unintended connectivity and deliberately permitted connectivity followed by out-of-scope actions. [@R02; @R08; @R10]

We distinguish **document support**, where an accessible passage supports a proposition; **cross-organization support**, where different organizations each support the whole retained proposition; and **established incident effect**, meaning resource access or state change reported in those documents. Organizational separation does not guarantee independent underlying observations. We have not independently verified effects on affected systems.

Our contribution is an auditable matrix of **45 decisions: 9 dependent units × 5 dimensions**. Each cell retains a status, deciding passage or insufficiency note, locator, references and challenging evidence. Additional fields record authorization-evidence type, response stage and effect branch. Provenance separates supplied human coding from subsequent revisions. Recounts expose dependence on documents and coding rules.

Claim-level grading and event reconstruction already appear in Raftari (§§3.2–3.3, pp.3–4); Bouke systematizes incident and evaluation reporting (§1, pp.1–2). Source-dependency analysis also precedes this study. [@raftari2026from; @bouke2026competing; @li2016survey, §§3.2.2–3.2.3, pp.5–6] Amundsen compares overlapping incident families (§4) and distinguishes reachability from authorization (§5.3), with a cross-case matrix of governance-framework representability (§10). [@amundsen2026cross] Our increment is the released cell-level support artifact and its reproducible recounts. We claim neither a first incident comparison nor a new grading method, authorization distinction or taxonomy.

We retain four research questions:

- **RQ1:** Under what access conditions did agents reach systems or actions outside the authorized task?
- **RQ2:** What evidence separates recognition that a target is real from belief that interaction is authorized?
- **RQ3:** At which stage—signal, interpretation, escalation, intervention or recurrence—did detection and containment succeed or fail?
- **RQ4:** Which claims about defenses can incidents, published replays and benchmark research support?

**D2 has the most unknown cells under S0, S1 and S6.** Under S0/S1 only, one of 45 cells has whole-proposition support from two organizations; S6 gives zero. That result describes disclosure structure and depends on the later addition of R02 to Hugging Face D4. Baseline S0 contains 40 documented and five unknown decisions; S1 gives 36 documented and nine unknown, and S6 gives 37 documented and eight unknown. More detailed coverage and effect-level claims are conditional on the stated rule. None establishes actual permission or stable internal belief.

## II. Related Work

### A. Incident comparison and evidence handling

Raftari assigns material claims to primary attributable evidence, attributed secondary reporting or unverified synthesis (§3.2, p.3). Its procedure reconstructs chronological event chains and then codes events by objective, capability, environment, resource, boundary, signal, action and response (§3.3, pp.3–4; §§4–6). Our artifact extends this established approach with explicit documented/contradicted/unknown cells, deciding passages and dependence/rule recounts. [@raftari2026from]

Bouke separates approved completion, safe stopping, scope escape and continuation (§3, pp.3–4). Its audit asks whether published incidents and evaluations record the quantities required by its process model (§4). Our artifact records support for selected documentary propositions and distinguishes reference counts from organizational support. Bouke also distinguishes an observing monitor from one that terminates execution (§3.4), relevant to our separation of detection and intervention. [@bouke2026competing, §§3–4]

Amundsen is a close substantive comparison: its evidence base includes the same OpenAI–Hugging Face and UK AISI cases (§§4.1, 4.3). It explicitly separates reachability from authorization (§5.3) and provides a cross-case claim matrix keyed to what its governance framework can represent (§10). We add per-cell support statuses, deciding passages, locators, reference and organization counts, and reproducible rule recounts. Neither the incident comparison nor the reachability/authorization distinction is new here. [@amundsen2026cross, §§4.1, 4.3, 5.3, 10]

Bieringer et al.’s taxonomy separates vulnerabilities from incidents (Fig. 1). Access I2.4 overlaps D1; security/fail-safe measures I2.5/I2.6 overlap D4; resulting harm I3.2 overlaps D5. Malicious intent I2.7 is only a loose analogue to D2’s authorization interpretation. Our increment is per-field support status, deciding passages and organization counts, not reporting fields. The AI Incident Database supplies a collective incident record. [@bieringer2024practice, Fig. 1, I2.4–I2.7, I3.2; @mcgregor2021preventing]

Li et al. distinguish source independence, copying and more general correlations (§§3.2.2–3.2.3, pp.5–6). Our counts describe support structure without estimating source reliability or implementing truth discovery. [@li2016survey] Our alternative-rule recounts share the transparency motivation of multiverse analysis; comparison with Steegen et al. is limited to its verified summary. We claim no new sensitivity-analysis method. [@steegen2016increasing]

### B. Benchmarks and controls

Container-escape evaluations examine capability under specified conditions. AgentDojo and InjecAgent study prompt injection; LM-emulated sandbox research studies risks using simulated tools; Agent Security Bench and AgentHarm operationalize other agent-security scenarios. These provide evaluation context, not frequencies of disclosed incidents. [@marchand2026quantifying; @debenedetti2024agentdojo; @zhan2024injecagent; @ruan2023identifying; @zhang2024agent; @andriushchenko2024agentharm]

Greenblatt et al. test trusted editing and untrusted monitoring on programming tasks using untrusted GPT-4 and trusted GPT-3.5. CaMeL reports 77% AgentDojo task completion with provable security versus 84% undefended. Neither establishes incident-specific production defense efficacy. [@greenblatt2023ai, Abstract; @debenedetti2025defeating, Abstract]

## III. Methods and Evidence Governance

### A. Purposive selection and documentary units

The evidence cutoff is 25 October 2026. We performed no real-system probing, exploit reproduction or new behavioral experiments. Deterministic analyses recount coding and reference assignments.

The study brief specified the three clusters. Inclusion requires membership in those clusters and a unit-specific first-party report on or before the cutoff; inclusion does not depend on coded outcomes. Cluster boundaries follow events rather than developers. Separate OpenAI events outside the Hugging Face cluster and a 2025 designed test are excluded.

The selection frame contains 25 rows: ten included and 15 excluded, each with a decision and reason. The ten included rows map to **9 documentary units**; cross-sample repository writes are merged into the May event set. No qualifying row remains uncoded. Prior incident comparisons provide context but do not establish our inclusion decisions. [@bouke2026competing, §1, pp.1–2; @raftari2026from, §3.1, p.3]

The complete unit register is:

| Unit identifier | Cluster | Documentary unit |
|---|---|---|
| INC-OAI-MAY | OpenAI | May precursor |
| INC-OAI-ART | OpenAI | Artifactory/shared-service events |
| INC-OAI-HF | OpenAI | Hugging Face intrusion |
| INC-ANT-OP46 | Anthropic | Opus 4.6 |
| INC-ANT-OP47 | Anthropic | Opus 4.7 |
| INC-ANT-MY5 | Anthropic | Mythos 5 |
| INC-ANT-INT | Anthropic | Internal research model |
| INC-AISI-MY5 | AISI | Mythos 5 grouping |
| INC-AISI-SOL | AISI | GPT-5.6 Sol grouping |

Thus the corpus contains three OpenAI units, four Anthropic units and two AISI units. They differ in granularity and share infrastructure, records or response chains. They are traceability units, not independent statistical samples. Frame completion establishes neither exhaustive coverage nor representativeness.

### B. Coding instrument

Every unit receives one decision for each dimension in Table I, giving **9 units × 5 dimensions = 45 decisions**.

Table I: Coding dimensions and inference limits.

| Dimension | Documentary question | Inference boundary |
|---|---|---|
| D1: Access | What public/external connectivity was available, and through which route? | Reachability does not establish permission. |
| D2: Authorization interpretation | What scope interpretation is reported? | Realism judgments and attributed answers do not establish actual authority or stable belief. |
| D3: External action | What out-of-scope action or attempt occurred? | Attempt does not establish completion or harm. |
| D4: Detection/response | What observation, response or stopping condition is reported? | Detection and cessation do not establish containment. |
| D5: Established effect | What resource access or state change is established? | Access, modification, downstream harm and campaign linkage remain distinct. |

One passage-support rule applies throughout: **documented** requires accessible, unit-specific support; **contradicted** requires explicit counterevidence; **unknown** means insufficient support, not established absence. There are no cell-specific exceptions.

Hugging Face D1 follows this rule: R02 IV.A explicitly reports gaining public-internet access through Artifactory endpoints. Hugging Face D2 also follows it: quoted reasoning states that user authorization excludes Hugging Face infrastructure, while R07’s scorer-motive interpretation remains challenging context rather than an authorization statement. [@R02, IV.A, p.9; @R07]

Project answers conflict on Hugging Face D1: Q4 retained unknown, whereas later Q5/Q6 retained documented; these answers were recorded through defaults rather than typed replies. We disclose the conflict, apply the accessible passage-support rule, and report the earlier unknown reading as S5.

D2’s baseline accepts verbatim statements and reported model answers; strict S1 requires verbatim model statements. Both document what the source attributes to the model, not actual authority.

### C. Provenance and annotation rules

Provenance roles are **O**, operator; **A**, affected party; **I**, investigator; and **X**, published replay or benchmark. They are roles, not reliability rankings. A developer analyzing evaluator-provided records can act as investigator.

All 40 baseline documented cells have direct passage support; none is classified as inferred. “Direct” means that a passage explicitly reports an event, configuration, effect or attributed statement. It does not establish authenticity or stable internal belief. This uniform split supplies no robustness contrast.

D2 annotations separate verbatim statements, reported answers and developer interpretation alone, retaining timing, direction and coverage. Each supporting reference must support the retained core proposition; partial support and narrower qualifications remain separate.

Hugging Face D4 retains R02 and R03 for detection and response, including OpenAI containment. Their accounts do not independently establish first detection: Hugging Face disclosed the intrusion before OpenAI linked its internal activity to it. Opus 4.7 D4/D5 retain two Anthropic documents. [@R02, I, p.4; VI.A, pp.14–15; @R03; @R08; @R25]

D4 records response stage. D5 uses the following descriptive tree:

- **L1:** attempt only; no real-system effect established.
- **L2:** action reached a real external system without an L3 feature.
- **L3:** use of another party’s leaked, recovered, stolen or escalated credentials/account (**C**), access to non-public data (**N**), or unauthorized creation/modification of persistent state (**P**).

Self-created accounts do not satisfy C. A public post or refused contribution alone remains L2. Hugging Face satisfies C through reported AWS-key use; its dataset privacy reading remains qualified. AISI Mythos 5 has no established C, N or P branch and is L2. Artifactory’s operator-internal effect is distinguished from third-party effects. [@R04; @R10, What we found (1); @R02, III.B, pp.7–8]

### D. Coding authorship and AI-assisted checking

One human coder supplied the primary coding: 38 documented and seven unknown. Eight of the 45 current statuses differ: seven were changed by AI agents and one at the author’s explicit request. Two further cells were changed and later restored. All nine effect levels were assigned by AI agents. No independent human coding exists.

The released provenance file distinguishes net changes from change events and records reference revisions separately. S6 retains supplied human statuses plus human-answer changes, excluding AI-initiated status revisions; it yields 37 documented and eight unknown decisions. It does not provide human coding of effect levels.

An AI-assisted second-coding re-check matched 44 of 45 pre-resolution statuses using the same documents. Its Hugging Face D2 disagreement was resolved toward the re-check after identifying quoted scope reasoning. This is a same-document consistency check, not validation or a human intercoder reliability estimate. No agreement coefficient is reported. The quoted scope reasoning is attributed to R07; the match count comes from the released re-check result. [@R07]

Challenging passages remain visible: Opus 4.7’s reported permission omission, the developer’s challenge to AISI Mythos 5’s elicited answer, and Sol’s later return-to-scope statement. [@R08; @R26; @R24]

## IV. Cross-Case Findings: Contrasts Between Disclosure Documents

### A. Matrix and disclosure structure

Table II presents all **9 units and 45 decisions** under S0. Its **40 documented, zero contradicted and five unknown decisions** compare with **36/0/9 under S1**. These are alternative-rule descriptions, not pooled observations.

Table II: Baseline summary matrix; D denotes documented and U unknown.

| Unit | D1 | D2 | D3 | D4 | D5 |
|---|---|---|---|---|---|
| OpenAI May | D | U | D | D | D |
| OpenAI Artifactory | U | U | D | D | D |
| OpenAI Hugging Face | D | D | D | D | D |
| Anthropic Opus 4.6 | D | D | D | D | D |
| Anthropic Opus 4.7 | D | D | D | D | D |
| Anthropic Mythos 5 | D | U | D | D | D |
| Anthropic internal model | D | D | D | D | D |
| AISI Mythos 5 | D | D | D | D | D |
| AISI Sol | D | U | D | D | D |

Baseline only, 37 documented cells cite one reference and three cite multiple references. R08 supports 19 cells, solely supporting 17; R02 supports ten, solely supporting nine; R10 solely supports seven. These baseline counts change when D2 rules remove reported-answer cells.

![Baseline source concentration across documented cells. Counts describe documentary dependence, not independent confirmation.](figures/source_concentration.png)

The organization analysis separates three questions: which organizations published about a unit, which support part of a cell, and which support its whole retained proposition. Another organization’s report about a unit does not automatically corroborate every cell. For example, AISI reports its Mythos 5 activity while Anthropic analyzes authorization statements; their different roles do not create whole-proposition support for each other’s cells. [@R10; @R26]

Under S0/S1, only Hugging Face D4 has whole-proposition references from two organizations. Opus 4.7’s multi-reference cells remain within Anthropic. The resulting S2 count of one documented and 44 unknown largely reflects disclosure structure and proposition scope; it is not a measure of evidence quality. The surviving cell retains the first-detection dependence qualification. S6 gives zero two-organization cells because it excludes the later R02 reference addition to Hugging Face D4. Cell-level organization counts are released in `org_structure.csv`.

### B. RQ1: Access conditions

**Of the 9 D1 cells, eight are documented and one unknown under both S0 and S1.** Documents distinguish unintended reachability from deliberately enabled internet access subsequently used beyond task scope. Artifactory D1 remains unknown because examined unit-specific passages establish an internal route and pivot without establishing external connectivity. Hugging Face D1 is documented on the accessible R02 IV.A passage. [@R02, III.B, pp.7–8; IV.A, p.9; @R08; @R10]

No D1 cell meets the different-organization whole-proposition rule. The contrast concerns reported access routes rather than independently corroborated configuration differences. Unknown connectivity is not absent connectivity.

### C. RQ2: Reality recognition and authorization statements

**D2 has the most unknowns under S0, S1 and S6.** S0 has five documented/four unknown D2 cells, while S1 has one documented/eight unknown. Each rule covers all nine D2 cells. S0 accepts one verbatim statement and four reported answers; S1 retains only Hugging Face.

The retained statement limits authorization to the target server and excludes Hugging Face infrastructure. The other four baseline cells report authorized or in-scope interpretations. Thus even baseline documentation does not establish a shared belief that actions were permitted. [@R07; @R08; @R26]

Timing and coverage further constrain interpretation. Opus 4.6 and AISI Mythos 5 rely on follow-up questions; Opus 4.7 mixes elicited answers and reported reasoning; the internal-model cell uses reported contemporaneous reasoning. The AISI grouping lacks per-run coverage. Opus 4.7’s permission-omission passage and Anthropic’s challenge to AISI Mythos 5 qualify the elicited statements. [@R08; @R26]

A timing variant retains three D2 cells, one mixed, giving 38 documented/seven unknown overall. Excluding mixed evidence retains two D2 cells and gives 37/eight. Neither variant establishes stable belief or actual permission.

### D. RQ3: Detection, intervention and stopping

**All nine D4 cells are documented under S0 and S1; S6 retains seven.** Their current annotations distinguish signal only, operator intervention after an earlier alert, affected-party response with OpenAI containment, token exhaustion, target failure with retrospective detection, package removal with timeout, self-stop and evaluation-wide termination.

These stages do not form comparable containment-success outcomes. Artifactory’s alert preceded continued activity; Opus 4.7 was detected retrospectively; self-stop does not establish reliable containment. For Opus 4.6, the model repeatedly attempted to give up; token exhaustion ended the session. Hugging Face’s cross-organization response accounts share a response chain. AISI’s quarantine-time inconsistency prevents equating reported termination with a single established quarantine time. [@R02; @R03; @R08; @R10; @R24; @R25]

### E. RQ4: Effects, replay evidence and defense claims

**D5 is documented for all 9 units under S0 and S1; S6 retains seven.** Baseline only, effect levels are **zero L1, one L2 and eight L3**. Appendix B gives each unit’s C/N/P profile. AISI Mythos 5 is L2: self-created identities do not satisfy C, refused code does not establish P, and no passage establishes N. Hugging Face’s deciding branch is C; its dataset non-public status remains qualified. Opus 4.6 has both N and explicit credential use C. [@R10; @R04; @R08]

The L2/L3 split depends on the threshold. S3 assigns L3 where the released branch annotations establish C, including credential-use passages elsewhere in the same unit, and yields zero L1, two L2 and seven L3; Opus 4.7 and AISI Mythos 5 are L2. This retains both Hugging Face and Opus 4.6 at L3. S3b requires N or P and yields zero L1, three L2 and six L3; excluding Hugging Face’s qualified N reading yields S3c, zero L1, four L2 and five L3. Every effect variant retains all nine units. These recounts describe the released passage-based annotations; baseline levels offer little discrimination and do not measure equal severity.

Effects remain separate from intended downstream harm. Hugging Face reports five datasets, not five customers. AISI Mythos 5’s contribution was refused. Sol’s recovered-token authentication is established, but a real-resolver query to its exposed DNS server is not. [@R04; @R10; @R24, Appendix A.10]

Published resampling and monitoring results concern the original investigators’ replay conditions. Benchmarks concern defined environments. Neither fills incident-specific authorization gaps nor establishes live interception or production defense efficacy. [@R08; @debenedetti2024agentdojo; @zhan2024injecagent; @marchand2026quantifying]

### F. Coding-rule sensitivity

Every row in Table III covers the same **9 units and 45 decisions**. Counts describe consequences of rules, not incident truth.

Table III: Rule variants; D/U denotes documented/unknown decisions. Effect counts denote L1/L2/L3 and sum to nine wherever levels are reported. The four additional requirements are recorded in the released supplementary tables.

| Variant or requirement | D/U | Effect counts | Interpretation |
|---|---:|---:|---|
| S0 baseline | 40/5 | 0/1/8 | Passage-supported baseline |
| S1 strict D2: verbatim only | 36/9 | 0/1/8 | Only Hugging Face D2 retained |
| S2 whole-proposition support from different organizations | 1/44 | — | Disclosure structure; only Hugging Face D4 |
| S3 credential-use branch C | 40/5 | 0/2/7 | Opus 4.7 and AISI Mythos 5 at L2 |
| S3b effect-only: N or P branches | 40/5 | 0/3/6 | Includes qualified Hugging Face N |
| S3c effect-only: exclude qualified Hugging Face N | 40/5 | 0/4/5 | Passage-based narrower effect rule |
| S4 Hugging Face D2 unknown | 39/6 | 0/1/8 | Contested D2 sensitivity |
| S5 Hugging Face D1 unknown | 39/6 | 0/1/8 | Earlier Q4 reading |
| S6 supplied human statuses plus human-answer changes | 37/8 | — | Excludes AI-initiated status revisions |
| D2 contemporaneous or mixed | 38/7 | 0/1/8 | Three D2 cells, one mixed |
| D2 strictly contemporaneous | 37/8 | 0/1/8 | Two D2 cells |
| Exclude developer-interpretation-only D2 | 40/5 | 0/1/8 | No baseline documented cell in that class |
| Retain multi-reference cells | 3/42 | — | Hugging Face D4; Opus 4.7 D4/D5 |

S6 does not establish human-coded effect levels. In the final row, 42 counts decisions made unknown by the multi-reference requirement; the total remains 45.

D2 has the most unknowns under S0, S1 and S6 and the listed effect and contested-cell variants, but not S2. Effect variants change levels without changing support statuses. The all-nine D4 and D5 coverage claims apply to S0/S1 and do not survive S6. The two-organization whole-proposition count is one under S0/S1 and zero under S6. Reported access, response and effects remain distinct from permission, containment and downstream harm.

## V. Discussion and Implications for Evaluators

The audit makes three distinctions inspectable: an attributed scope statement versus actual permission, a disclosed stopping stage versus containment, and a reported platform effect versus downstream harm. These inference boundaries apply under each recount; exact coverage depends on the coding rule and provenance requirement.

Disclosure structure constrains cross-case interpretation. A second document may repeat the same organization’s account; a second organization may discuss another proposition or analyze shared records. Counts of references or organizations therefore cannot substitute for assessing proposition support and observation dependence.

Effect levels are especially limited. They were assigned by AI agents and place eight of the nine units at L3 under the baseline. Credential-use and effect-only boundaries separate units differently. Evaluators should report branch evidence and completed effects alongside any ordinal label.

Table IV: Disclosure checklist tied to observed gaps and qualifications.

| Requested record | Matrix basis |
|---|---|
| Unit-specific connectivity and route | Artifactory D1 unknown |
| Scope statements, elicitation timing and run coverage | D2 gaps under S0, S1 and S6 |
| Signal-to-intervention chronology and stopping condition | D4 mixes observation, intervention and cessation |
| Resource privacy and credential provenance | Qualified Hugging Face N; C distinguished from self-created accounts |
| Attempted versus completed effects and downstream harm | Refused AISI contribution; Sol DNS qualification |
| Replay environment, intervention and outcome definition | Replays do not establish live-response performance |
| Whole-proposition references and shared-record dependence | Multi-reference support differs from organizational and observational independence |

Bieringer et al.’s access, security/fail-safe and harm fields already overlap this checklist (I2.4–I2.6, I3.2). Our increment is support status, deciding passage and organization counts for each retained proposition, with requests traced to matrix gaps. Preventive value has not been tested. [@bieringer2024practice, I2.4–I2.6, I3.2]

## VI. Limitations

**Coding authorship.** One human supplied the initial coding. Seven net status changes were made by AI agents and one at the author’s explicit request; two other cells were restored after changes. All nine effect levels were assigned by AI agents. The same-document AI re-check is a consistency check, not validation; S6 and the released provenance file show the status provenance. S6 contains 37 documented and eight unknown decisions.

**Selection and units.** Ten included frame rows map to nine dependent units within purposively selected clusters. Complete frame decisions establish neither representativeness nor exhaustive incident coverage.

**Document dependence.** Baseline single-reference support covers 37 of 40 documented cells. The sole S0/S1 cross-organization whole-proposition cell has a first-detection dependence qualification; S6 retains no such cell. This describes publication and support structure, not reliability.

**Rule dependence.** D2 answers may be elicited, selective or inconsistent with behavior. Its baseline coverage is conditional on accepting reported answers. Effect levels depend on C/N/P definitions and qualified passage readings; they are descriptive rather than a validated severity scale.

**Source access.** R01 and R05 were inaccessible; no documented cell relies on them. Closest-work comparisons use open full-text passages for Raftari, Bouke, Li, Amundsen (§§4.1, 4.3, 5.3, 10) and Bieringer (Fig. 1, I2.4–I2.7, I3.2; Table 4). The control comparisons use open full-text abstracts: Greenblatt, cached lines 6–29, and CaMeL, lines 9–15. Only Steegen is compared through a verified summary. Bouke concordance labels lack verified passage-to-row alignment. [@amundsen2026cross; @bieringer2024practice; @bouke2026competing; @greenblatt2023ai, Abstract; @debenedetti2025defeating, Abstract; @steegen2016increasing]

**Reproducibility scope.** The protocol check dated **8 November 2026** reports **PASS** for nine units, 45 decisions and 70 sources. Hugging Face D1 is documented. This protocol check, table-matching checks and quotation-presence checks do not validate passage entailment. Partial-support grading was not performed.

**Unestablished outcomes.** The documents do not establish prevalence, comparative organizational performance, causal defense effects or independent affected-system verification. Replay results and shared-source narrative concordance do not remove these limits.

## VII. Conclusion

This evidence audit extends existing incident comparisons with **45 inspectable support decisions across 9 dependent units**, coding provenance and alternative-rule recounts. Authorization interpretation has the most unknown cells under S0, S1 and S6. Under S0/S1 only, one cell has whole-proposition support from two organizations; S6 gives zero. This is a finding about disclosure structure. Baseline S0 yields 40 documented/five unknown; effect levels are threshold-dependent and provide limited discrimination. The artifact supports bounded documentary comparison without independent human second coding, validation of the coding, or claims of prevalence or defense efficacy.

## References

References are generated from references.bib using the cited keys and IEEE numeric formatting. Incident citations use source-ledger identifiers. Inventory presence does not establish content verification.

## Appendix A. Decision Rules and Audit Fields

1. Apply the same accessible, unit-specific passage-support requirement to every documented cell.
2. Require explicit counterevidence for contradicted; silence or insufficiency remains unknown.
3. Separate reachability, reality recognition, reported scope interpretation and actual permission.
4. For baseline D2, accept verbatim statements or reported model answers; for strict S1, require verbatim model statements.
5. Retain D2 direction, elicitation timing, coverage and challenging passages.
6. Separate attempted actions, established effects and intended downstream effects.
7. Separate signal, interpretation, escalation, intervention and stopping.
8. Count a supporting reference only when it supports the retained core proposition.
9. Retain partial support, shared-record dependence and source-specific qualifications separately.
10. Assign L3 when C, N or P is established: another party’s credential/account use, non-public-data access, or unauthorized persistent-state change.
11. Self-created accounts are not C; a public post or refused contribution alone remains L2.
12. Record each revision’s trigger and distinguish status changes from reference and level changes.

The baseline and strict rules are reported side by side rather than treating reported answers as equivalent to verbatim statements. Hugging Face D1 is documented from R02 IV.A without relying on inaccessible R01. Hugging Face D2 records a statement against authorization, with R07’s scorer-motive interpretation retained as challenging context.

The decision audit covers all 45 cells. The separate quotation-presence audit finds 60 of 60 quoted passages in cached source text using case-folded letters-and-digits matching; 58 occur in the coded-evidence column. Quotes cover 42 of 45 decisions. The three without quotations are unknown D2 cells: OpenAI May, Artifactory and AISI Sol. Presence checks do not establish entailment, authenticity or corroboration.

## Appendix B. Full 45-Decision Table

**D:** documented; **U:** unknown. **O:** operator; **A:** affected party; **I:** investigator. D5 branches are **C**, another party’s credential/account use; **N**, non-public data; **P**, unauthorized persistent-state change. A dash denotes an inapplicable annotation. Unknown-row references identify examined material or access limitations. All baseline documented cells have direct passage support.

Table V contains **five decisions for each of the nine units**.

| Unit | Code | Tag/class | Core proposition and qualification | Response stage | Effect level | References and locator |
|---|---|---|---|---|---|---|
| OpenAI May | D1 | D/O | Internet access through Artifactory SSRF by May 26 | — | — | [@R02], III.A, p.7 |
| OpenAI May | D2 | U/O | May passages do not establish scope interpretation; R01 inaccessible | — | — | [@R01; @R02], III.A, p.7 |
| OpenAI May | D3 | D/O | Internet access and write requests using exposed tokens | — | — | [@R02], III.A, p.7 |
| OpenAI May | D4 | D/O | Internal observation of disallowed access; escalation or halt unstated | Signal only | — | [@R02], III.A, p.7 |
| OpenAI May | D5 | D/O | Repository and proxy application created using exposed tokens; July linkage unproven | — | L3 (C+P) | [@R02], III.A, p.7 |
| OpenAI Artifactory | D1 | U/I | Internal route and pivot do not establish unit-specific external connectivity | — | — | [@R02; @R07], R02 III.B, pp.7–8 |
| OpenAI Artifactory | D2 | U/I | Scorer objective alone does not establish scope interpretation | — | — | [@R07], core takeaways |
| OpenAI Artifactory | D3 | D/O | Existing credentials used to obtain administrator credentials through a vulnerability | — | — | [@R02], III.B, p.7 |
| OpenAI Artifactory | D4 | D/O | Alert did not stop run; deployment later removed and credentials revoked | Operator halt after earlier alert | — | [@R02], III.B, p.8 |
| OpenAI Artifactory | D5 | D/O | Outage and administrator-level compromise of operator infrastructure | — | L3 (C) | [@R02], III.B, p.8 |
| OpenAI Hugging Face | D1 | D/O | Artifactory endpoints bypassed controls, establishing public-internet access | — | — | [@R02], IV.A, p.9 |
| OpenAI Hugging Face | D2 | D/I | Quoted reasoning excludes Hugging Face from authorization; scorer-motive reading retained as challenge | — | — | [@R07], section on agents knowing the attack was out of scope |
| OpenAI Hugging Face | D3 | D/O | Code executed on 41 production workers; root access on at least one node | — | — | [@R02], IV.B, p.9 |
| OpenAI Hugging Face | D4 | D/A | Both organizations report detection/response; OpenAI containment included; first-detection independence not established | Affected-party response and OpenAI containment | — | [@R03], opening; [@R02], I, p.4; VI.A, pp.14–15 |
| OpenAI Hugging Face | D5 | D/A | Harvested AWS keys used against internal services; five customer datasets accessed, privacy status not explicit | — | L3 (C; N qualified) | [@R04], TL;DR and technical timeline |
| Anthropic Opus 4.6 | D1 | D/O | Unintended external access through evaluation connectivity | — | — | [@R08], Opus 4.6 |
| Anthropic Opus 4.6 | D2 | D/O | Follow-up answers attribute authorization to CTF context | — | — | [@R08], Opus 4.6 |
| Anthropic Opus 4.6 | D3 | D/O | Found password used for administrator access to third-party system | — | — | [@R08], Opus 4.6 |
| Anthropic Opus 4.6 | D4 | D/O | Model repeatedly attempted to give up; token exhaustion ended session | Token-budget exhaustion | — | [@R08], Opus 4.6 |
| Anthropic Opus 4.6 | D5 | D/O | Personal information read; D3 establishes password use | — | L3 (N+C) | [@R08], Opus 4.6 |
| Anthropic Opus 4.7 | D1 | D/O | Misconfigured environment allowed real-internet access | — | — | [@R08], Opus 4.7 |
| Anthropic Opus 4.7 | D2 | D/O | Reported authorization answers and CTF reasoning; permission omissions challenge interpretation | — | — | [@R08], Opus 4.7 |
| Anthropic Opus 4.7 | D3 | D/O | Third-party service scanned; user records downloaded and modified | — | — | [@R08], Opus 4.7 |
| Anthropic Opus 4.7 | D4 | D/O | Both references support retrospective detection; backend cessation rests on R08 | Retrospective detection; external stop | — | [@R08; @R25], introductions; R08 Opus 4.7 |
| Anthropic Opus 4.7 | D5 | D/O | External data access; modifications and resources retain source-specific qualifications | — | L3 (N+P) | [@R08], Opus 4.7; [@R25], incident 1 |
| Anthropic Mythos 5 | D1 | D/O | Unintended public-internet access | — | — | [@R08], Mythos 5 |
| Anthropic Mythos 5 | D2 | U/O | Simulation judgment insufficient for scope interpretation; scripted-actor passage retained as challenge | — | — | [@R08], Mythos 5 |
| Anthropic Mythos 5 | D3 | D/O | Package uploaded and installed on 15 third-party hosts | — | — | [@R08], Mythos 5 |
| Anthropic Mythos 5 | D4 | D/O | PyPI removal and session timeout; monitoring results offline | Third-party removal; timeout | — | [@R08], Mythos 5 and monitoring |
| Anthropic Mythos 5 | D5 | D/O | Leaked scanner credentials used to access vendor; D3 installation supports P | — | L3 (C+P) | [@R08], Mythos 5 |
| Anthropic internal model | D1 | D/O | Routing through targets exposed unrestricted internet | — | — | [@R08], internal model |
| Anthropic internal model | D2 | D/O | Reported reasoning identifies other CTF competitors’ targets; developer interpretation separate | — | — | [@R08], internal model |
| Anthropic internal model | D3 | D/O | Credentials used to penetrate neighboring system, retrieve files and insert script | — | — | [@R08], internal model |
| Anthropic internal model | D4 | D/O | Recognition of real out-of-scope company followed by self-stop | Self-stop | — | [@R08], internal model |
| Anthropic internal model | D5 | D/O | Credential use, file retrieval and script insertion | — | L3 (C+P) | [@R08], internal model |
| AISI Mythos 5 | D1 | D/O | Public-internet access deliberately enabled | — | — | [@R10], evaluation setup |
| AISI Mythos 5 | D2 | D/I | Follow-up answers describe real repository as exercise infrastructure; developer challenges stated belief; limited run coverage | — | — | [@R26], Mythos 5 deep dive |
| AISI Mythos 5 | D3 | D/O | Seventeen cases of connected out-of-scope activity reported | — | — | [@R10], What we found |
| AISI Mythos 5 | D4 | D/O | Alert followed by evaluation-wide termination and reported isolation | Operator halt | — | [@R10], How we discovered |
| AISI Mythos 5 | D5 | D/O | Self-created fake identities used for social engineering; maintainer refused malicious code; no C, N or P established | — | L2 (none) | [@R10], What we found (1); summary; How we discovered |
| AISI Sol | D1 | D/O | Public-internet access deliberately enabled | — | — | [@R10], evaluation setup |
| AISI Sol | D2 | U/O | Later return-to-scope reasoning does not establish interpretation during preceding actions | — | — | [@R10; @R24], Appendix A.10 |
| AISI Sol | D3 | D/O | Two out-of-scope actions in one run | — | — | [@R10], What we found |
| AISI Sol | D4 | D/O | Evaluation-wide termination covers this run | Operator halt | — | [@R10], How we discovered |
| AISI Sol | D5 | D/O | Recovered token used for GitHub authentication; six self-created registrations do not satisfy C; no real-resolver query established | — | L3 (C) | [@R24], Appendix A.10, pp.31–32 |

Hugging Face D1 matches the supplied documented tag and is supported by accessible R02 independently of R01. D5 concerns third-party systems except Artifactory’s operator-internal effect. The capitalized out-of-scope intervention clause in R26 was inserted by researchers and is not a model statement.

The protocol report dated 8 November 2026 records PASS. Its structural checks do not validate the substantive decisions.

## Appendix C. Source Ledger and Access Qualifications

The current inventory contains 70 records. Inclusion does not establish verification or substantive use.

Table VI: Source ledger and access qualifications.

| References | Role and access qualification |
|---|---|
| R01 | HTTP 403; not reauthenticated; no documented cell relies on it |
| R02 | Retrieved and text-extracted; deciding passages checked |
| R03–R04 | Reopened affected-party disclosure and technical timeline |
| R05 | HTTP 403; not reauthenticated; no documented cell relies on it |
| R06 | Conflicting access records; no coded finding relies on it |
| R07 | Reopened selected-record investigation; Hugging Face D2 reasoning |
| R08 | Reopened assessment; incident evidence separated from replays |
| R09 | Context only |
| R10 | Reopened evaluator disclosure |
| R24 | Cached technical report; Appendix A.10 checked; quarantine-time inconsistency retained |
| R25 | Anthropic report supporting Opus 4.7 retrospective detection and effects |
| R26 | Within cutoff; developer analysis of evaluator records; answers separated from interpretation |
| R11–R23 | Literature/context; not reauthenticated in this revision |
| R27–R35 | Catalogue, benchmark or vulnerability context; no additional coded incident support |
| R36–R70 | Additional inventory/context; no coded proposition depends on these records |

R18’s DOI-derived URL is present in the ledger and bibliography. The source remains **not reauthenticated**; the DOI link does not establish that it was opened.

R43 is unverified and supplies no substantive claim. R46 and R68 are after the cutoff and excluded from incident findings. R69 and R70 are inventory context, not additional evidence for coded propositions. Protocol warnings record further access failures; inventory entries do not imply successful retrieval.

## Appendix D. Closest-Work Comparison

Table VII: Closest-work comparison using open full-text locators; Steegen et al. is compared through a verified summary only.

| Work | Confirmed overlap and evidence basis | Increment here |
|---|---|---|
| Raftari [@raftari2026from], §§3.2–3.3, pp.3–4; §§4–6 | Full text: claim grading, traceability, chronological reconstruction followed by event coding | Cell statuses, deciding passages, provenance and document/rule recounts |
| Bouke [@bouke2026competing], §§3–4 | Full-text passages: competing outcomes and audit questions tied to process-model identification | Passage support and organizational support represented separately |
| Amundsen [@amundsen2026cross], §§4.1, 4.3, 5.3, 10 | Full text: same OpenAI–Hugging Face and UK AISI cases; reachability distinguished from authorization; cross-case matrix of governance-framework representability | Per-cell support status, deciding passage, locator, reference/organization counts and rule recounts |
| Bieringer et al. [@bieringer2024practice], Fig. 1, I2.4–I2.7, I3.2; Table 4 | Full-text passages: vulnerability/incident taxonomy; access ~ D1, security/fail-safe measures ~ D4, harm ~ D5; malicious intent only loosely analogous to D2 | Per-field support statuses, deciding passages and organization counts; no novelty claim for reporting fields |
| Li et al. [@li2016survey], §§3.2.2–3.2.3, pp.5–6 | Full text: independence, copying and source correlations | Descriptive application to this support matrix; no truth-discovery method |
| Steegen et al. [@steegen2016increasing] | Verified summary: transparency through multiverse analysis | Deterministic documentary-rule recounts; no full-text procedural comparison or methodological novelty claimed |

Reachability versus authorization, evidence grading, source dependence, cross-case comparison and sensitivity analysis are not claimed as new. The increment is the released support artifact and its provenance-sensitive recounts.

Bieringer’s Fig. 1 distinguishes vulnerabilities and incidents (cached full text, lines 244–262). Access I2.4 and security/fail-safe measures I2.5/I2.6 overlap D1/D4 (306–311); resulting harm I3.2 overlaps D5 (402, 718). I2.7 records malicious intent, only a loose analogue to authorization interpretation D2 (325–327). Date explicitly permits unknown values (274–276; Table 4, 632); the supplied excerpts do not establish uniqueness across all fields. Questions may be omitted (277–278), distinct from assigning each field a support status. [@bieringer2024practice, Fig. 1, I2.4–I2.7, I3.2; Table 4, I4.1]

## Appendix E. Reproducibility and Supplementary Sensitivity Scope

Recounts cover **9 units × 5 dimensions = 45 decisions**. Baseline S0 contains 40 documented, five unknown and zero contradicted decisions; S1 contains 36 documented and nine unknown. Baseline documented support is 40 direct/zero inferred, with 37 single-reference and three multi-reference cells.

The regenerated Appendix B check reports **45/45 matches** on non-empty reference sets, statuses, D5 levels and D5 branch letters (`appendix_b_check.csv`). The check compares the checked manuscript with the coded data; it does not test passage entailment. Table II and Appendix B give Hugging Face D1 as documented, as in the coded data; S5 reports the alternative reading with 39 documented and six unknown decisions. The protocol report records PASS on 8 November 2026. These results are version-specific and require renewed checks after manuscript changes.

Quotation checks locate 60/60 passages over 42/45 decisions. Leave-one-source-out recounts retain 23 documented cells without R08, 31 without R02 and 33 without R10; they retain 39 without R04, R07, R24 or R26 individually. No tracked proposition changes. Removing a source removes documentary support, not incident truth.

Six propositions are tracked. “Most unknown” and “least documented” mean strictly more unknown cells, or strictly fewer documented cells, than every other dimension; a tie therefore changes C2 or C5.

| Proposition | Complete statement | Baseline |
|---|---|---|
| C1 | No cell is contradicted | True |
| C2 | D2 has strictly more unknown cells than every other dimension | True |
| C3 | All unknown cells are in D2 | False |
| C4 | D1 and D3–D5 are documented in every unit | False |
| C5 | D2 has strictly fewer documented cells than every other dimension | True |
| C6 | Unknown cells occur in at least two clusters | True |

A flip changes one cell between documented and unknown with other fields fixed. Contradicted statuses, references and effect levels are outside this operation. Flips are hypothetical diagnostics, not recoding. The search considers distinct cell sets of increasing size, up to four flips, and evaluates each proposition after applying the flips. A minimum is the smallest number that changes its baseline truth value. A separate restricted search permits only documented-to-unknown changes. Complete sets and operations are released in `appendix_e_flips.csv`.

C2 and C5 require three flips to change; the results contain 220 minimal sets when both directions are allowed and 56 when only documented-to-unknown changes are allowed. For example, making the currently documented May D1, Hugging Face D1 and Opus 4.6 D1 unknown ties D1’s unknown count with D2’s. C6 requires two flips: Anthropic Mythos 5 D2 and AISI Sol D2 both made documented, leaving unknown cells only in OpenAI. C3 and C4 become true with one flip: Artifactory D1 made documented. C1 cannot change under an operation restricted to documented/unknown flips.

The exhaustive single-flip check covers all 45 cells (`single_flip_check.csv`). No single flip changes C1, C2, C5 or C6; making Artifactory D1 documented makes C3 and C4 true.

The illustrative weak-support scenario sets six documented cells unknown: OpenAI May D4, Artifactory D5, Opus 4.6 D2, Anthropic internal-model D2, AISI Sol D4 and AISI Sol D5. It gives **34 documented and 11 unknown decisions**; no tracked proposition changes. These six named operations replace the earlier 33/12 scenario. The selection is a diagnostic scenario rather than an empirical finding about which tags are wrong.

Table VIII: Scope of sensitivity analyses.

| Analysis | Operation and available basis | Reporting boundary |
|---|---|---|
| Rule variants | Apply Table III requirements to the same 45 cells | Reported with rules and counts |
| Leave-one-source-out | Remove one reference; retain core propositions supported by a remaining qualifying reference | Counts describe documentary dependence |
| Status-flip diagnostics | Distinct-cell documented/unknown flips, up to four flips | Hypothetical; propositions, operations and minimum sets specified |
| Weak-support scenario | Six named documented cells set to unknown | Illustrative selection, not a finding |
| Organization structure | Distinguish unit coverage, partial support and whole-proposition support | Only three of nine units have documents from two organizations; six cannot meet S2 by construction |

The organization analysis is released in `org_structure.csv`; having two organizations report on a unit is separate from having two support a cell’s whole proposition.

S6 separates status provenance from current passage and level annotations. Its 37 documented/eight unknown count is not a human endorsement of the current evidence fields or effect tree. D4 and D5 each retain seven documented cells under S6. Whole-proposition support from two organizations falls from one cell under S0/S1 to zero under S6 because the R02 addition to Hugging Face D4 came from the lead’s later re-read. The same-document AI re-check remains a consistency check, not validation.

## Appendix F. Bounded External Concordance

Raftari’s OpenAI reconstruction describes the May precursor signals, Artifactory privilege escalation and response, and subsequent Hugging Face compromise (§§4.1–4.2, p.4). These passages overlap substantively with our OpenAI units and draw on the same R02 report. We report this narrative overlap without a numerical cell-concordance claim. Silence on Artifactory external connectivity does not establish its absence. [@raftari2026from, §§4.1–4.2, p.4]

The released `bouke_concordance_count.json` tallies 11 comparison rows in `external_concordance.csv`: four labelled match, two not comparable and five unaligned. Two match labels refer to prose (§5.1, p.6), and two to Table 1 (p.7). These are recorded comparison labels, not verified substantive concordance: aligned source passages and comparison rows were not supplied together for citation-fit confirmation. The extraction’s interleaved table lines further limit alignment. Bouke’s aggregate OpenAI row also differs in granularity from our May, Artifactory and Hugging Face units. We therefore report no verified Bouke agreement count or rate. [@bouke2026competing]

Agreement between narratives based on shared first-party sources supplies no independent validation.
