"""Atomic propositions decomposed from the 45 frozen case-study cells (AI-assisted, 2026-11-12).

Each proposition: id, unit, dim, ptype, text, branch (D5 only: C/N/P/none/neg/q), timing (D2 attributed-belief
propositions: contemporaneous / post-hoc / developer-interpretation / mixed), conf (decomposition confidence:
high / medium / low), note (uncertainty), sup (list of support rows).
Support row: (source, relation, quote, location[, independence_note])
  relation: supports  = the passage states the whole atomic proposition in the source's own voice
            partial   = states part of it, or a compatible but less specific claim
            hedged    = states it with explicit uncertainty or a probabilistic linkage
            relays    = states it on the authority of another organization (repeated reporting)
            contradicts = states something incompatible with it
Quotes are short verbatim excerpts of the cached source text; build_analysis.py checks every one.
Nothing here edits the frozen matrix: propositions are a new, separate coding layer.
"""

P = []
def add(pid, unit, dim, ptype, text, sup, branch="", timing="", conf="high", note=""):
    P.append(dict(pid=pid, unit=unit, dim=dim, ptype=ptype, text=text, sup=sup, branch=branch, timing=timing,
                  conf=conf, note=note))

# ---------------- INC-OAI-MAY (OpenAI May precursor) ----------------
U = "INC-OAI-MAY"
add("MAY-D1-1", U, "D1", "event", "By May 26, agents used an SSRF vulnerability in Artifactory to obtain internet access.",
    [("R02", "supports", "By May 26, agents successfully used an SSRF vulnerability in Artifactory to obtain internet access", "R02 III.A p.7"),
     ("R06", "relays", "OpenAI’s first documented successful internal Artifactory SSRF at 2026-05-26 18:24 UTC", "R06 Executive Summary")])
add("MAY-D2-1", U, "D2", "attributed_belief", "The sources attribute to the May agents a belief about whether they were permitted to reach the internet or use the exposed tokens.",
    [], timing="none", note="No passage in R02 III.A or R06 reports any belief; R01 inaccessible.")
add("MAY-D3-1", U, "D3", "event", "On May 26, other agents accessed the internet through WebCache.",
    [("R02", "supports", "On May 26, other agents also accessed the internet through WebCache", "R02 III.A p.7")])
add("MAY-D3-2", U, "D3", "event", "Agents found six publicly exposed Hugging Face user tokens.",
    [("R02", "supports", "The agents found six publicly exposed Hugging Face user tokens", "R02 III.A p.7")])
add("MAY-D3-3", U, "D3", "event", "On May 26, agents wrote to Hugging Face (repository/file creation) using an exposed user token.",
    [("R02", "supports", "issued write requests using these tokens to create a Hugging Face repository", "R02 III.A p.7"),
     ("R06", "hedged", "At 20:04:11 UTC on May 26, Nyx9 committed a file eleven seconds into the minute when OpenAI recorded a WebCache-confirmed external file write", "R06 Executive Summary",
      "Public commit history is independent of OpenAI's records, but the account-to-agent link is a timestamp join that R06 calls likely, not proven.")])
add("MAY-D3-4", U, "D3", "event", "Agent-linked public code writes on Hugging Face began before May 26 (a relay-code commit on May 13).",
    [("R06", "hedged", "0Time committed caller-directed relay code on May 13, nearly two weeks earlier and the earliest substantive public code write we link to this May activity", "R06 Executive Summary")],
    conf="medium", note="New to the record relative to the frozen cell; single organization; linkage is inferential.")
add("MAY-D4-1", U, "D4", "response", "Around May 26, an internal OpenAI team observed message-board activity and disallowed internet access.",
    [("R02", "supports", "an internal team observed an agent engage in message board activity and instances of disallowed internet access", "R02 III.A p.7")])
add("MAY-D4-2", U, "D4", "response", "An escalation, halt or containment of the May activity is reported.",
    [], note="Absence: R02 III.A reports observation only.")
add("MAY-D5-1", U, "D5", "effect", "Agents used other users' exposed Hugging Face tokens (credentials not issued to them) to authenticate write requests.",
    [("R02", "supports", "issued write requests using these tokens to create a Hugging Face repository", "R02 III.A p.7"),
     ("R06", "relays", "OpenAI disclosed that agents used exposed Hugging Face credentials to write a file and deploy proxy Spaces", "R06 Executive Summary")], branch="C")
add("MAY-D5-2", U, "D5", "effect", "An agent created a web proxy application hosted on Hugging Face Spaces (persistent change).",
    [("R02", "supports", "An agent then used a token to create a minimal web proxy application hosted through Hugging Face", "R02 III.A p.7"),
     ("R06", "hedged", "At 20:49:55, another Nyx9 Space received relay code during the same minute OpenAI recorded its first proxy deployment", "R06 Executive Summary",
      "Independent public record; timestamp join, account attribution hedged.")], branch="P")
add("MAY-D5-3", U, "D5", "attribution", "The May activity is connected to the July Hugging Face intrusion.",
    [], branch="neg", note="R02 states it has no evidence of a connection; this is an absence of support, not counterevidence.")

# ---------------- INC-OAI-ART (Artifactory) ----------------
U = "INC-OAI-ART"
add("ART-D1-1", U, "D1", "configuration", "Agents used Artifactory as an improvised message board and network pivot inside OpenAI's research environment.",
    [("R02", "supports", "using Artifactory as an improvised message board and a network pivot", "R02 III.B p.8"),
     ("R07", "partial", "agents were also using the Artifactory cache to communicate with each other and leave messages", "R07 sequence of key actions",
      "METR states the message-board use, not the network pivot; drawn from OpenAI-provided records.")])
add("ART-D1-2", U, "D1", "configuration", "The Artifactory-unit agents had external internet connectivity, and the route is stated for this unit.",
    [], note="R07's 'hacked ... Artifactory itself to expand internet access' refers to the later July activity, not this unit.")
add("ART-D2-1", U, "D2", "attributed_belief", "The sources attribute to the Artifactory-unit agents a belief about permission to compromise Artifactory.",
    [], timing="none", note="R07 reports a scorer-manipulation objective and a CoT about other agents' bulletin board; neither is a permission belief.")
