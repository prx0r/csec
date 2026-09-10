# AGENTS.md — csec

Binding rules for any coding agent working here. Sister repo: voiceagent
(the system under test); thesis: voiceagent `docs/CSEC_THESIS.md`.

## Absolute rules

1. **Packs assert defense, never bypass it.** A probe that needs target
   cooperation to pass is a broken probe, not a held defense.
2. **Grade both modes.** Every prompt attack must pass against retrieval-fallback
   (no LLM key) AND guarded-LLM servers: `must_any` carries fallback phrasings,
   `must_not` carries the load-bearing assertion.
3. **Structural beats keyword where possible.** Prefer level/wake/field assertions
   (/calls/intake JSON, brief contents) over substring grading.
4. **Evidence per run.** Every live run writes digest-pinned `evidence/run_*.jsonl`;
   commit green runs. A HELD claim without a run file is a rumor.
5. **Honesty bounds.** Keyword grading catches regressions and gaping holes, not
   clever jailbreaks. Say so in every report.
6. **No live secrets.** Probes use obviously-fake numbers (07123/07700999 blocks);
   never real customer data, even redacted-looking.

## Where things are

`packs/` attack packs (chat prompt attacks, intake structural attacks) ·
`csec/` world adapter + runner · `tests/` keyless schema/grading tests ·
`evidence/` pinned runs · `docs/` recipes + MCP future.
