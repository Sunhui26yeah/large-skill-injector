# Hosting Interns and Publishing as a Google SWE L4 (Core ML Frameworks & Compiler)

Planning note for Hui's Google start in **May 2027** as a PhD new-grad SWE at **L4** on Core ML
Frameworks & Compiler (XLA/JAX stack). Answers two coupled questions: *when can I co-host or host
an intern*, and *how do I keep publishing on a SWE ladder*. The two are coupled on purpose —
interns and student researchers are the main publication engine available to an infra SWE.

> **Confidence caveat.** Intern-host eligibility rules are org-level at Google and change over
> time; the specifics below are industry-common practice, not verified internal policy. Re-check
> against `go/intern-host`, `go/student-researcher` and the hiring manager before acting. Flagged
> items are collected under "Open questions" at the bottom.

## Eligibility, as generally practiced

- A **host** must be a full-time employee, typically **L4+**, and typically **~6 months tenured**
  by the time the internship starts.
- A **co-host** has a much lower bar — it mostly requires a willing experienced host to pair with.
- The binding constraint is not personal eligibility but **headcount, which is allocated at the
  team level roughly two quarters ahead** of the internship. Summer-intern host sign-up runs in
  roughly **Oct–Dec of the prior year**; matching and interviews run **Jan–Apr**.

## Timeline from a May 2027 start

| Cycle | Tenure at start | Feasible? |
|---|---|---|
| Summer 2027 interns (May–Aug 2027) | 0 months | **No** — matching closed in early 2027, before the start date |
| Student Researcher, Fall 2027 / Spring 2028 | 6–10 months | **Yes, earliest realistic** — co-host |
| Summer 2028 interns | 12 months | **Yes** — first natural cycle as primary host |
| Summer 2029 interns | 24 months | **Yes** — 2 interns plus a student researcher is sustainable |

**Student Researcher is the underrated shortcut.** It is rolling/quarterly rather than annual, can
be part-time, can run up to about a year, and is research- and publication-shaped by design — a
better fit for the publication goal than a summer internship, with lighter approval. Raising it in
fall 2027 puts the earliest co-hosting around **Nov 2027 – Jan 2028**.

### Action points, in order

1. **Jun 2027 (month 1)** — state the ambition explicitly in 1:1s: *I want to host interns and I
   want to publish*. This single sentence changes project allocation, and it has to land before
   the fall headcount planning, not after.
2. **~Jul 2027** — file the outside-collaboration / IP disclosure for any continuing NC State work
   with the PhD advisor, before a paper exists rather than after.
3. **Sep–Oct 2027** — the team plans 2028 intern headcount. Be part of that conversation.
4. **Oct–Dec 2027** — summer-2028 host sign-up window; register as co-host.
5. **Jan–Apr 2028** — write the intern project proposal. **This is the actual leverage point**: the
   proposal decides whether the internship yields a paper, not the intern's talent.
6. **May–Jun 2028** — first hosted summer intern.
7. **Aug–Sep 2028** — internship wrap → workshop paper; **Sep–Oct 2028** → full conference
   submission (start publication approval 4–6 weeks before the deadline).

## Publishing on the SWE ladder

The structural fact: this is the **SWE ladder, not Research Scientist**. Perf is judged on launches
and infra impact; papers do not count toward perf. Nobody blocks publishing, but nobody funds time
for it either. So papers have to be a **byproduct of roadmap work**, never a side project.

1. **Pick topics that sit on the XLA/JAX roadmap.** The PyTorch→XLA migration direction from the
   dissertation already qualifies and is natural MLSys / ASPLOS / CGO / PLDI material. A
   publication-motivated project that the team does not otherwise need will not survive two
   quarters on a SWE ladder.
2. **Push the paper-shaped work onto interns and student researchers.** One well-scoped intern ≈
   one paper is the standard productivity formula in Google infra orgs.
3. **Co-author with Google DeepMind / Google Research collaborators**, who carry publication
   expectations while an infra SWE carries the systems work and the data. Cross-org collaboration
   inside Google is far cheaper than external collaboration.
4. **Budget 2–6 weeks for internal publication approval** (legal + patent review). Work backward
   from ASPLOS/MLSys/NeurIPS deadlines accordingly.
5. **Pre-Google PhD work**: aim to submit the remaining NC State papers (the FSE 2027 / ICSE NIER
   candidates in `project-thesis-directions-2026`) **before the May 2027 start**, affiliated to NC
   State. Continuing the same line of work after joining makes IP ownership genuinely hard to
   explain. The ESEM 2026 camera-ready (Sep 2026) is already past and unaffected.

## The real driver: citations for an EB-1 green card

