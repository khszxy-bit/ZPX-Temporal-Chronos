# [Fully Open Integrated Technical Whitepaper v9.0] ZPX Chronos-Shield

## Exact Integer-Vector and Riemann-Sphere Reconstruction of Whole-Server Information Spaces, Time-Indexed Integrity Defense, and an Open-Publication Declaration Preserving Legitimate Rights

**Publication date:** November 17, 2026  
**Original research concept and independent project lead:** Space Analysis (우주분석)  
**AI research assistance:** Google Gemini AI and OpenAI GPT  
**Project status:** Open defensive research architecture, mathematical proofs, synthetic simulations, and a reproducible Python proof of concept (PoC)—**not** a certified, operational antivirus, firewall, or intrusion-prevention product.  
**Reproducible code:** ZPX_Chronos_Shield_Public_MIT_v8_2026-11-17.zip (Python 3.10+ and 12 unit tests).  
**Publication and licensing proposal:** For new protectable expression in this v9 whitepaper, **Creative Commons Attribution 4.0 International (CC BY 4.0)** is proposed. The previously distributed v8 code and accompanying materials continue under their included **MIT License**. Copyright, patent, trademark, and third-party rights are distinct. No one may license rights they do not own; the final publisher should confirm ownership, licensing, and filing plans before external release.

> **Declaration of open research and retained rights.** This project began as a fundamental design proposed by an independent researcher who is not a professional security software vendor. Gemini and GPT were used as research tools to develop, challenge, and test the design. Anyone should be able to examine the publicly licensed materials, improve them, build subsequent products, and earn money from permitted commercial use. **Making research freely available does not itself waive legally existing copyright, legitimate inventor status, trademark rights, or the historical record of research contributions.** Equally, permissions already granted under an open license must be respected. The purpose is to help reduce the harm caused by intrusions, ransomware, and information theft.

---

## Executive Summary: Six Conclusions

1. **A server can be modeled as one time-dependent information space.** A trusted installation baseline can be committed, and file additions, deletions, movements, and modifications can be tracked over time, with separate ingress and egress policies.
2. **Finite binary cells can be mapped to exact integer vectors and rational coordinates on a Riemann sphere and reconstructed without loss.** All 131,072 possible 17-bit inputs were tested. Each of 2,000 isolated one-bit flips was distinguished in the tested 2,000-bit input. No differential or integral calculus is required for these proofs.
3. **Geometric reversibility is not malware classification.** Both benign and malicious data can satisfy the same geometric identities. Security decisions require a trusted previous state, content/path integrity, authenticated authorization, a protected event history, and actual operating-system enforcement.
4. **Gemini's time-indexed whole-server space model and GPT's exact reconstruction and adversarial counterexample testing are complementary.** Lossy phase coordinates must not be used as the sole authorization criterion; SHA-256 Merkle commitments and HMAC-authenticated histories were incorporated in the PoC.
5. **A research project can be made freely available without abandoning legitimate rights.** MIT and CC BY grant specified permissions while preserving relevant attribution and copyright notices. Their generous commercial permissions generally do **not** create an obligation to pay royalties.
6. **A detailed, dated public disclosure can become prior art against later patent claims covering the same disclosed subject matter.** This defensive-publication effect depends on what was disclosed, when, and under which laws. It neither blocks genuinely new improvements nor automatically preserves the discloser's own patent prospects.

---

# Part I. An Accessible Explanation: The Whole-Server Space Concept

## 1. Model the entire server as one changing space—not merely a collection of files

At installation, define the entire monitored server state, **S₀**, as an approved information space. It comprises the observable parts of file contents, normalized paths, sizes, configurations, and executable objects. The architecture uses several levels of exact integer-vector and sphere-coordinate representation: local 17-bit regions, intermediate 289-bit groups, and higher-level file and whole-server states.

For example, a server may contain 1,000 files in the morning and acquire another log file in the afternoon. That can be normal. But an executable may also have one unauthorized bit changed without changing its length. Consequently, **a total byte-volume number alone is insufficient**: actual content, location, time, and authorization must be recorded.

A “server inside a large Riemann sphere” means a **logical geometric representation and reversible atlas**, not a claim that physical hardware turns into a sphere. The operational logic is:

**Detect a change in the whole approved state → narrow the changed region → reconstruct its original cell and file location.**

