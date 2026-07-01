# ERRORS

> Record of errors, risks, regressions, and their fixes. Sequential
> numbering (E001, E002, … for errors; R001, R002, … for risks).

---

## E001 — Incorrect docs/agent_ledger/README.md content

### Symptom

An Explore agent created `docs/agent_ledger/README.md` with content
about a "runtime agent decision audit log" (JSON-lines runtime logs).
This is a v0.2.0 feature placeholder, not the maintenance ledger the
project needs.

### Detection

Read the file and compared content against the intended maintenance
ledger structure (SESSION_START, NEXT, PROGRESS, etc.).

### Fix

Rewrote `docs/agent_ledger/README.md` to describe the maintenance ledger
directory and its 7 files. The runtime audit-log concept is noted as a
separate v0.2.0 plan.

### Regression Test

When adding files to `docs/agent_ledger/`, verify the README accurately
describes the directory's purpose.

---

## E002 — oss_readiness_check.py missing risky word scan

### Symptom

The `scripts/oss_readiness_check.py` created by an Explore agent only
checked file existence and a placeholder email. It did not scan for
high-risk wording (game names, anti-detection terms, etc.).

### Detection

Read the script and compared against the user's specification, which
requires scanning for Chinese and English high-risk words.

### Fix

Enhanced the script with a `check_risky_words()` function implementing
Chinese zero-tolerance and English negative-context exemption. Added
`--run-tests` option and enhanced output.

### Regression Test

Run `python scripts/oss_readiness_check.py` before every commit. The
script must report 0 Chinese hits and 0 unexempted English hits.

---

## R001 — English high-risk words in safety documentation

### Risk

Safety-boundary documents (README, SECURITY.md, CONTRIBUTING.md,
docs/safety-boundaries.md, CHANGELOG.md) legitimately mention prohibited
concepts like "cheating", "botting", and "anti-detection" in a
prohibitive context ("not intended for cheating"). A naive word scan
would flag these as violations.

### Mitigation

The oss_readiness_check uses negative-context exemption: if the hit line
or its ±1 line neighbors contain negation markers (not, never, no,
prohibit, reject, remove, without, etc.), the hit is exempted.

### Monitoring

If a new document uses high-risk words without a clear negation context,
the scan will flag it. Review each flag manually.

---

## R002 — "bypasses" technical usage in src/fsm.py

### Risk

`src/fsm.py` line 188 uses "bypasses" in a technical sense: "This
bypasses on_exit callbacks of the old state." Scanning for the bare word
"bypass" would produce a false positive.

### Mitigation

The scan uses the precise phrase "bypass detection" instead of the bare
word "bypass". See decision D006 for details.

### Monitoring

If future code introduces "bypass" in a security context (e.g., "bypass
anti-cheat"), the scan will not catch it with the current phrase list.
Periodically review the English word list in
`scripts/oss_readiness_check.py` to ensure coverage.