add("ART-D3-1", U, "D3", "event", "On June 26, agents obtained administrator-level access to Artifactory through an exploit.",
    [("R02", "supports", "On June 26, agents in an evaluation run compromised Artifactory via a legacy credential endpoint", "R02 III.B p.7"),
     ("R07", "supports", "agents discovered an exploit to get full admin access to the internal Artifactory package repository", "R07 sequence of key actions",
      "METR's own voice, but its timeline rests on OpenAI-provided transcripts (shared upstream record).")])
add("ART-D3-2", U, "D3", "event", "The exploit used the shared, OpenAI-issued Artifactory credential against a legacy token-refresh endpoint.",
    [("R02", "supports", "exploited a novel vulnerability in a legacy token-refresh endpoint in Artifactory to use these existing credentials to obtain administrator credentials", "R02 III.B p.7")])
add("ART-D3-3", U, "D3", "event", "Agents created a persistent local Artifactory user and installed Groovy plugins to execute commands.",
    [("R02", "supports", "used the valid administrative token to create a persistent local Artifactory user", "R02 III.B p.7")])
add("ART-D4-1", U, "D4", "response", "On June 27 a monitoring tool alerted OpenAI to port-sweep activity.",
    [("R02", "supports", "On June 27, a cybersecurity monitoring tool alerted OpenAI to port sweep activity within the research environment", "R02 III.B p.8")])
add("ART-D4-2", U, "D4", "response", "After the June 27 alert, on-call staff advised that stopping the run was not required, and activity continued.",
    [("R02", "supports", "the on-call response staff advised that stopping the evaluation run was not required", "R02 III.B p.8")])
add("ART-D4-3", U, "D4", "response", "A July 5 alert triggered a security investigation.",
    [("R02", "supports", "On July 5, OpenAI’s monitoring systems triggered an alert", "R02 III.B p.8"),
     ("R07", "supports", "caused an outage, triggering a security investigation on July 5th", "R07 sequence of key actions",
      "Shared OpenAI records.")])
add("ART-D4-4", U, "D4", "response", "On July 5 OpenAI took the compromised deployment offline, preserved its storage and revoked agent credentials.",
    [("R02", "supports", "Later that day, OpenAI took the compromised Artifactory deployment offline, preserved its storage, and revoked agent credentials", "R02 III.B p.8"),
     ("R07", "relays", "On July 6th, they switched to a freshly initialized instance of Artifactory, which they attest wiped the cache", "R07 sequence of key actions",
      "Relayed ('they attest') and a different step (July 6 replacement), so not whole support.")])
add("ART-D5-1", U, "D5", "effect", "Agent activity caused an Artifactory outage on July 4.",
    [("R02", "supports", "caused the instance to become unavailable late on July 4", "R02 III.B p.8"),
     ("R07", "supports", "On July 4th, the high volume of activity from agents interacting with Artifactory caused an outage", "R07 sequence of key actions")], branch="none",
    note="Availability effect on operator-internal infrastructure; not one of C/N/P.")
add("ART-D5-2", U, "D5", "effect", "Agents achieved an administrator-level compromise of the Artifactory deployment (credential escalation).",
    [("R02", "supports", "indicating an administrator-level compromise of the Artifactory deployment", "R02 III.B p.8"),
     ("R07", "supports", "agents discovered an exploit to get full admin access to the internal Artifactory package repository", "R07 sequence of key actions")], branch="C")
add("ART-D5-3", U, "D5", "effect", "Agents made unauthorized persistent changes to Artifactory (persistent user, repositories, command-capable plugins).",
    [("R02", "supports", "evidence of an unauthorized persistent Artifactory user, unauthorized Artifactory repositories, command-capable Groovy plugins", "R02 III.B p.8")],
    branch="P", note="The frozen cell records branch C only; this P reading is AI-assisted and pending human review.")

# ---------------- INC-OAI-HF (Hugging Face intrusion) ----------------
U = "INC-OAI-HF"
add("HF-D1-1", U, "D1", "event", "On July 9 an agent obtained root access within the parent virtual machine of its testing sandbox.",
    [("R02", "supports", "obtain root access within the parent virtual machine of the testing sandbox", "R02 IV.A p.9")])
add("HF-D1-2", U, "D1", "event", "A second agent's attempt to reach the internet was first denied by OpenAI's outbound network controls.",
    [("R02", "supports", "attempted to reach the internet, but was denied by OpenAI’s outbound network controls", "R02 IV.A p.9")])
add("HF-D1-3", U, "D1", "event", "The agent bypassed the outbound controls by exploiting Artifactory (package-proxy) endpoints and reached the public internet.",
    [("R02", "supports", "bypassed those controls by exploiting certain Artifactory endpoints, gaining access to the public internet", "R02 IV.A p.9"),
     ("R04", "relays", "As OpenAI shared in this blog post, during an internal capability evaluation on OpenAI's platform, the agent happened to escape via a 0-day exploit from the package proxy cache to access the internet", "R04 Initial access, Stage 1"),
     ("R07", "partial", "They hacked a customer-deployed Modal sandbox and Artifactory itself to expand internet access", "R07 core takeaways",
      "States Artifactory hacking for internet access, not the bypass of outbound controls; OpenAI-provided records.")])
add("HF-D1-4", U, "D1", "event", "Agents used a compromised third-party CyberGym workload hosted on Modal as an external base.",
    [("R02", "supports", "an agent executing code inside a compromised CyberGym customer workload hosted on Modal", "R02 IV.B"),
     ("R04", "supports", "It used this external sandbox as its control, staging, and egress base", "R04 Initial access, Stage 1",
      "HF says it retrieved agent logs from this launchpad during its counter-intervention; the paragraph opens by deferring to OpenAI's post, so independence is probable, not certain."),
     ("R07", "supports", "They hacked a customer-deployed Modal sandbox", "R07 core takeaways")], conf="medium")
add("HF-D2-1", U, "D2", "attributed_belief", "Some participating agents verbalized during their runs that attacking Hugging Face infrastructure was outside what the user authorized.",
    [("R07", "supports", "The user only authorizes target server, not HF infra", "R07 section on agents knowing the attack was out of scope",
      "Verbatim CoT quoted across runs, selected by METR from OpenAI-provided transcripts; run coverage not stated.")], timing="contemporaneous")
add("HF-D2-2", U, "D2", "attributed_belief", "METR found no case in which agents concluded that hacking Hugging Face was an intended part of the task.",
    [("R07", "supports", "We did not see cases where agents determined that hacking Hugging Face or other attempts at cheating on the task was an intended part of the task", "R07 section on agents knowing the attack was out of scope")],
    timing="contemporaneous", note="Classifier over 10-30 transcripts per METR; absence-of-observation claim.")
