# SmileScribePro React/TypeScript + Tauri Migration (Track A) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Tkinter desktop app with a shared React/TS UI (web + Tauri desktop) over a hosted FastAPI/Postgres server, at feature parity with legacy, with legacy data migrated.

**Architecture:** pnpm monorepo. `server/` owns all business logic and exposes `/api/v1` with an OpenAPI contract; `packages/api-client` is generated from it; `packages/ui` holds all screens; `apps/web` and `apps/desktop` (Tauri 2) are thin shells. Every table carries `clinic_id`; repositories refuse cross-clinic access.

**Tech Stack:** Python 3.12, FastAPI, SQLAlchemy 2, Alembic, PostgreSQL (SQLite in unit tests), pytest, PyJWT, argon2-cffi, python-docx, APScheduler; pnpm, Vite, React 18, TypeScript, Tailwind + shadcn/ui, TanStack Query, react-router, react-i18next, zod, openapi-typescript/openapi-fetch, Vitest, Playwright; Tauri 2 + updater plugin.

**Spec:** `docs/superpowers/specs/2026-11-10-react-tauri-migration-design.md`

## Global Constraints

- Legacy is CustomTkinter (not PySide6); legacy files stay untouched until Task 22.
- Clients never access the database; all data goes through `/api/v1` described by OpenAPI.
- Roles: `admin`, `doctor`, `receptionist`. Auth: JWT access + refresh.
- Every patient-data read/write is audit-logged. Cross-tenant access must fail.
- Languages: `en` and `fr` from day one. Default currency XAF (integer amounts, no floats).
- Secrets only from environment/secret manager; `email_pass.py` credentials never copied into the repo.
- Legacy dates are `dd/mm/yyyy` text; the importer converts to real dates.
- Clinic name/address/phone/logo are per-clinic settings (legacy hardcodes "EMMANUEL DENTAL CLINIC").
- Accessibility target WCAG 2.1 AA; dark mode supported.
- Track B features (odontogram, WhatsApp/SMS, payments, analytics) are out of scope; schema keeps hooks only (tooth-level field, attachment/notification/payment abstractions are NOT built here).

## Review Focus

1. Duplicate/empty names, non-ASCII (French accents), and very long text in patient fields: stored and returned intact, never a 500.
2. Legacy phone stored as `int` loses leading zeros and `+`; importer keeps digits as text and reports anomalies.
3. Bad legacy dates (`31/02/2024`, blank, `2024-03-01`): importer reports and skips/nulls them, never aborts the whole import.
4. Same intervention on same tooth twice in a proforma/bill: rejected with 422, other-tooth duplicate allowed (legacy rule).
5. Token expiry mid-session and a user whose role changed or was removed: next request gets 401/403 and UI returns to login, no stale access.

---

## Phase 1: Foundation

### Task 1: Monorepo scaffold and CI

**Files:**
- Create: `package.json`, `pnpm-workspace.yaml`, `tsconfig.base.json`, `.github/workflows/ci.yml`, `server/pyproject.toml`, `.gitignore` additions, `docs/dev-setup.md`

**Interfaces:** Produces workspace scripts `pnpm lint|typecheck|test` and `make -C server test`.

- [ ] **Step 1:** Create workspace layout from spec section 4 (`apps/web`, `apps/desktop`, `packages/{ui,api-client,domain}`, `server`, `tools/migrate-sqlite`) with empty packages that each define `lint`, `typecheck`, `test` scripts.
- [ ] **Step 2:** CI runs server (ruff, mypy, pytest) and JS (eslint, tsc, vitest) on push/PR.
- [ ] **Step 3:** Run `pnpm install && pnpm -r typecheck` and `cd server && pytest`; Expected: PASS (zero tests collected is acceptable only for server here).
- [ ] **Step 4:** Remove tracked `__pycache__/*.pyc` and `PRMS.db` from git index (keep files locally; add to `.gitignore`). Commit.

### Task 2: Server skeleton and health endpoint

**Files:**
- Create: `server/app/main.py`, `server/app/config.py`, `server/tests/test_health.py`

**Interfaces:** Produces `create_app(settings: Settings | None = None) -> FastAPI`; `Settings` reads `DATABASE_URL`, `JWT_SECRET`, `ENV` from environment.

