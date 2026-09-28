Data Governor: a profile-driven system that understands files, proposes how they should be organised, and only changes the filesystem through a safe, auditable execution layer.
Phase 1 — Foundation / MVP
The first milestone should prove the complete workflow using Jellyfin media because identification is relatively straightforward.
NAS
 ↓
Scanner
 ↓
Asset Catalogue
 ↓
Media Identification
 ↓
Governance Profile
 ↓
Proposed Changes
 ↓
Review UI
 ↓
Safe Executor
 ↓
Audit / Undo

The MVP needs a lightweight web UI, FastAPI backend, SQLite database, filesystem scanner, configurable scan roots, Jellyfin naming profile, proposal engine, accept/reject/edit workflow, safe move/rename executor, collision/path validation, and complete operation history with undo.
A key architectural rule should be established immediately: AI never directly modifies files. It produces structured metadata; deterministic code converts metadata + profile rules into filesystem operations.
Phase 2 — Document Governance
Once the framework works, introduce scanned documents as the second profile. This validates that profiles can use completely different methods of understanding content while sharing the same governance engine.
PDF
 ↓
Text present? ── Yes ──→ Extract
 ↓ No
OCR
 ↓
Extracted content
 ↓
Document classifier
 ↓
Structured metadata
 ↓
Namespace taxonomy
 ↓
Naming + folder rules

For example:
2022-04-17.pdf

→

Household/
  Council Tax/
    2022/
      2022-04-17 - Milton Keynes Council - Council Tax Bill.pdf

This phase introduces OCR, document classification, entity extraction, confidence scores, classification evidence, namespace taxonomies and an Unclassified workflow.
Phase 3 — Profiles as a First-Class Concept
Rather than hard-coding media and documents, define a common profile system.
Conceptually:
profile:
  name: Personal Documents
  asset_types:
    - application/pdf

understanding:
  strategy: document

classification:
  taxonomy: personal_documents

organisation:
  path: "{namespace}/{organisation}/{year}"
  filename: "{date} - {organisation} - {subject}"

safety:
  allow_rename: true
  allow_move: true
  allow_delete: false

ai:
  mode: local_only

Different profiles can then plug different understanding strategies into the same engine:
Media      → filename + metadata + TMDB
Documents  → text + OCR + LLM
Photos     → EXIF + image understanding
Music      → tags + MusicBrainz
Backups    → filename/path rules
Other      → generic LLM classification

Phase 4 — Intelligence Layer
I'd deliberately make this hybrid rather than "LLM everything."
               Asset
                 ↓
        Deterministic extraction
                 ↓
           Rules/parser
                 ↓
         External metadata
                 ↓
          Enough certainty?
           ↙           ↘
         YES            NO
          ↓              ↓
      classify          LLM
           ↘           ↙
        Structured Metadata

Every result should have structured fields, confidence, evidence/source and warnings. The governance engine consumes that output rather than arbitrary LLM-generated paths.
Phase 5 — Catalogue
Every scanned asset gets an identity independent of its filename.
Something roughly like:
Asset
 ├── ID
 ├── hash
 ├── original path
 ├── current path
 ├── MIME type
 ├── size
 ├── timestamps
 ├── profile
 ├── extracted metadata
 ├── classification
 └── processing status

This unlocks duplicate detection, previously-processed detection, reclassification when rules change and eventually semantic search.
Importantly, a renamed file remains the same asset.
Phase 6 — Trust & Automation
Initially:
ALL CHANGES → HUMAN APPROVAL

Later profiles could have policies such as:
≥ 99%  → Auto approve
90–99% → Review
< 90%  → Flag

I'd keep this disabled until there's enough real-world history to understand failure modes.
The system should also learn from corrections without immediately requiring model training. User edits can simply become examples/context for future classifications.
Longer-term product shape
The eventual architecture I'd aim toward is:
                 DATA GOVERNOR
                      │
         ┌────────────┼────────────┐
         │            │            │
     UNDERSTAND     GOVERN       CATALOGUE
         │            │            │
     What is it?   Where does    What do we
                    it belong?    know about it?
         │            │            │
         └────────────┼────────────┘
                      │
                   PROPOSE
                      │
                    REVIEW
                      │
                   EXECUTE
                      │
                  AUDIT/UNDO

That keeps the project from becoming a collection of special-purpose file-renaming scripts.
For the first development milestone, I'd keep the scope deliberately narrow: Raspberry Pi/NAS deployment, one scan root, SQLite, Jellyfin movie/TV profile, scan → proposal → review → execute, and full undo. No automatic approval, deletion, OCR or generic profile editor yet.
Once that vertical slice works reliably, scanned documents should be milestone two. That's the point where we'll discover whether the abstraction really works.
From here, we can turn Phase 1 into an actual engineering backlog with epics → user stories → technical tasks → acceptance criteria, and establish the repository/service structure before writing code.