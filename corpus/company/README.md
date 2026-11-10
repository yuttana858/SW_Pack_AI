---
id: kb.company.readme
title: Company data folder - supplier-certified and house data
domain: company
tags: [company, supplier-certified, house-data, override, material-records, tolerances, customer-specs]
applies_to: [corrugated, folding-carton, rigid, flexible, cushioning, pallet]
confidence: reference
status: draft
last_reviewed: 2026-11-09
reviewer: unreviewed
supersedes: []
sources: []
---

# Company data folder

## What this folder is

This folder holds **your company's own data**: supplier-certified board records, house-measured values, house tolerances and customer specifications. It is the only place in the corpus where `confidence: supplier-certified` is allowed.

## Precedence rule (overrides everything else)

- Data in `company/` **overrides** every other file in the corpus. Retrieval ranks it first.
- Any value elsewhere marked *industry-typical* ("replace with supplier/house data in `company/`") must be replaced by the matching record here when one exists.
- If a `company/` record conflicts with a published standard (e.g. a carrier rule minimum), the assistant reports both and flags the conflict; it never silently uses the lower value for compliance.

## Layout

| Path | Content |
|---|---|
| `company/materials/_template.yaml` | Empty board material record. Copy it, never edit the template itself |
| `company/materials/<supplier>-<grade-id>.yaml` | One file per supplier grade (per plant if properties differ) |
| `company/tolerances/` | House manufacturing and dimensional tolerances (create when needed) |
| `company/customers/` | Customer specifications (create when needed) |

The field definitions and validation rules for material records are in `materials/material-record-schema.md`.

## Rules for adding a record

1. Copy `_template.yaml` to `<supplier>-<grade-id>.yaml`.
2. Fill values from the supplier certificate or your own lab report; keep units as defined in the schema (mm, g/m², kN/m, kPa, %).
3. Set `calibrated: true` and `provenance: supplier-certified` (or `house-measured`) only when `certificateRef`, `certificateDate` and `approvedBy` are filled.
4. Re-certify before `validUntil`; do not delete superseded records — set the old one's `notes` to "superseded by <id>".
5. Do not put confidential customer data here unless the RAG deployment is access-controlled for it.