~~~mermaid
flowchart TD
    A["Installation: trusted whole-server state S0"] --> B["Commit content, paths, and coordinate atlas"]
    B --> C["Record authorized changes over time"]
    C --> D{"Does current state match approved history?"}
    D -- "Yes" --> E["Record normal transition"]
    D -- "No" --> F["Trace 289-bit → 17-bit → original location"]
    F --> G["Alert; connect to actual OS enforcement"]
    E --> C
~~~

## 2. Where do the 90-degree condition and Archimedean one-third relationship belong?

The originating design prioritizes a defined **information space and volumetric structure** before inspecting individual bits. Two chosen vectors can generate an exactly orthogonal third axis. The classical relation that a pyramid or cone occupies one-third of the volume of the corresponding prism or cylinder **with the same base and height** can also be used as an exact geometric comparison for a specified construction.

However, benign and malicious data can both satisfy these identities. Therefore, neither **“90° means safe”** nor **“one-third means harmless”** follows from the geometry. The security-relevant question is whether the current coordinates and contents are consistent with an **authenticated, previously approved** state and its authorized changes.

## 3. What developers receive

- An architecture for tracing entire-server states through a **time-indexed history**.
- An **exact 17-bit/289-bit reconstruction mechanism** for the monitored binary cells.
- Cryptographic integrity checks sensitive to file relocation and same-length replacement.
- A prototype **authorization model** distinguishing expected updates from unauthorized changes.
- A distinction between **ingress** (writing, deployment, execution) and **egress** (reading, copying, transmission).

Independent developers, academic researchers, and commercial vendors can build higher-performance storage, operating-system integrations, administrative interfaces, and professionally tested defenses around this research skeleton.

---

# Part II. Mathematical Definitions and Exact Proofs

## 4. Formal definition of a server state

Let the finite set of server files explicitly selected for monitoring be

\[
S_t=\{(p_i,b_i(t))\}_{i=1}^{n_t},
\qquad b_i(t)\in\{0,1\}^{8m_i(t)}.
\]

Here **pᵢ** is a canonical path identifier, **bᵢ(t)** is the content bitstring, and **mᵢ(t)** is its length in bytes. The total observed information volume is

\[
V_{\mathrm{byte}}(S_t)=\sum_i m_i(t).
\]

This is **not** the same metric as the geometric volume derived from a vector cross product. Without distinguishing these two meanings of “volume,” an unchanged total size could conceal a content modification.

## 5. Reversible encoding of 17-bit integer cells

For a bit cell **b = (b₀, …, bₙ₋₁)** of length **1 ≤ n ≤ 17**, split the bitstring into two sections. The first has length **h = ⌈n/2⌉**. Encode the two sections as finite-width signed integers **(x, y)** using a fixed bit order and a specified reversible representation.

**The lengths and ordering of both sections must be preserved.** With those conventions, the mapping between the original cell and **(x, y)** is one-to-one.

For a larger file, process successive 17-bit cells and group them into 289-bit intermediate units (**17 × 17**). The atlas preserves data exactly only when the required cell coordinates and metadata are retained. **An arbitrarily large server cannot generally be compressed without loss into a single fixed-size 3D coordinate.**

## 6. An exact third orthogonal axis from two vectors

Define

\[
A=(1,x,0),\qquad B=(0,1,y),
\]

and calculate

\[
\boxed{C=A\times B=(xy,-y,1)}.
\]

Their dot products are

\[
A\cdot C=xy-xy=0,
\qquad
B\cdot C=-y+y=0.
\]

Thus **C** is exactly orthogonal to both **A** and **B**, with no numerical approximation from calculus. The associated parallelepiped volume indicator is

\[
\boxed{D=\det[A,B,C]=\lVert C\rVert^2=x^2y^2+y^2+1>0}.
\]

For a corresponding pyramid constructed with the same base and height, the volume is **D/3**. This is a mathematically exact relationship **for the specified geometric construction**—not a universal claim that all server data or all conceivable spaces are forced into a fixed 1:2:3 ratio, nor a malware classifier.

## 7. Exact Riemann-sphere projection and inverse

Choose a fixed positive integer scale **s = 5** and define