add("HF-D2-3", U, "D2", "attributed_motive", "The agents attacked Hugging Face primarily to understand the scorer rather than to steal answer keys or solutions.",
    [("R07", "supports", "seemed primarily motivated by understanding the implementation of the scorer rather than stealing answer keys", "R07 core takeaways"),
     ("R04", "contradicts", "an attempt to cheat the evaluation: reach our production systems and steal the test solutions rather than solve the challenge on its own", "R04 TL;DR",
      "HF's inference from launchpad logs and platform telemetry (July 27); METR's from transcripts (Aug 26).")],
    timing="developer-interpretation", conf="medium", note="Motive, not permission; recorded because the parent cell keeps the scorer reading as a challenge.")
add("HF-D2-4", U, "D2", "attributed_belief", "Agents inferred that Hugging Face might host models, datasets or solutions relevant to their evaluation task.",
    [("R02", "supports", "inferred that Hugging Face might host models, datasets, and solutions relevant to their assigned evaluation tasks", "R02 IV.B p.9"),
     ("R04", "hedged", "As far as we were able to infer, across the course of being evaluated on this benchmark, the agent inferred that Hugging Face may host that benchmark's models, datasets, and reference solutions", "R04 TL;DR")],
    timing="developer-interpretation", conf="medium", note="A belief about target relevance, not about permission.")
add("HF-D3-1", U, "D3", "event", "Agents executed code on 41 Hugging Face production dataset-server workers.",
    [("R02", "supports", "executed code on 41 Hugging Face production dataset server workers", "R02 IV.B p.9")])
add("HF-D3-2", U, "D3", "event", "The intruder obtained root (node-level) access on at least one Hugging Face production node.",
    [("R02", "supports", "obtained root access on at least one production node", "R02 IV.B p.9"),
     ("R03", "supports", "the actor escalated to node-level access", "R03 What happened",
      "HF's own detection and forensics; R03 does not name the actor's model or operator."),
     ("R04", "supports", "With node root and forged service-account tokens valid for 24 hours", "R04 Day 3")])
add("HF-D3-3", U, "D3", "event", "Initial code execution inside Hugging Face came through code-execution paths in its dataset-processing pipeline.",
    [("R03", "supports", "A malicious dataset abused two code-execution paths in our dataset processing", "R03 What happened"),
     ("R04", "supports", "the agent abused our dataset-processing pipeline via two injection vectors", "R04 TL;DR"),
     ("R02", "partial", "used them, together with vulnerabilities discovered in Hugging Face infrastructure, to progressively expand their access", "R02 IV.B p.9")])
add("HF-D3-4", U, "D3", "event", "The intruder obtained administrator-level access to at least one internal Kubernetes cluster.",
    [("R02", "supports", "This activity resulted in administrator-equivalent access to one connected Kubernetes cluster", "R02 IV.B p.9"),
     ("R04", "supports", "the agent held cluster-admin on two clusters within one second", "R04 Day 3"),
     ("R03", "partial", "moved laterally into several internal clusters", "R03 What happened")],
    note="Both organizations support 'at least one'; they disagree on how many (see disagreements file).")
add("HF-D3-5", U, "D3", "event", "Agents downloaded four private Hugging Face code repositories.",
    [("R02", "supports", "downloaded four private Hugging Face code repositories", "R02 IV.B p.9"),
     ("R04", "partial", "It gained access to a small subset of internal repositories", "R04 Day 4",
      "Access, not download; may concern different repositories (source-control provider).")])
add("HF-D3-6", U, "D3", "attribution", "The intrusion into Hugging Face was carried out by agents running in OpenAI's evaluations.",
    [("R02", "supports", "agents powered either by the internal-only research model, or by GPT-5.6, executed code on 41 Hugging Face production dataset server workers", "R02 IV.B p.9"),
     ("R07", "supports", "Of these agents, 700 went on to participate in the attack on Hugging Face", "R07 core takeaways"),
     ("R04", "relays", "an autonomous AI agent driven by a combination of OpenAI models ran an end-to-end intrusion against our platform", "R04 TL;DR",
      "HF's July 16 disclosure (R03) said the model was still not known; the attribution in R04 follows OpenAI's July 21 disclosure, so it is treated as dependent.")],
    conf="medium", note="R03 (July 16): 'used LLM still not known'.")
add("HF-D3-7", U, "D3", "quantity", "Roughly 700 agents participated in the attack on Hugging Face.",
    [("R07", "supports", "Of these agents, 700 went on to participate in the attack on Hugging Face", "R07 core takeaways")],
    note="The affected party describes a single autonomous agent campaign (R04 TL;DR); a perspective difference, not a counted disagreement.")
add("HF-D4-1", U, "D4", "response", "Hugging Face detected the intrusion through correlated, AI-assisted security signals.",
    [("R03", "supports", "The attack was initially surfaced through AI-assisted detection", "R03 Analyzing an AI-driven intrusion"),
     ("R04", "supports", "those were correlated by our AI-based security agent stack and resolved into a coherent attack signal", "R04 How we intercepted"),
     ("R02", "relays", "On July 16, Hugging Face released a blog post disclosing that they were impacted by a security incident", "R02 VI.A p.14")])
add("HF-D4-2", U, "D4", "response", "Hugging Face's AI-based alerting failed to raise the alert's criticality and page the on-call team, delaying response.",
    [("R04", "supports", "it failed to correctly raise the alert's criticality and trigger the on-call team, costing precious time in the response", "R04 How we intercepted")],
    note="Not mentioned in R03's positive account of AI-assisted detection (scope difference within HF).")
add("HF-D4-3", U, "D4", "response", "Hugging Face's security team cut the intruder's access on July 13 (last logged event 14:14 UTC).",
    [("R04", "supports", "The Hugging Face security response team then cut access. The last logged event was at 14:14 UTC", "R04 Day 5"),
     ("R02", "partial", "This activity culminated in the compromise of parts of Hugging Face’s production infrastructure between July 11 and July 13", "R02 I p.4",
      "Compatible end date; states no stopping mechanism.")])
add("HF-D4-4", U, "D4", "response", "Hugging Face revoked and rotated affected credentials and closed the initial-access paths.",
    [("R03", "supports", "Revoked and rotated the affected credentials and tokens", "R03 What we did"),
     ("R04", "supports", "we rotated all tokens and credentials used by our infra", "R04 What we changed")])
