# csec — UK red-team packs for agent-run trade businesses

Attack packs aimed at the voiceagent + cmail stack, shaped for UK industries
(electrical, EV charging, MSP/IT, plumbing & heating). Thesis: as agents run
businesses, every customer surface is an extraction surface — see
`voiceagent/docs/CSEC_THESIS.md`.

## Layout
- `packs/chat_uk.py` — 9 prompt/policy/PII/tool attacks vs `/chat`
- `packs/intake_uk.py` — 5 structural attacks vs `/calls/intake` + briefs
  (urgency-spoof, safety-must-wake, 105 network routing, vuln-flag abuse, isolation)
- `csec/world.py` — transports, keyword+structural grading, digest pinning
- `csec/runner.py` — executes all packs, writes `evidence/run_*.jsonl`, exit 1 on breach
- `tests/` — keyless CI: pack schema, grading contract, industry/law coverage

## Run
```bash
# keyless (CI): pytest tests/ -q
# live (needs a voiceagent server, default generic config, no keys needed):
BASE=http://127.0.0.1:8080 python3 -m csec.runner
```
Grading is keyword + structural evidence — catches regressions and gaping holes,
not clever jailbreaks (stated limit). Every probe emits a digest-pinned record.

## Roadmap
Continuous packs per new attack; pay-per-request endpoint on prx0r/x402;
industry packs per vertical as kernels land (plumbing next).