\[
P(x,y)=(X,Y,Z)
=\left(
\frac{2sx}{s^2+x^2+y^2},
\frac{2sy}{s^2+x^2+y^2},
\frac{x^2+y^2-s^2}{s^2+x^2+y^2}
\right).
\]

### Theorem A — Exact membership of the sphere

For all integer **x, y**, the point satisfies

\[
X^2+Y^2+Z^2=1.
\]

**Proof.** Expanding the numerator gives

\[
4s^2x^2+4s^2y^2+(x^2+y^2-s^2)^2
=(s^2+x^2+y^2)^2.
\]

This is exactly the square of the denominator. Therefore the quotient is exactly one. ∎

### Theorem B — Exact reversibility

For finite **x, y**, we have **1 − Z > 0**, and

\[
\boxed{x=\frac{sX}{1-Z},\qquad y=\frac{sY}{1-Z}}.
\]

**Proof.** Substitution yields **1−Z=2s²/(s²+x²+y²)>0**, and the inverse formulas recover the original **x, y**. The fixed cell lengths and bit ordering then reconstruct the original bitstring. Exact rational arithmetic may be used to avoid floating-point rounding. ∎

### Theorem C — Distinguishing a one-bit change

For cells of the same fixed length and position, two different bitstrings have different integer-coordinate pairs **(x, y)**. By Theorem B, they therefore have different sphere coordinates **P(x, y)**. A changed monitored bit cell can thus be distinguished by its **exact reversible representation**. ∎

**Scope of the proof:** This establishes *representation and distinguishability*. It does **not** prove that a production agent observes every operating-system write, knows malicious intent, or blocks encryption before harm occurs.

## 8. A 17-fold phase summary and an exact reversible atlas serve different purposes

Gemini's original 17-symmetric phase-based summaries can be considered for pattern exploration and visualization. But a compact summary of a longer arbitrary bitstring must be checked for collisions before it is treated as an authentication value.

The independently reproduced **v6** compressed coordinates had no more than

\[
1021\times509=519{,}689
\]

possible **(x, y)** values, whereas a 16-byte input permits **2¹²⁸** possible bitstrings. By the pigeonhole principle, an injective mapping is impossible.

In the existing synthetic test with random seed **1706**, a coordinate collision was observed at sample **442**, producing the same compressed coordinate **(-50, -105)** for different inputs.

This does **not** invalidate Gemini's broader idea of monitoring a whole-server space through time. It does show that **these compressed coordinates alone must not authenticate or authorize a change**. They may be used for inspection and display while actual authorization relies on trusted integrity evidence.

---

# Part III. Security Architecture and Implementation Boundaries

## 9. Bind whole-server paths and contents to a cryptographic commitment

For every monitored file, use a length-delimited, canonical encoding of its path **p**, size **m**, and full contents **b**. Define a leaf value of the form

\[
L(p,b)=H(\mathrm{tag}\Vert|p|\Vert p\Vert|b|\Vert H(b)).
\]

Combine sorted leaves in a Merkle tree to obtain

\[
R_t=\operatorname{MerkleRoot}(S_t).
\]

A standardized cryptographic hash such as SHA-256 is used. **Unlike the exact sphere atlas, the hash is not reversible.** Collision resistance is a computational security property, not a proof that no collision can ever exist.

A same-size file replacement can change the leaf, as can a path rename. A real file-system specification must additionally define what to do about ownership, permissions, links, special files, containers, live databases, and concurrent writes.

## 10. Authenticate the temporal event ledger

Each event **Eₜ** binds a sequence number, trusted time, action type, previous and current roots, approved identity, and previous authentication value. Compute

\[
M_t=\operatorname{HMAC}_K\!\left(\operatorname{Canonical}(E_t)\right).
\]

**HMAC is a message authentication code**, not encryption and not the same as a public/private-key digital signature. If the baseline and HMAC key remain under the same permissions as a compromised host administrator, the attacker may modify both. A production design therefore needs separate key custody, protected approval procedures, and independently stored or externally forwarded audit records.

## 11. Treat ingress and egress as distinct security boundaries

- **Ingress:** Who may install, alter, or execute which objects? This requires authenticated identity, approved changes, and code-execution controls.
- **Egress:** Who may read, copy, or transmit which contents to which destination? **Read-only theft** can occur without changing a file and will not be detected by file-integrity checking alone.
- **Prototype tokens:** A synthetic token binds a path, destination, nonce, current approved root, and content digest. Replays are rejected, but the v8 implementation does not force every real network transmission through this check.