- [ ] **Step 1:** Write `test_health_returns_ok`: `GET /api/v1/health` -> 200, `{"status": "ok"}`.
- [ ] **Step 2:** Run `pytest server/tests/test_health.py -v`; Expected: FAIL (no app).
- [ ] **Step 3:** Implement `create_app` and `Settings`; app refuses to start in `ENV=prod` if `JWT_SECRET` is unset or equals a default.
- [ ] **Step 4:** Add `test_prod_requires_jwt_secret`; run both tests; Expected: PASS. Commit.

### Task 3: Database models, tenancy, Alembic baseline

**Files:**
- Create: `server/app/db/{base.py,session.py}`, `server/app/models/*.py`, `server/alembic/`, `server/tests/test_models.py`

**Interfaces:**
- Produces models (all with `id`, `clinic_id` except `Clinic`): `Clinic(name, address, phone, email, logo_path, currency, locale)`, `User(email, password_hash, role, is_active)`, `Doctor(name, address, email, phone)`, `Patient(name, doctor_id, address, phone: str, profession, dob: date|None, gender, medical_conditions, tooth, observations, treatment_plan, registered_on: date, archived_at: datetime|None)`, `Treatment(name, code, price: int)`, `Appointment(patient_name, phone, email, starts_at: datetime)`, `Intervention(doctor_id, patient_id, description, amount_paid: int, performed_on: date)`, `Bill`, `BillLine`, `Proforma`, `ProformaLine(tooth)`, `Quote`, `ReminderJob`, `AuditLog(user_id, action, entity, entity_id, at)`.
- Produces `TenantRepo[T]` with `get(id)`, `list(**filters)`, `add(obj)` always scoped by `clinic_id`.

- [ ] **Step 1:** Test `test_repo_cannot_read_other_clinic`: patient created in clinic A is not returned by `TenantRepo` bound to clinic B (`get` -> `None`, `list` -> `[]`).
- [ ] **Step 2:** Run; Expected: FAIL.
- [ ] **Step 3:** Implement models and `TenantRepo`; archived patients replace the legacy `archives` table (soft state via `archived_at`).
- [ ] **Step 4:** Generate Alembic baseline; test `alembic upgrade head` on a fresh SQLite and Postgres (CI service) creates all tables. Commit.

### Task 4: Auth, roles, audit log

**Files:**
- Create: `server/app/auth/{security.py,deps.py,router.py}`, `server/app/audit.py`, `server/tests/test_auth.py`

**Interfaces:**
- Produces `POST /api/v1/auth/login {email,password} -> {access_token, refresh_token}`, `POST /api/v1/auth/refresh`, dependency `require_role(*roles) -> CurrentUser(id, clinic_id, role)`, and `audit(user, action, entity, entity_id)`.

- [ ] **Step 1:** Tests: `test_login_success`, `test_login_wrong_password_401`, `test_expired_token_401`, `test_deactivated_user_401_on_next_request`, `test_receptionist_cannot_delete_patient_403`, `test_cross_clinic_token_cannot_read_patient`.
- [ ] **Step 2:** Run; Expected: FAIL.
- [ ] **Step 3:** Implement argon2 hashing, PyJWT tokens (access 15 min, refresh 7 days), role dependency that re-reads the user row on every request (covers deactivation/role change).
- [ ] **Step 4:** Run tests; Expected: PASS. Commit.

### Task 5: SQLite importer with verification report

**Files:**
- Create: `tools/migrate-sqlite/importer.py`, `tools/migrate-sqlite/tests/test_importer.py`, `tools/migrate-sqlite/tests/fixtures/legacy.db` (built by a fixture script, including bad rows)

**Interfaces:**
- Produces `import_legacy(db_path: Path, session: Session, clinic_id: int) -> ImportReport` where `ImportReport(counts: dict[str,int], skipped: list[Anomaly], money_total: int)`; CLI `python -m importer <db> --clinic <id> [--dry-run]`.

- [ ] **Step 1:** Tests: `test_row_counts_match_per_table`, `test_money_total_matches_sum_of_amount_paid`, `test_phone_kept_as_text_with_anomaly_noted` (legacy int `677170167` -> `"677170167"`), `test_bad_dates_reported_not_fatal` (`31/02/2024`, blank, ISO), `test_dry_run_writes_nothing`, `test_import_is_idempotent_on_rerun`.
- [ ] **Step 2:** Run; Expected: FAIL.
- [ ] **Step 3:** Implement mapping `patient->Patient`, `archives->Patient(archived_at set)`, `treatment->Treatment`, `doctor->Doctor`, `doctor_patient_records->Intervention`, `appointments->Appointment`, `schedules`/`patientRemind->ReminderJob`; parse `dd/mm/yyyy` strictly.
- [ ] **Step 4:** Run; Expected: PASS. Commit.