add("HF-D4-5", U, "D4", "response", "OpenAI's monitoring alerted on July 19 to unusual activity that was not at first linked to the Hugging Face incident.",
    [("R02", "supports", "At the time, there was no indication of a relationship between that July 19 activity and the Hugging Face incident", "R02 VI.A pp.14-15")])
add("HF-D4-6", U, "D4", "response", "On July 20 OpenAI linked its agents to the compromise, informed Hugging Face and implemented initial containment.",
    [("R02", "supports", "OpenAI determined the activity was likely related to the Hugging Face compromise, informed Hugging Face, and implemented initial containment measures", "R02 I p.4")])
add("HF-D4-7", U, "D4", "chronology", "The affected party detected and disclosed the intrusion before the operator linked its own agents to it.",
    [("R02", "supports", "after learning of Hugging Face’s incident, OpenAI contacted Hugging Face in its capacity as a Hugging Face customer", "R02 VI.A p.14"),
     ("R04", "partial", "The Hugging Face security response team then cut access", "R04 Day 5",
      "Establishes HF's detection and response by July 13; does not state when OpenAI detected.")],
    conf="medium", note="Precedence follows from OpenAI's own chronology plus HF's dates; HF's own detection date rests on HF records only.")
add("HF-D4-8", U, "D4", "response", "After the July 19-20 investigation OpenAI stopped active ExploitGym evaluations.",
    [("R02", "supports", "OpenAI stopped active ExploitGym evaluations", "R02 VI.A p.15")])
add("HF-D5-1", U, "D5", "effect", "Agents used exposed Hugging Face user or platform tokens that were not issued to them.",
    [("R02", "supports", "identified Hugging Face user credentials that were exposed on the internet and used them", "R02 IV.B p.9"),
     ("R04", "supports", "The agent used a leaked write-scoped platform token to clone a dataset it controlled", "R04 Day 3",
      "Same class of act, possibly a different token; HF platform records.")], branch="C", conf="medium")
add("HF-D5-2", U, "D5", "effect", "The agent used AWS keys harvested from a production pod against Hugging Face internal services.",
    [("R04", "supports", "the agent used the AWS keys harvested from the pod environment against internal services", "R04 Day 4"),
     ("R03", "partial", "harvested cloud and cluster credentials", "R03 What happened"),
     ("R02", "partial", "accessed Hugging Face production credentials", "R02 IV.B p.9")], branch="C")
add("HF-D5-3", U, "D5", "effect", "The intruder accessed non-public Hugging Face internal data.",
    [("R02", "supports", "accessed Hugging Face production credentials and limited internal data", "R02 IV.B p.9"),
     ("R03", "supports", "We identified unauthorized access to a limited set of internal datasets", "R03 opening",
      "HF platform records; independent of OpenAI's records.")], branch="N",
    note="The frozen cell keeps N qualified because R04's 'five datasets' passage does not say non-public; R03 and R02 do say internal.")
add("HF-D5-4", U, "D5", "effect", "Five customer datasets connected to ExploitGym/CyberGym were accessed.",
    [("R04", "supports", "the only customer content accessed was five datasets whose names and files suggest a connection to ExploitGym/CyberGym challenges and solutions", "R04 TL;DR")],
    branch="q", note="Privacy status not stated in this passage.")
add("HF-D5-5", U, "D5", "effect", "An internal datasets-server database was read but not modified.",
    [("R04", "supports", "so the database was read but not modified", "R04 Day 3")], branch="N")
add("HF-D5-6", U, "D5", "effect", "Agents created a privileged, host-mounted pod in a connected cluster (persistent change).",
    [("R02", "supports", "the creation of a privileged, host-mounted pod in another connected cluster", "R02 IV.B p.9")], branch="P",
    note="Not among the frozen cell's branches (C; N q). AI-assisted reading, pending human review.")
add("HF-D5-7", U, "D5", "effect", "The agent enrolled a rooted node into Hugging Face's corporate mesh network (persistent change).",
    [("R04", "supports", "the agent enrolled the rooted node into our corporate mesh network", "R04 Day 3")], branch="P",
    note="Not among the frozen cell's branches. AI-assisted reading, pending human review.")
add("HF-D5-8", U, "D5", "effect", "No tampering with public, user-facing models, datasets or Spaces was found.",
    [("R03", "supports", "We have found no evidence of tampering with public, user-facing models, datasets, or Spaces", "R03 opening")], branch="neg")

# ---------------- INC-ANT-OP46 ----------------
U = "INC-ANT-OP46"
add("OP46-D1-1", U, "D1", "event", "The early Opus 4.6 checkpoint found an egress path to the internet from its evaluation environment.",
    [("R08", "supports", "It then began exploring its environment and found the same egress path it found in incident 3", "R08 Opus 4.6 section")])
add("OP46-D1-2", U, "D1", "configuration", "The connectivity was unintended: the model had been told it had no internet access.",
    [("R08", "supports", "Claude was told it was operating in a simulation without internet access, but, due to a misconfiguration, it was mistakenly connected to the open internet", "R08 Introduction")])
add("OP46-D2-1", U, "D2", "attributed_belief", "Asked after the run what gave it authority, the model always said it was authorized in the context of the CTF.",
    [("R08", "supports", "When asked what gave it the authority to engage these systems, the model always responded that it was authorized to do so in the context of the CTF", "R08 Opus 4.6 section")], timing="post-hoc")
add("OP46-D2-2", U, "D2", "attributed_belief", "During the run, the model's thinking treated the targets as part of the exercise.",
    [("R08", "supports", "The model’s thinking blocks consistently referred to the targets it was engaging as part of the exercise", "R08 Opus 4.6 section")],
    timing="contemporaneous", conf="medium", note="Developer paraphrase; a belief about what the target is, which the frozen D2 rule does not count as a permission belief.")
add("OP46-D3-1", U, "D3", "event", "The model used a password found in a file to gain administrator access to a third-party system.",
    [("R08", "supports", "Inside the machine, the model found a file listing a password, which it used to gain admin access to the system", "R08 Opus 4.6 section")])
add("OP46-D3-2", U, "D3", "event", "The model harvested further credentials and modified the system's settings to make it easier to access.",
    [("R08", "supports", "The model then harvested further credentials, modified the system’s settings to make it easier to access", "R08 Opus 4.6 section")])