## 12. Reference algorithm for a defensive implementation

~~~text
INSTALL(trusted_server_state):
    scope := explicit_allowlist_of_monitored_objects
    S0 := collect_consistent_path_and_content_snapshot(scope)
    R0 := authenticated_merkle_root(S0)
    store_R0_and_approval_keys_off_host()
    build_exact_sphere_atlas_on_selected_segments(S0)

ON_CHANGE(event, new_state):
    if not authenticated_identity_or_not_authorized_transition(event):
        alert_and_request_OS_enforcement()  # not implemented in v8
        return
    if not validate_event_chain(event):
        alert(); return
    Rnew := merkle_root(new_state)
    append_authenticated_event(event, Rold, Rnew)
    display_time_indexed_spatial_delta()

VERIFY():
    current := collect_consistent_scope_snapshot()
    if merkle_root(current) != last_approved_root:
        changed_objects := compare_manifest_by_path_and_content()
        for object in changed_objects:
            exact_reverse_map_289_to_17_bit_cells(object)
        alert_without_claiming_certain_malware_identity()

EGRESS(request):
    require_authenticated_identity_and_nonreusable_token()
    require_real_gateway_to_enforce_all_relevant_paths()
~~~

## 13. What remains to be engineered before production deployment?

| Component | Current public v8 status | Additional production work |
|---|---|---|
| Exact integer-vector and Riemann-sphere atlas | Implemented and mathematically tested | Optimize targeted recomputation and visualization |
| Content/path Merkle root | Implemented | Incremental updates and consistent large-scale snapshots |
| Time-indexed HMAC ledger | Simulated | External logging, protected keys, trusted time, recovery |
| Directory change checking | Read-only command-line prototype | Missed-event handling, race conditions, symlink policies |
| Ingress/egress authorization | Simulated policies | Real kernel/gateway enforcement and authenticated identities |
| Antivirus/EDR behavior monitoring | Not implemented | Process/memory/behavior monitoring and incident response |
| Empirical attack-blocking rates | Not measured | Independent attack tests, false positives, performance benchmarks |

An achievable development route is integration with established Linux **fs-verity**, **IPE/IMA**, and Windows **App Control** or comparable execution controls. This is an effort to complement existing security layers, not an experimentally justified reason to discard EDR, firewalls, privileged-access management, or immutable backups.

---

# Part IV. Reproducible Mathematical and Technical Simulations

## 14. Test results—and exactly what they establish

| Test | Observed outcome | Valid conclusion |
|---|---:|---|
| Exhaustive 17-bit domain | **131,072/131,072** round trips | Accurate reconstruction of fixed-width cells |
| 250-byte / 2,000-bit input | **118 / 7 / 1** cells | Correct 17/289/2,000-bit hierarchy counts |
| Flip each of 2,000 bit positions | **2,000/2,000** distinguished | Local sphere coordinates change for tested monitored flips |
| Two vectors and cross product | **Exact orthogonality** | A·C=B·C=0 and specified integer-volume identity |
| Gemini v6 compressed representation | Collision at sample **442** | Concrete counterexample to coordinate-only authentication |
| Software unit tests | **12 passed** | Synthetic implementation satisfies its defined test suite |
| Prevention rate against real ransomware | **No evidence reported** | Not verified |
| Speed or false-positive superiority over EDR | **No evidence reported** | Not verified |

These findings were verified in the existing public Python v8 package; the 12 unit tests were run again when preparing the Korean v9 whitepaper and passed.

Unpack the source archive, then run the following with **Python 3.10 or later**:

~~~bash
python zpx_open_core.py
python compare_gemini_v6_coordinates.py
python -m unittest -v test_zpx_open_v8.py
python benchmark_v8.py
~~~

The optional read-only directory example uses a disposable sample directory. The **init** command creates new baseline and key files and must not be run casually on production infrastructure:

~~~bash
python zpx_snapshot_cli.py init --directory sample_directory --manifest baseline.json --keyfile baseline.key
python zpx_snapshot_cli.py check --directory sample_directory --manifest baseline.json --keyfile baseline.key
~~~