## Phase 2: Core flow (patients, appointments, treatments)

### Task 6: Patients, treatments, doctors, appointments API

**Files:**
- Create: `server/app/modules/{patients,treatments,doctors,appointments}/{router.py,schemas.py,service.py}`, `server/tests/test_{patients,treatments,appointments}.py`

**Interfaces:**
- Produces REST: `GET/POST /patients`, `GET/PATCH/DELETE /patients/{id}`, `POST /patients/{id}/archive`, `POST /patients/{id}/restore`, `GET /patients?q=&archived=`; same CRUD for `/treatments`, `/doctors`, `/appointments`. All write calls audit-logged.

- [ ] **Step 1:** Tests: `test_create_and_get_patient`, `test_search_matches_name_and_phone`, `test_unicode_and_long_text_roundtrip` (French accents, 5,000-char observations), `test_archive_hides_from_default_list_restore_returns`, `test_delete_requires_admin`, `test_write_creates_audit_entry`, `test_duplicate_names_allowed`.
- [ ] **Step 2:** Run; Expected: FAIL. **Step 3:** Implement. **Step 4:** Run; Expected: PASS.
- [ ] **Step 5:** Commit; export `openapi.json` via `server/scripts/export_openapi.py`.

### Task 7: API client and shared domain package

**Files:**
- Create: `packages/api-client/{src/index.ts,package.json}`, `packages/domain/src/*.ts`, `packages/api-client/tests/client.test.ts`

**Interfaces:**
- Produces `createApiClient({baseUrl, getToken, onUnauthorized}) -> Client` (typed from generated `schema.d.ts`); on 401 it refreshes once, then calls `onUnauthorized()`. `packages/domain` exports zod schemas `PatientInput`, `TreatmentInput`, `AppointmentInput`.

- [ ] **Step 1:** Tests (Vitest + msw): `refreshes_once_on_401_then_retries`, `calls_onUnauthorized_when_refresh_fails`, `PatientInput_rejects_empty_name`.
- [ ] **Step 2-4:** Run fail -> implement -> run pass. `pnpm generate:api` regenerates `schema.d.ts` from `openapi.json` and CI fails if it is stale. Commit.

### Task 8: UI shell, auth flow, i18n, theme

**Files:**
- Create: `packages/ui/src/{App.tsx,auth/*,layout/*,i18n/{en,fr}.json,theme/*}`, `apps/web/src/main.tsx`, tests alongside

**Interfaces:** Produces `<App apiBaseUrl platform: 'web'|'desktop'>`, `useAuth() -> {user, login, logout}`, route guard `<RequireRole roles>`. Platform differences (print, file save) go through `PlatformAdapter { print(url): Promise<void>; saveFile(blob, name): Promise<void> }` provided by each shell.

- [ ] **Step 1:** Tests: `redirects_to_login_when_unauthenticated`, `receptionist_does_not_see_admin_nav`, `language_switch_persists_and_translates_nav` (en/fr), `unauthorized_callback_returns_to_login`.
- [ ] **Step 2-4:** Run fail -> implement -> pass. Add axe check `no_a11y_violations_on_login`. Commit.

### Task 9: Patients, appointments, treatments screens

**Files:**
- Create: `packages/ui/src/features/{patients,appointments,treatments}/*`, tests alongside

**Interfaces:** Consumes `Client` (Task 7), `PatientInput` (Task 7). Produces `<PatientsPage/>`, `<PatientForm/>`, `<AppointmentsPage/>`, `<TreatmentsPage/>`.

- [ ] **Step 1:** Tests: `patient_list_debounced_search_calls_api`, `form_shows_zod_errors_for_empty_name`, `archive_asks_confirmation`, `keyboard_navigation_through_form`, `shows_empty_state_and_error_state`.
- [ ] **Step 2-4:** Run fail -> implement -> pass. Commit.

### Task 10: Web app wiring and Playwright smoke test

**Files:**
- Create: `apps/web/*`, `e2e/smoke.spec.ts`, `server/scripts/seed_demo.py`

- [ ] **Step 1:** E2E `login_create_patient_book_appointment_logout` against seeded server (docker compose: postgres + server + web).
- [ ] **Step 2:** Run `pnpm e2e`; Expected: FAIL then PASS after wiring. Commit. **Phase 2 ships here (web).**