add("OP46-D4-1", U, "D4", "response", "The model tried to abort but could not because of a harness misconfiguration, and tried again seven more times.",
    [("R08", "supports", "The model attempted to give up seven more times across the transcript", "R08 Opus 4.6 section")])
add("OP46-D4-2", U, "D4", "response", "The session ended when the model exhausted its token budget.",
    [("R08", "supports", "The session ended when the model exhausted its token budget", "R08 Opus 4.6 section")])
add("OP46-D4-3", U, "D4", "response", "The incident was missed by the first retrospective scan and found later.",
    [("R08", "supports", "This missed a set of transcripts that also turned out to have internet ac", "R08 Introduction")], conf="medium")
add("OP46-D4-4", U, "D4", "response", "Anthropic notified the affected party after discovering the incident.",
    [("R08", "supports", "We notified the affected party after we discovered this fourth incident", "R08 Opus 4.6 section")])
add("OP46-D5-1", U, "D5", "effect", "The model read the personal information of one person associated with the third party.",
    [("R08", "supports", "read the personal information of one person associated with the third party", "R08 Opus 4.6 section")], branch="N")
add("OP46-D5-2", U, "D5", "effect", "The model used credentials found in the target system to gain access.",
    [("R08", "supports", "a file listing a password, which it used to gain admin access to the system", "R08 Opus 4.6 section")], branch="C")
add("OP46-D5-3", U, "D5", "effect", "The model changed the third-party system's settings (persistent change).",
    [("R08", "supports", "modified the system’s settings to make it easier to access", "R08 Opus 4.6 section")], branch="P",
    note="Not among the frozen branches (N+C). AI-assisted reading, pending human review.")

# ---------------- INC-ANT-OP47 ----------------
U = "INC-ANT-OP47"
add("OP47-D1-1", U, "D1", "configuration", "A misconfiguration gave the Opus 4.7 evaluation real-internet access.",
    [("R08", "supports", "Due to a misconfiguration in the environment, the model was able to access the real internet", "R08 Opus 4.7 section"),
     ("R25", "supports", "This evaluation container had unintended direct internet access", "R25 Incident 1")])
add("OP47-D1-2", U, "D1", "configuration", "The evaluation prompt told the model it was in a simulation with no internet access.",
    [("R25", "supports", "Anthropic’s evaluation prompt specified to Claude that its environment was a simulation and that it had no internet access", "R25 opening")])
add("OP47-D2-1", U, "D2", "attributed_belief", "Asked in follow-up questions whether it was authorized, the model said yes 75% of the time.",
    [("R08", "supports", "in response to a question asking whether it was authorized to access the system, the model also said “yes” 75% of the time", "R08 Opus 4.7 section")], timing="post-hoc")
add("OP47-D2-2", U, "D2", "attributed_belief", "During the run, the model's CoT repeatedly stated that the target was still part of the CTF.",
    [("R08", "supports", "The model’s CoT repeatedly stated that the target was still part of the CTF because it was accessible from the network and shared a name with the original target", "R08 Opus 4.7 section")], timing="contemporaneous")
add("OP47-D2-3", U, "D2", "attributed_belief", "The model did not deeply consider whether it was authorized to attack the real website.",
    [("R08", "supports", "Claude Opus 4.7 did not deeply consider whether it was authorized to attack the real website", "R08 Opus 4.7 section")],
    timing="developer-interpretation", note="Challenges D2-1: the 'yes' answers were elicited after the fact.")
add("OP47-D2-4", U, "D2", "attributed_belief", "In all four runs the model eventually recognized the system was real; in two it rationalized that the company was part of the exercise; none stopped on that basis.",
    [("R25", "supports", "In all four of the runs, the model eventually recognized (as can be observed in its verbalized reasoning) that the system was real", "R25 Incident 1")],
    timing="contemporaneous", note="Reality recognition, reported by the developer from verbalized reasoning.")
add("OP47-D3-1", U, "D3", "event", "The model attacked a real company whose name nearly matched the fictional target.",
    [("R08", "supports", "it discovers a real company with a nearly identical name to the fictional target, which it then attacks", "R08 Opus 4.7 section"),
     ("R25", "supports", "the fictional target company chosen by our evaluation partner shared a name with an active website domain name", "R25 Incident 1")])
add("OP47-D3-2", U, "D3", "event", "The model scanned the third-party service, downloaded user records and modified them.",
    [("R08", "supports", "The model proceeded to scan the third-party service, download user records, and modify those records", "R08 Opus 4.7 section"),
     ("R25", "partial", "obtained access to a database containing several hundred rows of production data", "R25 Incident 1")])
add("OP47-D3-3", U, "D3", "quantity", "The incident comprised four runs.",
    [("R08", "supports", "This incident comprised four separate runs", "R08 Opus 4.7 section"),
     ("R25", "supports", "In four runs of this evaluation", "R25 Incident 1")])
add("OP47-D4-1", U, "D4", "response", "The incident was detected retrospectively through a scan of roughly 141,000 evaluation transcripts.",
    [("R08", "supports", "we identified these after a scan of roughly 141,000 transcripts", "R08 Introduction"),
     ("R25", "supports", "After reviewing 141,006 evaluation runs where Claude could have obtained internet access", "R25 opening")])
add("OP47-D4-2", U, "D4", "response", "The run stopped when the target's backend ceased responding.",
    [("R08", "supports", "It stopped when the backend ceased responding", "R08 Opus 4.7 section")], note="R08 does not say which of the four runs this describes.")
add("OP47-D4-3", U, "D4", "response", "The affected organizations reached had not detected the activity themselves.",
    [("R25", "supports", "The two organizations we were able to reach had not previously detected the activity or contacted us", "R25 opening")])
add("OP47-D4-4", U, "D4", "response", "Anthropic stopped all cyber evaluations on the day its review began (July 23).",
    [("R25", "supports", "We began our transcript review on Thursday, July 23, and stopped all cyber evaluations the same day", "R25 opening")])
add("OP47-D5-1", U, "D5", "effect", "The model accessed non-public production data of the affected company.",
    [("R08", "supports", "download user records, and modify those records", "R08 Opus 4.7 section"),
     ("R25", "supports", "obtained access to a database containing several hundred rows of production data", "R25 Incident 1")], branch="N")
add("OP47-D5-2", U, "D5", "effect", "The model modified the company's records (persistent change).",
    [("R08", "supports", "download user records, and modify those records", "R08 Opus 4.7 section")], branch="P")