**Do not advertise “100% hacker prevention,” “zero false positives,” or “guaranteed zero-day blocking” based on these tests.** The verified properties are exact coordinate recovery and defined synthetic integrity checks. They are useful, bounded results—not proof of deployment-grade prevention.

## 15. Strengths, limitations, and comparison with existing security technology

| Comparison | Potential ZPX research benefit | Current limitation |
|---|---|---|
| File Integrity Monitoring (FIM) | A joint view of spatial structure, state changes, and history | Existing FIM already detects hash/path changes; superiority is unproven |
| Hashes and Merkle trees | Reversible coordinates can locate original changed **bits** | Original data must be retained; sphere calculation adds overhead |
| EDR/XDR | A structured audit layer for approved file/configuration changes | Fileless activity, stolen identities, and legitimate-tool abuse require other defenses |
| Firewalls and DLP | Potential linkage of whole-state history to egress policy | Copying or exfiltration remains possible unless all relevant channels are enforced |
| Large servers | Incremental Merkle updates and selective local reconstruction may scale | No production benchmarks for millions of files, live databases, or high availability |

The critical **ablation experiment** must compare **(A) cryptographic hashes plus existing policy** with **(B) those mechanisms plus the reversible sphere atlas**, using the same workloads, devices, threat model, and cost metrics. Measure performance, false positives, troubleshooting time, and actual security benefit. If the sphere layer adds no practical value for a specific workload, simplifying that part is an acceptable engineering result.

---

# Part V. Open Publication Without Waiving Legitimate Intellectual Property Rights

## 16. Publication is not the same as abandonment of rights

The legal ownership of a copyright and the permission granted to the public are separate matters. Publishing a whitepaper for free does not, by itself, abandon copyright in protectable human-authored expression. **MIT** allows copying, modification, redistribution, and selling subject to preservation of its notices. **CC BY 4.0** allows sharing, adaptation, and commercial reuse with attribution.

Four categories must be kept distinct:

1. **Copyright in expression:** Protectable original human-authored prose, diagrams, and source-code expression—not the underlying abstract mathematical ideas as such.
2. **Patent rights:** Potentially protect concrete technical inventions under applicable filing, examination, inventorship, novelty, and inventive-step rules. A whitepaper copyright notice does not automatically create a patent.
3. **Trademarks:** Names and official branding, such as **ZPX** and **ZPX Chronos-Shield**, may need separate clearance and registration/usage analysis.
4. **Confidential information:** Once full technical details are genuinely made public, they generally cannot remain confidential trade secrets at the same time.

Because Gemini and GPT generated portions of the draft and code, ownership and statutory copyright eligibility are **not guaranteed for every AI-produced element**. Human creative selection, editing, design decisions, and actual individual contributions matter. Preserve dated versions of the original concept, architectural decisions, prompts, mathematical corrections, code revisions, and tests.

## 17. Can a large company take the disclosure and patent it so others cannot use it?

### 17.1 A sufficiently detailed early publication may become prior art

When an accessible whitepaper, source repository, drawing, and reproducible experiment disclose a concrete technical method with a verifiable date, their contents may qualify as **prior art** against later patent applications claiming the same disclosed method.

This is known as **defensive publication**. The World Intellectual Property Organization (WIPO) discusses it as a strategy for preventing later exclusive patent claims over already disclosed inventions.

Nevertheless:

- It cannot physically prevent a company from **filing** an application.
- A patent office may not automatically discover the publication; evidence of the publication's content and date is crucial.
- A title, slogan, or vague claim may provide less protection than an enabling technical description with equations, architecture, and reproducible code.
- A company may still develop and possibly patent **genuinely novel improvements not disclosed earlier**.
- Your later publication does not automatically invalidate **older patents held by third parties**.

**Correct conclusion:** A complete, dated disclosure can help resist monopoly claims over what it actually teaches; it cannot guarantee universal freedom from all patents.

### 17.2 Public disclosure can also limit the original researcher's future patents

South Korea recognizes a **12-month novelty grace-period exception** for certain qualifying disclosures, subject to filing and evidence requirements. Other jurisdictions may differ considerably, and several overseas routes may be less forgiving. If exclusive patents are a serious possibility, **review filing before additional full public disclosure**. For previously published ZPX articles, identify the actual first disclosure date.

### 17.3 If the goal is unrestricted worldwide development

Detailed defensive publication and properly drafted open-source licensing support widespread adoption. However, a **copyright license and a patent license are not the same**.