### Task 11: Tauri 2 desktop shell

**Files:**
- Create: `apps/desktop/src-tauri/{tauri.conf.json,src/main.rs,capabilities/*}`, `apps/desktop/src/platform.ts`

**Interfaces:** Produces `desktopAdapter: PlatformAdapter` (native print via Tauri command, save dialog via `plugin-dialog`). Configurable server URL on first launch, stored in app config.

- [ ] **Step 1:** Vitest test `desktopAdapter.saveFile_invokes_dialog_and_writes` with mocked Tauri APIs.
- [ ] **Step 2-3:** Implement; `pnpm tauri build --debug` on Windows CI runner produces an installer; Expected: build succeeds, app launches to login. Commit.

## Phase 3: Billing, proformas, quotes, interventions, documents

### Task 12: Billing and proforma domain logic

**Files:**
- Create: `server/app/modules/billing/{service.py,router.py}`, `server/tests/test_billing.py`, `server/tests/legacy_cases.py`

**Interfaces:**
- Produces `compute_bill(lines: list[BillLineIn], discount_pct: int = 0) -> BillTotals(amount: int, discount: int, net: int)` (legacy discount is fixed 0; keep param), `validate_proforma_lines(lines) -> None` raising `DuplicateToothError` (legacy rule: same intervention on same tooth rejected; same intervention on different tooth allowed; legacy blank tooth then set = update). REST `POST /bills`, `GET /bills/{id}`, `POST /proformas`, `GET /proformas/{id}`, `POST /quotes`.

- [ ] **Step 1:** Characterization tests with hand-built cases from `bill.py:bill_updates` and `proforma.py:add_update_cart`: `bill_total_is_sum_of_prices`, `empty_cart_is_zero`, `same_tooth_twice_rejected_422`, `different_tooth_same_intervention_allowed`, `negative_or_non_numeric_price_rejected`, `amount_in_words_fr_en` (num2words, XAF).
- [ ] **Step 2-4:** Run fail -> implement -> pass. Commit.

### Task 13: Interventions and docx/PDF documents

**Files:**
- Create: `server/app/modules/documents/{docx_builder.py,router.py}`, `server/templates/{bill.docx,proforma.docx,consultation_sheet.docx}`, `server/tests/test_documents.py`

**Interfaces:**
- Produces `build_bill_docx(bill, clinic) -> bytes`, `build_proforma_docx(...)`, `build_cashbook_docx(rows, month, clinic) -> bytes`, `GET /bills/{id}/document?format=docx|pdf`. Clinic header uses `Clinic` settings, never hardcoded text. Templates copied from legacy `template.docx`/`consultation/consultation_sheet.docx`.

- [ ] **Step 1:** Tests: `docx_contains_clinic_name_and_patient_and_total`, `docx_header_uses_clinic_settings_not_emmanuel`, `pdf_export_returns_pdf_magic_bytes`, `document_for_other_clinic_404`.
- [ ] **Step 2-4:** Run fail -> implement (PDF via LibreOffice headless in the server image) -> pass. Commit.

### Task 14: Billing, proforma, quote, intervention screens

**Files:**
- Create: `packages/ui/src/features/{billing,proformas,quotes,interventions}/*`

**Interfaces:** Consumes `PlatformAdapter.print/saveFile` (Task 8), documents endpoint (Task 13).

- [ ] **Step 1:** Tests: `cart_total_updates_live`, `duplicate_tooth_shows_server_422_message`, `download_calls_saveFile_with_docx_blob`, `print_uses_adapter`, `fr_amount_in_words_displayed`.
- [ ] **Step 2-4:** Run fail -> implement -> pass. E2E `create_bill_and_download_docx`. Commit. **Phase 3 ships.**

## Phase 4: Cashbook, archives, doctors, reminders

### Task 15: Cashbook and reports API

**Files:**
- Create: `server/app/modules/cashbook/{service.py,router.py}`, `server/tests/test_cashbook.py`

**Interfaces:** Produces `cashbook(clinic_id, month: date) -> CashbookReport(rows: list[Row], per_patient_totals: dict[str,int], grand_total: int)`; `GET /cashbook?month=YYYY-MM`, document export via Task 13 builder.

- [ ] **Step 1:** Tests: `grand_total_equals_sum_of_rows`, `per_patient_totals_group_by_patient`, `month_boundaries_inclusive` (1st and last day), `month_with_no_rows_returns_zero_not_error`, `month_param_with_sql_metacharacters_returns_422` (legacy built SQL via f-string).
- [ ] **Step 2-4:** Run fail -> implement with parameterized queries -> pass. Commit.