Publishing here is not an ambition item — it is immigration infrastructure. The stated plan is to
use **off-hours** for papers in order to accumulate citations for an EB-1 petition (see
`project-opt-h1b-timeline-2027`, which already records the preference for EB-1 over EB-2). That
reframes the whole strategy, and one part of it is actively risky.

> **Not legal advice.** Employment-IP and immigration specifics below need a real attorney and the
> internal policy pages; they are recorded here as the shape of the problem, not as answers.

### Off-hours does not mean off-Google, for *this* topic

California Labor Code **§2870** (Washington's RCW 49.44.140 is similar) limits how far an invention
assignment agreement can reach: it cannot claim work done **entirely on personal time, without
employer equipment or confidential information**, that *also* (a) does not relate to the employer's
business or actual/anticipated R&D, and (b) does not result from work performed for the employer.

ML compilers and PyTorch→XLA **fail both prongs at Google** — that is precisely the employer's
business and precisely the assigned work. So an off-hours paper in that area is still Google's
work product and still needs internal publication approval. Spending evenings on it changes *who
reviews it*, not *who owns it*.

Practical consequence: there is no "clean personal track" for in-area work. The two viable lanes are
(1) publish in-area **through** the official channel with Google affiliation, or (2) keep a
genuinely adjacent lane — the empirical/SE side of the dissertation (migration practices,
agentic-code studies, FSE/ICSE-shaped work) is far more defensible as outside Google's business
than XLA compiler internals. Lane 2 still gets disclosed under the outside-activity policy.

### Google affiliation does not weaken the petition

Nothing in EB-1A/EB-1B requires independent or non-employer research. Google-affiliated papers count
fully, and the affiliation measurably *raises* citation rates and invited-talk odds. The instinct to
protect a "personal" publication record is not worth the IP exposure it buys.

### Ranked by citations per hour spent

1. **Senior-author with the former advisor's current students.** They do the work, citations accrue
   to a shared record. Cheapest citation engine available; requires outside-collaboration approval.
2. **Papers attached to shipped XLA/JAX features.** People cite infrastructure they actually use —
   this has by far the highest citation ceiling, and it is also the roadmap work.
3. **Visibility work**: arXiv preprints early, open-source artifacts, talks. Citations follow
   reachability more than quality.
4. **Reviewing / program-committee service.** Does not generate citations, but satisfies the
   separate EB-1A "judging the work of others" criterion — start accumulating immediately, it is
   cheap and slow to build.
5. **Solo off-hours papers** — the worst return of the five, and the only one carrying IP risk.

### Timing

EB-1A is self-petitionable at any time and does not wait for an employer; EB-1B needs the employer
to file and roughly three years in the field (the PhD counts). Google's immigration team typically
engages around the 12-month mark, which lands in **mid-2028** — but if the beneficiary was born in
mainland China or India, EB-1 priority dates retrogress and the filing date matters far more than
the approval date, so the petition should be prepared in parallel rather than after. Confirm the
current visa-bulletin position with counsel; it moves.

## Relationship to the L4 → L5 promotion

Hosting interns is standard **leadership evidence** in an L4→L5 packet, but it is an additive
signal — technical impact remains the deciding one. Convenient timing: if the push for an L5
starting level does not succeed, the summer-2028 cycle (one intern with real output plus a paper)
lands inside the window of the first promotion packet.

## Open questions to verify after joining

- Exact level and tenure bar for host vs. co-host in this specific org (`go/intern-host`).
- Whether Student Researcher hosting has its own tenure requirement, and what the quarterly
  application/start cadence actually looks like.
- Whether work completed entirely before joining, under a university affiliation, still requires
  internal publication approval.
- The current process for declaring an ongoing academic collaboration with a former advisor, and
  how IP is apportioned for joint work.
- Conflict-of-interest/recusal rules if recruiting an intern or student researcher out of the
  former lab.
- The outside-activity / moonlighting policy: what off-hours academic publishing requires in the
  way of disclosure and approval, and where the line sits between "adjacent" and "in-area".
- Whether the internal publication-approval process treats an off-hours, university-affiliated
  paper differently from a Google-affiliated one.
- With counsel: EB-1A vs. EB-1B sequencing, and whether to self-petition ahead of Google's own
  green-card timeline given priority-date retrogression.

## Related

- [Alphabet / Google](../entities/Alphabet.md) — company page
- Claude auto-memory: `project-google-team-core-ml-compiler`, `project-thesis-directions-2026`,
  `project-opt-h1b-timeline-2027` (hosting eligibility is independent of the visa timeline, but the
  publication strategy is not — the EB-1 citation requirement is what makes publishing non-optional)