For future versions and contributor policies, **Apache License 2.0** is an option to evaluate because it contains an **express, limited patent grant** and a patent-litigation termination provision. This does not solve every third-party patent issue. The existing v8 package remains under the MIT terms with which it was distributed; valid permissions already granted should not be presumed revocable unilaterally.

## 18. Recommended publishing and licensing structure

| Material | Recommended approach | What developers may do | What remains with the originator |
|---|---|---|---|
| New protectable v9 whitepaper text/diagrams | **Propose CC BY 4.0** | Share, translate, adapt, and commercially use with attribution | Retained authorship/attribution interests where recognized; no default royalty |
| Existing v8 Python code and accompanying materials | **Keep their MIT License** | Copy, improve, sell, and redistribute with required notices | Protectable copyright and credit; no compulsory royalty |
| Abstract mathematical principles | Cannot be monopolized merely by attaching a copyright license | Independently implement subject to relevant laws | Concrete patent claims, if any, require separate legal analysis |
| ZPX names and official logos | Evaluate a separate trademark and brand policy | Truthfully describe research provenance | Potential protection against misleading claims of official affiliation |
| Unreleased Gemini conversations or third-party code | Outside this document's blanket permission | Follow original rights-holder permissions and service terms | No license to content the publisher does not own |

**The goal is not a CC0-style waiver or public-domain dedication.** Equally, one should not attach “all commercial use prohibited” language to code already offered under a permissive MIT license; that would contradict the stated terms.

### Suggested publication notice

> **© 2026 Space Analysis (우주분석).** Legitimate rights in human research/design contributions and protectable expression are retained. This whitepaper is offered for public study and reuse under **CC BY 4.0**, **only to the extent that its publisher has rights to license its contents**. The separate **ZPX Chronos-Shield v8** software package remains under its included **MIT License**. Neither public disclosure nor this notice itself waives existing patent, trademark, or other legal rights. No exclusive copyright is asserted over abstract mathematics, generic ideas, or third-party material. Gemini and GPT served as AI research tools, not independent legal co-authors.

This notice **does not create a patent monopoly**. Applicable rights depend on the actual creative contribution, inventive work, authorship, registrations, prior art, and national laws. This whitepaper offers general publication-strategy analysis rather than individualized legal advice.

## 19. If a company makes a fortune using the project, must it pay the original researcher?

**Generally no**, if the company uses only material validly licensed under the MIT and CC BY permissions and complies with their conditions. These licenses typically do not require royalties or a share of sales.

That is consistent with the original researcher's expressed wish: **“Take the research skeleton, build something useful, and make money if you can.”**

However, freedom from mandatory royalties does **not** exclude:

- Voluntary financial support or research sponsorship.
- A separate paid consulting engagement.
- Joint research and development agreements.
- Voluntary credit, in-kind assistance, or engineering contributions.
- Negotiated agreements involving separate, independently developed technology.

None of these payments is guaranteed, and no responsible projection can promise they will occur.

### Optional, non-binding sponsorship statement

> **Voluntary Research Support.** Use and commercial development of the public code do not require a donation or revenue sharing. Individuals and companies who find this work useful and wish to support further independent research, technical validation, or collaboration are welcome to do so voluntarily. The permissions granted by the open licenses are the same whether or not anyone contributes. Independent research also takes time, computing resources, and—as the originator likes to joke—coffee money. 🙂

Add a payment channel or contact address only if the original researcher chooses to publish one. Local tax and business obligations should be checked if financial support is actually received.

## 20. Practical measures to preserve evidence of contribution and publication

1. **Identify the project lead:** Use **Space Analysis (우주분석)** consistently, while acknowledging Gemini and GPT as AI tools rather than asserting unsupported legal co-authorship.
2. **Keep source evidence:** Archive original design statements, AI conversations and corrections, intermediate calculations, versions, code, and test records.
3. **Establish dates:** Preserve version identifiers, hashes of released archives, public URLs, and timestamps. Publish later corrections as identifiable new versions.
4. **Make the technical disclosure searchable:** Include reproducible algorithms, data structures, formulas, relevant assumptions, and negative results—not just slogans.
5. **Attach actual standard licenses:** Preserve the v8 **LICENSE** and **NOTICE.md**. Identify the proposed CC BY terms for new v9 whitepaper expression without contradicting earlier MIT permissions.
6. **Do not disclose operational secrets:** Exclude real private keys, internal hostnames, production baselines, credentials, network diagrams, and personal data.
7. **Review patent strategy before further details are published:** Especially when foreign protection is contemplated. For material already public, reconstruct the original disclosure timeline.

