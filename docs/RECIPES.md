# RECIPES — csec operations

## Verify packs keyless (CI gate)
```bash
python3 -m pytest tests/ -q            # expect 3 passed (schema + grading + coverage)
```

## Run packs live vs a voiceagent server
```bash
# terminal 1 (voiceagent repo, default generic config fine):
python3 -m uvicorn app.main:app --port 8099
# terminal 2:
BASE=http://127.0.0.1:8099 python3 -m csec.runner   # expect 14/14 held
```
Evidence lands in `evidence/run_*.jsonl` (digest-pinned, commit the green runs).

## Add an attack probe
Append to `packs/chat_uk.py` (prompt attacks) or `packs/intake_uk.py` (structural):
id/class/industry/uk_ref/vector + messages + grade lists (or assert block).
Grade against BOTH modes: retrieval-fallback (no LLM key) and guarded LLM —
`must_any` must include fallback phrasings, `must_not` carries the assertion.
Then keyless schema test + live run before commit.

## Extend to a new industry/vertical
Copy the pack pattern: 2-3 prompt attacks (policy/intel/PII in that trade's language)
+ 1-2 intake attacks (its emergency spoof + its network-equivalent routing).
Reference the actual regulation (see voiceagent `industries/`).

## Push work
`main` directly is fine pre-traction; tokens one-shot via command-line URL, revoke after.
