# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**HMSS (Hostel Management and Search System)** — a university group project (SWD392-G1) focused on software modeling and design using the **COMET (Concurrent Object Modeling and Architectural Design) methodology** by Gomaa. This is a documentation/modeling repo, not a running application. The deliverable is a `.docx` report with diagrams.

**Domain:** Web-based hostel room search and rental management with four actor roles: Visitor, Tenant, Owner, System Admin. 18 use cases covering search, rental requests, property/room management, verification, and admin controls.

## Repository Structure

- `260310-hmss/` — Main project artifacts organized by COMET phases:
  - `step-1.*` — **Phase 1: Requirements Modeling** (actors, use cases, relationships, UC diagram)
  - `phase-2/` — **Phase 2: Analysis Modeling** (static model, communication diagrams as `.md` + `.drawio`)
  - `phase-3/` — **Phase 3: Design Modeling** (design communication diagrams, class interface specs, design class diagram blueprints). Two variants per UC: pure-COMET (`uc-XX-name/`) and ASP.NET+React stack-specific (`uc-XX-name-aspnet-react/`)
  - `diagrams/` — Draw.io source files for analysis communication diagrams (`uc-XX.drawio`)
  - `plans/` — Implementation plans for design phases
- `scripts/fill_hmss_requirements_docx.py` — Python script to auto-populate the requirements section of the Word report from markdown artifacts
- `output/doc/` — Generated `.docx` reports and exported diagram images
  - `generate_hmss_report.py` — Script to generate the full report
- `skills/` — Custom Claude Code skills for generating COMET artifacts:
  - `gomaa-class-design/` — Generates Phase 3 design artifacts (class interfaces, design class diagrams) from Phase 2 inputs
  - `gomaa-class-design-markdown/` — Markdown-only variant
  - `drawio-design-class-diagram/` — Generates Draw.io XML for design class diagrams
  - `drawio-communication-diagram/` — Generates Draw.io XML for communication diagrams
- `tools/` — Python tooling modules
- `tmp_gomaa_*.txt` — Reference text extracted from Gomaa textbook chapters

## COMET Deliverables Checklist

Each artifact below is a concrete deliverable. Status: done/partial/todo.

### Phase 1: Requirements Modeling (Black box — what the system does)
| # | Artifact | Format | Status |
|---|----------|--------|--------|
| 1 | Use Case Diagram | `.drawio` / UML | done |
| 2 | Use Case Descriptions (18 UCs) | `.md` text (main seq, alt seq, pre/post conditions, NFRs) | done |
| 3 | Activity Diagrams (optional) | `.drawio` / UML | skipped |

### Phase 2: Analysis Modeling (Problem domain — identify software objects)
| # | Artifact | Format | Status |
|---|----------|--------|--------|
| 4 | System Context Class Diagram | `.md` | done |
| 5 | Entity Class Diagram (Static Model) | `.md` (attributes only, no operations yet) | done |
| 6 | Communication Diagrams (per UC, 18x) | `.md` + `.drawio` (simple messages, business-level names) | done |
| 7 | Statechart Diagrams (for stateful control classes) | `.md` / `.drawio` | partial |

### Phase 3: Design Modeling (Solution domain — technical design for coding)
| # | Artifact | Format | Status |
|---|----------|--------|--------|
| 8 | Integrated Communication Diagram | `.md` (merge all UC comm diagrams) | todo |
| 9 | Subsystem Architecture Diagram | `.md` / `.drawio` (Client/Server layers) | todo |
| 10 | Concurrent Communication Diagram | `.md` (sync/async arrows, actual method calls) | todo |
| 11 | Class Interface Specs + Design Class Diagram | `.md` + `.drawio` (full operations, in/out params, pre/post) | partial (UC-17 done, rest todo) |
| 12 | Deployment Diagram | `.drawio` / UML (physical nodes, network links) | todo |

### Phase 4: Detailed Design (Implementation-ready)
| # | Artifact | Format | Status |
|---|----------|--------|--------|
| 13 | Pseudocode / Algorithm Specs | `.md` text (logic inside each method) | todo |
| 14 | Relational Database Schema | `.md` (tables, PKs, FKs derived from Entity Class Diagram) | todo |

Each use case follows the naming convention: `uc-XX-kebab-case-name`
Phase 3 has two variants per UC: pure-COMET (`uc-XX-name/`) and ASP.NET+React stack-specific (`uc-XX-name-aspnet-react/`)

## Key Commands

```bash
# Generate requirements section in Word report
python scripts/fill_hmss_requirements_docx.py

# Generate full report
python output/doc/generate_hmss_report.py
```

## Conventions

- Use case artifacts are markdown files with structured tables and sections
- Draw.io files (`.drawio`) are XML-based; companion `.md` files describe the same diagram in markdown
- Phase 3 has two output variants: pure COMET (academic) and ASP.NET+React (stack-specific simplified design)
- Class interface specs follow template in `skills/gomaa-class-design/references/class-interface-spec-template.md`
- Design class diagram blueprints follow template in `skills/gomaa-class-design/references/design-class-diagram-blueprint-template.md`

## Custom Skills

When working on COMET modeling tasks, use the project-specific skills:
- `/comet-requirements` — Phase 1 guidance
- `/comet-analysis` — Phase 2 guidance
- `/comet-design` — Phase 3 guidance
- `gomaa-class-design` skill — Automated Phase 3 artifact generation from Phase 2 inputs