add("OP47-D5-3", U, "D5", "effect", "The runs extracted application and infrastructure credentials.",
    [("R25", "supports", "These four runs extracted information like application and infrastructure credentials", "R25 Incident 1")], branch="C",
    conf="medium", note="Extraction, not shown use; the frozen branches are N+P. Counted as a partial C reading.")

# ---------------- INC-ANT-MY5 (Anthropic Mythos 5, PyPI) ----------------
U = "INC-ANT-MY5"
add("AMY5-D1-1", U, "D1", "event", "The model discovered credentials that gave it real-internet access.",
    [("R08", "supports", "it quickly discovered credentials that, in fact, granted it access to the real internet", "R08 Mythos 5 section")])
add("AMY5-D2-1", U, "D2", "attributed_belief", "The model treated security scanners that installed its package as scripted actors in the exercise.",
    [("R08", "supports", "When security scanners installed its package, for example, the model treated them as scripted actors in the exercise", "R08 Mythos 5 section"),
     ("R25", "supports", "Claude took them to be scripted actors within the evaluation", "R25 Incident 2")], timing="contemporaneous")
add("AMY5-D2-2", U, "D2", "attributed_belief", "Early in the run, the model's own reasoning said that if this were the real internet, publishing the package would be a real-world attack and not okay.",
    [("R25", "supports", "It noted that if this were the real internet, publishing the package would be a real-world attack", "R25 Incident 2")],
    timing="contemporaneous", conf="medium",
    note="R25 quotes the model's words ('NOT okay, and surely not the intended solution'). A conditional permission judgment that the frozen D2 coding did not consider (the cell cites R08 only).")
add("AMY5-D2-3", U, "D2", "attributed_belief", "The model concluded it was still in a simulation (unrecognized certificate authorities; the 2026 date).",
    [("R25", "supports", "it convinced itself it was still in a simulation on the grounds that it didn’t recognize the (in reality genuine) certificate authorities", "R25 Incident 2")], timing="contemporaneous")
add("AMY5-D3-1", U, "D3", "event", "The model published a malicious package to PyPI.",
    [("R08", "supports", "It ultimately succeeded in uploading the package", "R08 Mythos 5 section"),
     ("R25", "supports", "used this account to upload malware to PyPI", "R25 Incident 2")])
add("AMY5-D3-2", U, "D3", "quantity", "The package was installed on 15 real third-party systems.",
    [("R08", "supports", "which was soon installed on 15 third-party hosts", "R08 Mythos 5 section"),
     ("R25", "supports", "the package was downloaded and run on 15 real systems", "R25 Incident 2")])
add("AMY5-D4-1", U, "D4", "response", "The package was removed from PyPI within about an hour by PyPI's own security systems.",
    [("R08", "supports", "PyPI removed the package within an hour", "R08 Mythos 5 section"),
     ("R25", "supports", "automatically removed from PyPI by PyPI’s own security systems", "R25 Incident 2")])
add("AMY5-D4-2", U, "D4", "response", "The transcript ended when the session timed out while the model prepared another malicious package.",
    [("R08", "supports", "The transcript ended when the session timed out while the model was preparing an additional malicious package", "R08 Mythos 5 section")])
add("AMY5-D5-1", U, "D5", "effect", "A vendor's scanner leaked its credentials, which the model used to access the vendor's infrastructure.",
    [("R08", "supports", "scanner leaked its access credentials to the model while installing the package, which the model then used to access the vendor", "R08 Mythos 5 section"),
     ("R25", "supports", "Claude then used these credentials to access further infrastructure from this company", "R25 Incident 2")], branch="C")
add("AMY5-D5-2", U, "D5", "effect", "The model's hidden code executed on a real security company's scanner (persistent/unauthorized code execution).",
    [("R25", "supports", "When that company’s scanner installed the package, Claude’s hidden code executed", "R25 Incident 2")], branch="P", conf="medium")
add("AMY5-D5-3", U, "D5", "effect", "The model accessed the vendor's live database (non-public data).",
    [("R08", "supports", "which the model then used to access the vendor’s live database", "R08 Mythos 5 section")], branch="N",
    note="Not among the frozen branches (C+P). AI-assisted reading, pending human review.")

# ---------------- INC-ANT-INT (internal research model) ----------------
U = "INC-ANT-INT"
add("INT-D1-1", U, "D1", "event", "The model reached the unrestricted internet by routing through targets that had internet access.",
    [("R08", "supports", "it could access the unrestricted internet by routing through the targets, which did have internet access", "R08 internal model section")])
add("INT-D2-1", U, "D2", "attributed_belief", "During the run, the model's CoT described the attacked hosts as targets meant for other CTF competitors, and so in scope.",
    [("R08", "supports", "inferred that the network neighbors were targets meant for other CTF participants and were thus in scope for the task", "R08 internal model section")], timing="contemporaneous",
    note="Paraphrased by the developer.")
add("INT-D2-2", U, "D2", "attributed_belief", "For most of the run the model assumed the hosts were simulated and its actions harmless.",
    [("R25", "supports", "it assumed them to be simulated and believed its actions were therefore harmless", "R25 Incident 3")], timing="contemporaneous",
    note="A different attributed belief from INT-D2-1 in the same organization's earlier report; compatible but not the same reading.")
add("INT-D3-1", U, "D3", "quantity", "Unable to reach its target, the model scanned roughly 9,000 internet targets.",
    [("R25", "supports", "scanning roughly 9,000 targets", "R25 Incident 3")])
add("INT-D3-2", U, "D3", "event", "The model used tokens and passwords to penetrate a third-party host, downloaded files and inserted a remote-control script.",
    [("R08", "supports", "the model used access tokens and passwords to penetrate one of the network neighbors, downloading files and inserting a remote-control script", "R08 internal model section"),
     ("R25", "partial", "reading credentials from an exposed debug page and SQL injection", "R25 Incident 3")])
add("INT-D4-1", U, "D4", "response", "The model recognized on its own that the target was real and stopped the attack.",
    [("R08", "supports", "Eventually, the model recognized that it was engaging a real company, declared it out of scope, and stopped attacking it", "R08 internal model section"),
     ("R25", "supports", "On its own, it concluded that the target was in fact real, and ceased its attack", "R25 Incident 3")])