---

# Part VI. An Open Invitation to Developers

## 21. Verify, improve, and commercialize—but follow rigorous engineering practice

To independent researchers, universities, security engineers, and companies around the world:

- When discovering an error, publish the **minimal reproducible counterexample and a proposed correction**.
- Do not confuse **mathematically exact coordinates** with **demonstrated real-world intrusion prevention**.
- Measure the limitations involving fileless attacks, stolen administrator accounts, legitimate-tool abuse, read-only theft, brief modifications restored between checks, and denial-of-service.
- Connect the prototype to existing Linux or Windows protection mechanisms before considering enforcement, and **test blocking only in controlled non-production environments** until independently validated.
- You may develop commercial implementations and sell permitted derivatives. Please comply with the applicable licenses and preserve the required notices.
- If possible, help the original independent researcher continue verification. Open research has real costs even when the source is free.

## 22. Proposed research tasks for independent teams

1. Compare the cost and benefit of selectively computing reversible 17/289-bit atlases against **Merkle-only** baselines.
2. Test compromised baseline-updating authority, stolen keys, and malicious administrator activity under separated trust roots.
3. Measure **false positives and resource usage** under legitimate software updates, rapid log growth, and database workloads.
4. Test reboot, rollback, snapshot restoration, and cluster migration while preserving an auditable event history.
5. Quantify blind spots for attacks that do not modify persistent files or that misuse authorized tools.
6. Publish throughput, CPU, memory, latency, and operational-cost measurements at realistic server sizes.
7. Test whether spatial-change visualization actually reduces a security analyst's **time to identify root cause**.
8. Define a contributor policy covering licensing, express patent grants, brand usage, and accurate attribution.

---

# Part VII. Final Validation and Public Research Declaration

## 23. Which claims can currently be supported?

| Claim | Current assessment | Scope |
|---|---|---|
| Whole-server state as a time-indexed information space | **Feasible** | A finite monitored state and transitions can be defined |
| Exact reconstruction: bits → integers → sphere → bits | **Mathematically proven under conditions** | Fixed lengths/order and exact rational coordinates |
| Exact 90° orthogonality of the constructed cross product | **Proven** | The relevant dot products equal zero |
| Specified pyramid volume is one-third of corresponding prism | **True for the stated geometry** | Not a universal malware indicator |
| Lossless encoding of an arbitrary server in one finite sphere point | **Not established; generally impossible** | Finite-summary information limit |
| Detecting persistent unauthorized file changes | **Feasible in the model** | Trusted baseline, complete observation, checking time, cryptographic assumptions |
| Preventing all malware, insider threats, and zero-days | **Not demonstrated** | No production OS enforcement or representative attack trial |
| Open availability while retaining legitimate rights | **Possible** | Distinguish ownership from permissions granted |
| Prior public disclosure helping resist identical later patents | **Possible, conditional** | Publication specificity, date, patent examination, local law |
| Mandatory payment by commercial adopters | **No, not under the proposed permissive licenses** | Voluntary sponsorship remains possible |

## 24. Public declaration—ready for quotation

> I am **Space Analysis**, an independent researcher who has proposed treating a server's entire information state as a space that can be modeled and reconstructed through integers, vectors, and Riemann-sphere coordinates. I am not publishing a certified, unbreakable security product. With the assistance of the Gemini and GPT AI research tools, I have developed and examined a **basic research architecture**, its mathematics, reproducible tests, and counterexamples.
>
> I am sharing this work because I want researchers, universities, independent developers, and companies everywhere to build better defenses against hacking, ransomware, and data theft. Subject to the specified open licenses, anyone may study the public materials, improve the code, create subsequent products, and earn money through permitted commercial work.
>
> **This public release does not mean that the original researcher and other contributors abandon any legally recognized rights in their human creative or inventive contributions.** At the same time, no claim of exclusive ownership is made over abstract mathematics, generic technical ideas, or material owned by third parties.
>
> This whitepaper discloses what has been mathematically established, what the synthetic software tests reproduced, and what remains unproven. Everyone is invited to challenge the design with independently reproducible results. No unverified protection rate is presented as a demonstrated fact.
>
> There is no mandatory revenue-sharing obligation attached to the permissively licensed public work. Nevertheless, voluntary sponsorship, collaboration, and recognition of the project's original research contributions would be sincerely welcome.
>
> **Let the technology be available, let credit remain accurate, and let the results benefit society.**

