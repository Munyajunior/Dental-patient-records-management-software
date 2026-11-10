# SmileScribePro: React/TypeScript + Tauri Migration (Track A) and Product Differentiation (Track B)

Date: 2026-11-10
Status: Draft for review

## 1. Context and correction

The current app (SmileScribePro v3.0) is a **CustomTkinter/Tkinter** desktop app, not PySide6
(PyQt5 appears only in `requirements.txt`). It is ~6.5k lines in 16 flat Python files. UI and
data access are mixed (raw `sqlite3` inside widget code). It depends on Windows-only APIs
(`win32print`, `win32api`, a Windows service with named pipes, `winreg`), generates documents
with `python-docx` templates, and stores data in a local `PRMS.db` (SQLite; tables: patient,
treatment, patientRemind, appointments, schedules, doctor, doctor_patient_records, archives).

## 2. Goals

- Replace the Tkinter UI with **React + TypeScript**, packaged for desktop with **Tauri 2**.
- **One shared UI codebase** reusable for desktop, web and (later) mobile.
- A **central hosted server** is the source of truth; all clients are thin.
- A real **update path** (desktop updater, CI-deployed web/server).
- Keep current features (parity) and migrate existing `PRMS.db` data.
- Meet modern standards (auth, audit, encryption, backups, accessibility, privacy).
- Prepare differentiating features (Track B) that make clinics willing to pay.

Non-goals (this spec): implementing Track B features, native mobile app, region-specific
integrations beyond those listed in section 7.

## 3. Target market (decisions made)

- Customers: small clinics (1-5 chairs) first; multi-branch groups later. Tenancy is designed
  for multi-clinic/branch from day one, but branch-level reporting UI is deferred.
- Launch regions: Cameroon/Francophone Africa and Sub-Saharan Africa generally.
  Implications: English + French (i18n from day one), mobile money (MTN/Orange via an
  aggregator), WhatsApp/SMS reminders, tolerance of poor connectivity.
- Card payments via **PayPal**.

## 4. Architecture

```
dental-app/ (pnpm workspaces monorepo)
├─ apps/
│  ├─ web/          Vite + React + TS
│  └─ desktop/      Tauri 2 shell around the shared UI (Windows first), updater plugin
├─ packages/
│  ├─ ui/           shared screens/components (Tailwind + shadcn/ui, i18n, a11y)
│  ├─ api-client/   typed client generated from the server OpenAPI schema
│  └─ domain/       shared TS types + zod validation
├─ server/          FastAPI + SQLAlchemy + Alembic, PostgreSQL
│  └─ modules: auth, tenants/clinics, patients, appointments, treatments, billing,
│     proformas, quotes, interventions, cashbook, archives, doctors, documents, reminders
└─ tools/migrate-sqlite/   one-off PRMS.db -> Postgres importer + verification report
```

Principles:
- Clients never touch the database; everything goes through `/api/v1` (OpenAPI is the contract).
- The server owns business logic, ported from the existing modules with Tkinter removed.
- The data layer is behind repositories so tests can use SQLite and prod uses Postgres.
- Desktop may later bundle a local sidecar for offline clinics; not in Track A.

## 5. Handling of legacy-specific pieces

| Legacy | Replacement |
|---|---|
| `python-docx` bills/proformas/consultation sheets | Server generates docx (and PDF) from existing templates; client downloads |
| `win32print` printing | Browser print (web); Tauri native print (desktop) |
| Windows service + named pipes reminders | Server scheduler (APScheduler) sending email; push/desktop notifications from clients |
| `permission.py` | JWT login (access + refresh), roles: admin, doctor, receptionist; audit log |
| `email_pass.py` credentials | Server-side secrets via environment/secret manager, never in the repo |
| Local `PRMS.db` | PostgreSQL + Alembic migrations; importer from SQLite |

## 6. Modern-standards baseline

- Authentication, role-based authorization, per-tenant data isolation, audit log of all
  patient-data access and changes.
- TLS everywhere, encryption at rest, automated backups and restore test.
- Patient data export and deletion/anonymization (GDPR/HIPAA-style privacy).
- Accessibility (WCAG 2.1 AA targets), keyboard navigation, dark mode, responsive layout.
- i18n (en, fr) with locale-aware dates/currency (XAF and others).
- Structured logging, error reporting, CI (lint, typecheck, tests), signed releases.

## 7. Track B: differentiators (separate spec and plan, built on Track A)

Prioritized for small clinics in the launch regions:
1. Interactive **odontogram** (per-tooth conditions and treatment history).
2. **No-show reduction:** WhatsApp/SMS/email reminders and online booking.
3. **Treatment plans/quotes** with shareable link, e-signature, instalments.
4. **Payments:** mobile money, PayPal card payments, invoices, cashbook reports.
5. Analytics dashboard (revenue, no-show rate, chair utilization).
6. Later: patient portal, X-ray/image attachments, inventory, AI-assisted notes.

Track A designs the schema and API so these slot in without rework (tooth-level records,
attachment storage abstraction, notification-channel abstraction, payment-provider abstraction).

## 8. Phasing (Track A), each phase shippable

1. Monorepo scaffold, CI, server skeleton, auth/roles, tenancy, schema, SQLite importer.
2. Patients, appointments, treatments in React (web + desktop).
3. Billing, proformas, quotes, interventions, docx/PDF output.
4. Cashbook, archives, doctors, reminders.
5. Hardening: tests, backups, signing + updater, deployment.
6. Cutover plan; remove Tkinter code.

## 9. Testing and verification

- Server: pytest, including characterization tests comparing bill/proforma totals and
  cashbook sums against the legacy logic on sample data.
- Migration: importer produces a report (row counts per table, monetary totals) that must match.
- UI: Vitest component tests, Playwright smoke tests for core flows on web and desktop.
- Security: dependency audit and basic authz tests (cross-tenant access must fail).

## 10. Risks and open items

- Data volume and quality in existing `PRMS.db` files (untyped columns, e.g. phone as int).
  The importer must normalize and report anomalies instead of failing silently.
- Hosting choice, cost and data-residency requirements are not decided; assume a single
  region deployment behind the API until chosen.
- Mobile money aggregator selection is deferred to Track B.
- Offline desktop mode is deferred; the API design must not preclude it.