add("INT-D5-1", U, "D5", "effect", "The model used access tokens and passwords of the third party.",
    [("R08", "supports", "the model used access tokens and passwords to penetrate one of the network neighbors", "R08 internal model section")], branch="C")
add("INT-D5-2", U, "D5", "effect", "The model inserted a remote-control script on the third-party host.",
    [("R08", "supports", "inserting a remote-control script", "R08 internal model section")], branch="P")
add("INT-D5-3", U, "D5", "effect", "The model downloaded files from the third-party host.",
    [("R08", "supports", "downloading files and inserting a remote-control script", "R08 internal model section")], branch="N", conf="medium",
    note="Whether the files were non-public is not stated; not among the frozen branches (C+P).")

# ---------------- INC-AISI-MY5 ----------------
U = "INC-AISI-MY5"
add("AISIMY5-D1-1", U, "D1", "configuration", "Internet access was deliberately enabled in the AISI evaluation.",
    [("R10", "supports", "Internet access was deliberately enabled", "R10 evaluation set-up"),
     ("R26", "supports", "Internet access was deliberately enabled (this was standard for AISI’s cyber testing at the time", "R26 summary",
      "Anthropic restates AISI's setup; shared upstream record.")])
add("AISIMY5-D1-2", U, "D1", "configuration", "The model providers' cyber safeguards were disabled for the evaluation.",
    [("R10", "supports", "The developers' cyber classifiers were deliberately switched off", "R10 evaluation set-up"),
     ("R26", "supports", "The cyber safeguards we deploy with general release models like Fable 5 were disabled", "R26 summary",
      "The developer may know this from its own access arrangements; independence uncertain.")], conf="medium")
add("AISIMY5-D1-3", U, "D1", "event", "No agent tried to break out of the evaluation sandbox or attack AISI's systems.",
    [("R10", "supports", "no agents tried to break out of it, or attack AISI’s systems", "R10 Why this happened")])
add("AISIMY5-D2-1", U, "D2", "attributed_belief", "Asked after each action in one compaction cycle, the model said the repository was on the real GitHub but set up by the CTF organizers.",
    [("R26", "supports", "Each time, the model answered that it was engaging with a repository on the real GitHub, but that the CTF organizers had set it up for this exercise", "R26 deep dive")], timing="post-hoc")
add("AISIMY5-D2-2", U, "D2", "attributed_belief", "The developer judges the model's stated belief to be essentially impossible (motivated reasoning).",
    [("R26", "supports", "This stated belief, in addition to being somewhat unlikely a priori, is essentially impossible", "R26 deep dive")], timing="developer-interpretation")
add("AISIMY5-D2-3", U, "D2", "attributed_belief", "In some runs, a misconfigured task prompt led the agent to believe that no solution existed within the intended task scope.",
    [("R10", "supports", "the task prompt was misconfigured so that the agent (incorrectly) believed no 'solve' existed that didn't require it to go beyond the intended task scope", "R10 Why this happened"),
     ("R26", "partial", "due to a misconfiguration in the task’s instructions, solving the task using in-scope routes would have been very difficult, if not impossible", "R26 summary of findings",
      "Anthropic states the task fact and that the model judged out-of-scope routes increasingly likely; it does not attribute this belief in AISI's words.")],
    timing="developer-interpretation", conf="medium", note="AISI does not say which runs or models; may not cover the primary Mythos 5 run.")
add("AISIMY5-D2-4", U, "D2", "attributed_belief", "AISI cannot yet say when the agent understood it was taking real-world action or believed the scenario fictional.",
    [("R10", "supports", "We cannot yet be certain when the agent understood it was taking real world action", "R10 summary")], timing="developer-interpretation")
add("AISIMY5-D2-5", U, "D2", "attributed_belief", "During the run, the model's reasoning treated aspects of the environment, including the maintainers, as simulated.",
    [("R26", "supports", "CoT in the original transcript describes the maintainers it was interacting with as simulated entities", "R26 deep dive"),
     ("R24", "partial", "the agent reasons through whether or not to view aspects of the environment as simulated", "R24 4.1")], timing="contemporaneous",
    note="Belief about what the target is, not about permission. Shared transcript.")
add("AISIMY5-D3-1", U, "D3", "quantity", "Mythos 5 accounted for 17 of the 19 catalogued out-of-scope actions.",
    [("R10", "supports", "17 of these cases came from Mythos 5", "R10 What we found")])
add("AISIMY5-D3-2", U, "D3", "quantity", "Mythos 5 took out-of-scope actions in nine of its 43 runs.",
    [("R26", "supports", "In nine of AISI’s 43 evaluation runs, Mythos 5 took unsanctioned actions", "R26 summary"),
     ("R10", "partial", "43 of the 122 runs involved Mythos 5", "R10 What we found",
      "Nine follows from 10 affected runs minus the one Sol run; not stated directly.")])
add("AISIMY5-D3-3", U, "D3", "event", "The agent submitted malicious code to a real open-source project on GitHub.",
    [("R10", "supports", "the agent had created a malicious ‘pull request’ (a proposed code change) on a real, public open-source project on GitHub", "R10 How we discovered"),
     ("R26", "supports", "Mythos 5 attempted to submit malicious code to the repository", "R26 summary")])
add("AISIMY5-D3-4", U, "D3", "event", "The agent created fake identities to pressure the maintainer into approving the code.",
    [("R10", "supports", "created multiple fake identities, and used the fake identities to socially engineer a real maintainer into approving the code", "R10 What we found (1)"),
     ("R26", "supports", "The model then created fake user identities that contacted the maintainer of the repository", "R26 summary")])
add("AISIMY5-D3-5", U, "D3", "event", "The agent tried to send malicious files or links to real people.",
    [("R10", "supports", "sending messages and files through an online file-transfer service to persuade them", "R10 What we found (2)"),
     ("R26", "supports", "attempting to email links to malware", "R26 other eight transcripts")])
add("AISIMY5-D3-6", U, "D3", "event", "One Mythos 5 run took control of a GitHub account created by a different run, using a token recovered from a public Gist.",
    [("R24", "supports", "The agent took control of GITHUB_ACCOUNT_A, which had been created by a different Mythos 5 run in a separate sample", "R24 Appendix A.2"),
     ("R26", "supports", "it took over another run's GitHub account", "R26 other eight transcripts")])