---

## Appendix A. Short English Rights Statement

**English:** This whitepaper and its associated research code are made available to facilitate independent analysis, improvement, and permitted commercial development. Free disclosure is **not an automatic copyright waiver** and **not automatic creation of patent ownership**. The existing v8 code and accompanying documents retain their MIT terms. CC BY 4.0 is proposed for protectable new v9 whitepaper expression that the publisher has the authority to license. Patent filings should be considered before any additional disclosure where future exclusive rights are important. Voluntary support is welcome but not required.

## Appendix B. Reproducibility Package and Primary References

### Existing research and source code

- **WHITEPAPER_KR.md** — The original Korean v8 mathematical and security whitepaper.
- **zpx_open_core.py** — Exact 17/289-bit sphere atlas, content/path Merkle commitment, synthetic temporal ledger, and policy demonstration.
- **compare_gemini_v6_coordinates.py** — Independent reproduction of the compressed-coordinate collision.
- **zpx_snapshot_cli.py** — Read-only directory integrity check.
- **test_zpx_open_v8.py** — Twelve unit tests, including exhaustive 17-bit and 2,000-bit single-flip checks.
- **benchmark_v8.py**, **README.md**, **LICENSE**, **NOTICE.md** — Benchmark, usage, and licensing materials.

### Primary intellectual-property sources

1. WIPO, *Inventing the Future — Intellectual Property for Business*, defensive publication: <https://www.wipo.int/edocs/pubdocs/en/wipo_pub_917_1.pdf>.
2. WIPO, *Frequently Asked Questions: Patents*, prior art and grace periods: <https://www.wipo.int/en/web/patents/faq_patents>.
3. Korean Intellectual Property Office, *Grace Period for Public Disclosure (공지예외주장 제도)*: <https://www.kipo.go.kr/ko/kpoContentView.do?menuCd=SCD0200239>.
4. Korean Intellectual Property Office, warning regarding foreign patent filings after disclosure: <https://www.kipo.go.kr/ko/kpoBultnDetail.do?aprchId=BUT0000029&menuCd=SCD0200618&ntatcSeq=19514&sysCd=SCD02>.
5. Open Source Initiative, *MIT License*: <https://opensource.org/license/mit>.
6. Creative Commons, *Attribution 4.0 International*: <https://creativecommons.org/licenses/by/4.0/>.
7. Korea Copyright Commission, *Guide to Copyright Registration for Generative AI-Assisted Works*: <https://www.copyright.or.kr/eng/doc/etc_pdf/Guide_to_Copyright_Registration_for_Generative_AI-Assisted_Works.pdf>.
8. Apache Software Foundation, *Apache License, Version 2.0*: <https://www.apache.org/licenses/LICENSE-2.0>.

### Primary cybersecurity references

9. Linux kernel, *Integrity Policy Enforcement (IPE)*: <https://docs.kernel.org/admin-guide/LSM/ipe.html>.
10. Linux kernel, *fs-verity*: <https://docs.kernel.org/filesystems/fsverity.html>.
11. Microsoft, *App Control for Business*: <https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/appcontrol>.
12. NIST, *Zero Trust Architecture*, SP 800-207: <https://csrc.nist.gov/pubs/sp/800/207/final>.

---

## Final Statement

The originating architectural principle is preserved: **define the server's whole information space first, track its authorized evolution over time, and reconstruct changed regions down to exact original binary cells.** Gemini's whole-system temporal concept and GPT's reversible integer-sphere coordinates, collision counterexamples, and cryptographic integrity checks have been brought together in a reproducible research skeleton.

The public may develop and commercialize permitted implementations under the applicable licenses. **Making the research available does not require the originator to renounce legitimate rights or historical credit.** Equally important, the exact scope of the mathematics, incomplete enforcement mechanisms, patent-filing risks, and unverified real-world protection rates are disclosed transparently.