### Task 16: Reminders scheduler and email

**Files:**
- Create: `server/app/modules/reminders/{scheduler.py,mailer.py}`, `server/tests/test_reminders.py`

**Interfaces:** Produces `due_reminders(now: datetime) -> list[ReminderJob]`, `Mailer.send(to, subject, body)` (SMTP from env), APScheduler job `run_due_reminders()` that is idempotent (marks `sent_at`).

- [ ] **Step 1:** Tests: `due_reminder_sent_once`, `rerun_does_not_resend`, `smtp_failure_retried_then_marked_failed`, `reminder_for_other_clinic_uses_that_clinics_sender`.
- [ ] **Step 2-4:** Run fail -> implement -> pass. Commit.

### Task 17: Cashbook, archives, doctors, reminders screens

**Files:**
- Create: `packages/ui/src/features/{cashbook,archives,doctors,reminders}/*`

- [ ] **Step 1:** Tests: `cashbook_month_picker_requests_month`, `archive_restore_roundtrip`, `doctor_form_validation`, `reminders_list_shows_sent_status`.
- [ ] **Step 2-4:** Run fail -> implement -> pass. Commit. **Phase 4 ships.**

## Phase 5: Hardening and release

### Task 18: Privacy features and settings

**Files:**
- Create: `server/app/modules/privacy/*`, `packages/ui/src/features/settings/*`, `server/tests/test_privacy.py`

**Interfaces:** Produces `GET /patients/{id}/export -> JSON+attachments zip`, `POST /patients/{id}/anonymize`, clinic settings `GET/PUT /clinic` (name, address, phone, logo, currency, locale).

- [ ] **Step 1:** Tests: `export_contains_all_patient_records`, `anonymize_removes_pii_keeps_financial_totals`, `anonymize_is_audited_and_admin_only`, `logo_upload_rejects_non_image`.
- [ ] **Step 2-4:** Run fail -> implement -> pass. Commit.

### Task 19: Backups and deployment

**Files:**
- Create: `deploy/{docker-compose.prod.yml,Dockerfile.server,backup.sh,restore-test.sh}`, `docs/ops.md`

- [ ] **Step 1:** CI job `restore_test`: dump seeded DB, restore into a fresh DB, assert row counts equal; Expected: PASS.
- [ ] **Step 2:** Document TLS termination, encrypted volume/backups, retention, secrets. Commit.

### Task 20: Signed desktop releases and updater

**Files:**
- Create: `.github/workflows/release.yml`, `apps/desktop/src-tauri/` updater config

- [ ] **Step 1:** Release workflow builds signed Windows installer, publishes updater manifest to GitHub Releases.
- [ ] **Step 2:** Manual verification checklist in `docs/release.md`: install v0.1.0, publish v0.1.1, app prompts and updates; record result. Commit.

### Task 21: Authorization and dependency security sweep

**Files:**
- Create: `server/tests/test_authz_matrix.py`

- [ ] **Step 1:** Parametrized test over every route x role x clinic: `route_matrix_matches_policy_table`; fails if a new route is not in the policy table.
- [ ] **Step 2:** Add `pip-audit` and `pnpm audit` to CI. Run; Expected: PASS. Commit.

## Phase 6: Cutover

### Task 22: Cutover and Tkinter removal

**Files:**
- Delete: legacy root `*.py`, `*.spec`, `*.bat`, `requirements.txt`, `PRMS.db`, `__pycache__`; Modify: `README.md`; Create: `docs/cutover.md`

- [ ] **Step 1:** Cutover runbook: freeze legacy, run importer on each clinic's `PRMS.db` with `--dry-run`, review report, run for real, verify counts and money totals against report, keep legacy copy for 30 days.
- [ ] **Step 2:** Only after sign-off, remove legacy files and update README (Tkinter -> new stack, screenshots later). Commit.

---

## Self-Review Notes

- Spec coverage: sections 4/5 -> Tasks 1-5, 8, 11-16; section 6 -> Tasks 3, 4, 8, 18-21; section 8 phases map 1:1 to the phases above; section 9 testing is embedded per task; Track B is excluded per spec section 7.
- Open item carried from spec: hosting region/provider is not chosen; Task 19 uses docker compose and must be adapted once chosen.
- Phase boundaries are shippable and each phase gets a fresh review before the next begins.