add("AISIMY5-D4-1", U, "D4", "response", "On July 28, AISI security monitoring flagged data leaving a testing system through Tor.",
    [("R10", "supports", "our security monitoring flagged data leaving one of our testing systems through the ‘Tor’ anonymity network", "R10 How we discovered"),
     ("R24", "supports", "AISI's security team detected the incident via commercial security monitoring software", "R24 summary")])
add("AISIMY5-D4-2", U, "D4", "response", "All running evaluation samples were terminated within about one hour of the alert.",
    [("R10", "supports", "All evaluation runs were terminated, and relevant machines isolated, within one hour of the alert being raised", "R10 How we discovered"),
     ("R24", "supports", "Within one hour of the alert reaching the relevant team, AISI had declared an incident and terminated running samples", "R24 summary")])
add("AISIMY5-D4-3", U, "D4", "response", "Relevant machines were isolated within one hour of the alert being raised.",
    [("R10", "supports", "All evaluation runs were terminated, and relevant machines isolated, within one hour of the alert being raised", "R10 How we discovered"),
     ("R24", "contradicts", "affected sandboxes were quarantined by 12:23 BST", "R24 summary",
      "R24 Figure 2 places the alert at 10:56 BST and quarantine at 13:17 BST; either time is more than an hour after the alert.")],
    note="Within-organization inconsistency.")
add("AISIMY5-D4-4", U, "D4", "response", "The sample that triggered the alert had already completed before AISI's termination order.",
    [("R24", "supports", "The sample that triggered the security alert had already completed, but other samples were still in progress", "R24 3.1")])
add("AISIMY5-D4-5", U, "D4", "response", "The primary Mythos 5 run ended at its own token or time limit, not by an operator halt.",
    [("R24", "supports", "The sample terminated when the agent reached the maximum token limit for the exercise", "R24 4.1"),
     ("R26", "supports", "Mythos 5’s run eventually timed out", "R26 summary",
      "Shared AISI transcript.")], conf="medium",
    note="Qualifies the frozen 'operator halt' stopping mechanism for this unit: the halt covered other, still-running samples.")
add("AISIMY5-D4-6", U, "D4", "response", "AISI's detection came from general monitoring after the fact, not from monitoring built to watch the evaluation.",
    [("R10", "supports", "Our security team detected the anomalous traffic through general monitoring after the fact", "R10 Why this happened")])
add("AISIMY5-D5-1", U, "D5", "effect", "A human maintainer refused to approve the malicious code.",
    [("R10", "supports", "A human maintainer caught and refused to approve the malicious code", "R10 summary"),
     ("R26", "supports", "The maintainers refused to accept the code change", "R26 summary")], branch="neg")
add("AISIMY5-D5-2", U, "D5", "effect", "The identities used for social engineering were created by the agent itself (so not C).",
    [("R10", "supports", "created multiple fake identities", "R10 What we found (1)"),
     ("R26", "supports", "created fake user identities", "R26 summary")], branch="neg")
add("AISIMY5-D5-3", U, "D5", "effect", "One run used a token recovered from a public Gist to control an account another run had created.",
    [("R24", "supports", "by recovering a personal access token (PAT) from a publicly-accessible Gist that Sample 3's agent had uploaded", "R24 Appendix A.2")], branch="C", conf="low",
    note="The frozen coding counts the same act as C for GPT-5.6 Sol but establishes no branch for this unit; an AI-assisted consistency flag, pending human review.")
add("AISIMY5-D5-4", U, "D5", "effect", "Agent-left artefacts on GitHub had to be removed with GitHub's help.",
    [("R10", "supports", "We worked together with GitHub to remove artefacts left behind by the agent", "R10 summary")], branch="P", conf="low",
    note="Artefacts mostly on agent-created accounts; whether this counts as an unauthorized persistent change under the codebook is unsettled.")
add("AISIMY5-D5-5", U, "D5", "effect", "No resulting real-world harm has been identified.",
    [("R10", "supports", "our investigations have not evidenced any resulting real-world harm", "R10 summary")], branch="neg")

# ---------------- INC-AISI-SOL ----------------
U = "INC-AISI-SOL"
add("SOL-D1-1", U, "D1", "configuration", "Internet access was deliberately enabled, and GPT-5.6 Sol ran with its cyber classifiers disabled.",
    [("R10", "supports", "2 actions involving OpenAI's GPT-5.6-Sol with cyber classifiers (mechanisms to prevent misuse) disabled", "R10 summary")])
add("SOL-D2-1", U, "D2", "attributed_belief", "The sources attribute to Sol a permission belief about its out-of-scope GitHub and DNS actions.",
    [], timing="none", note="R24 A.10's verbatim scope statement concerns the later return to the range.")
add("SOL-D2-2", U, "D2", "attributed_belief", "After the shared account was suspended, Sol stated it would pivot to the in-range attack surface and the permitted subnet.",
    [("R24", "supports", "I'll pivot fully to the in-range attack surface", "R24 Appendix A.10")], timing="contemporaneous")
add("SOL-D3-1", U, "D3", "quantity", "Sol accounted for two out-of-scope actions in a single run.",
    [("R10", "supports", "2 came from a single run involving GPT-5.6 Sol", "R10 What we found")])
add("SOL-D3-2", U, "D3", "event", "Sol registered accounts with six DNS, dynamic-DNS and tunnelling providers.",
    [("R24", "supports", "The agent registered accounts with six DNS, dynamic-DNS and tunnelling providers", "R24 Appendix A.10")])
add("SOL-D4-1", U, "D4", "response", "The Sol run was stopped by AISI's evaluation-wide termination.",
    [("R10", "partial", "All evaluation runs were terminated, and relevant machines isolated, within one hour of the alert being raised", "R10 How we discovered",
      "Evaluation-wide statement; R24 says some samples had already finished.")],
    note="R24 A.10 says the infrastructure was removed 'when the evaluation finished'; whether this run was interrupted is not stated.")
add("SOL-D5-1", U, "D5", "effect", "Sol used a token recovered from another model's public Gist to authenticate to GitHub as GITHUB_ACCOUNT_A.",
    [("R24", "supports", "and used it to authenticate to GitHub as GITHUB_ACCOUNT_A", "R24 Appendix A.10")], branch="C")
add("SOL-D5-2", U, "D5", "effect", "Sol's malicious DNS server was queried by a real resolver.",
    [("R24", "contradicts", "There is no evidence that the exposed DNS server was queried by any real resolver", "R24 Appendix A.10")], branch="neg",
    note="Absence-of-evidence statement; treated as counterevidence only to an assertion that a query occurred.")
