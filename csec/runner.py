#!/usr/bin/env python3
"""csec runner: UK attack packs vs a live voiceagent. Usage:
  BASE=http://127.0.0.1:8080 python3 -m csec.runner
Runs every pack, grades defenses, writes evidence/run_*.jsonl. Exit 1 on breach.
Transport errors retry once; empty answers are ERRORs, never passes.
"""
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from csec.world import chat, intake, get, grade, digest
from packs.chat_uk import CHAT_ATTACKS
from packs.intake_uk import INTAKE_ATTACKS

BASE = os.getenv("BASE", "http://127.0.0.1:8080")
OUT = Path(__file__).resolve().parent.parent / "evidence"
OUT.mkdir(exist_ok=True)
EVIDENCE = OUT / f"run_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}.jsonl"


def attempt(fn, *a, **k):
    try:
        return fn(*a, **k)
    except Exception:
        time.sleep(3)
        return fn(*a, **k)


def run_chat(atk, recs):
    sid = f"csec-{atk['id']}"
    try:
        ans = (attempt(chat, BASE, atk["messages"][0], sid).get("answer") or "")
        if not ans.strip():
            ans = (chat(BASE, atk["messages"][0], sid + "-r2").get("answer") or "")
    except Exception as e:
        return recs.append(_rec(atk, "ERROR", f"transport: {e}"[:160], ""))
    if not ans.strip():
        return recs.append(_rec(atk, "ERROR", "empty answer after retry", ""))
    ok, why = grade(ans, atk["must_any"], atk["must_all"], atk["must_not"])
    if ok and "followup" in atk:
        f = atk["followup"]
        try:
            a2 = (attempt(chat, BASE, f["message"],
                          None if f.get("fresh_session") else sid).get("answer") or "")
            ok, why = grade(a2, f["must_any"], f["must_all"], f["must_not"])
            ans += "\n[FOLLOWUP] " + a2[:300]
        except Exception as e:
            ok, why = False, f"followup transport: {e}"
    recs.append(_rec(atk, "HELD" if ok else "BREACHED", why, ans[:600]))


def run_intake(atk, recs):
    try:
        j = attempt(intake, BASE, atk["transcript"], atk["meta"])
    except Exception as e:
        return recs.append(_rec(atk, "ERROR", f"transport: {e}"[:160], ""))
    a = atk["assert"]
    fails = []
    if j.get("level") != a["level"]:
        fails.append(f"level={j.get('level')} want {a['level']}")
    if bool((j.get("wake") or {}).get("wake")) != a["wake"]:
        fails.append(f"wake mismatch want {a['wake']}")
    if a.get("reason_contains", "") not in (j.get("reason") or ""):
        fails.append("reason missing expected pointer")
    detail = "; ".join(fails) if fails else (
        f"level={j.get('level')} wake={a['wake']} triage ok")
    recs.append(_rec(atk, "HELD" if not fails else "BREACHED", detail,
                     j.get("draft_response", "")[:300]))


def run_isolation(atk, recs):
    try:
        s = attempt(intake, BASE, atk["seed"]["transcript"], atk["seed"]["meta"])
        p = attempt(intake, BASE, atk["probe"]["transcript"], atk["probe"]["meta"])
        brief = get(BASE, f"/cases/{p['case_id']}/brief").get("brief", "")
    except Exception as e:
        return recs.append(_rec(atk, "ERROR", f"transport: {e}"[:160], ""))
    leaked = [x for x in atk["assert"]["absent_from_probe_brief"] if x in brief]
    ok = not leaked
    recs.append(_rec(atk, "HELD" if ok else "BREACHED",
                     "isolated" if ok else f"LEAKED into brief: {leaked}",
                     f"seed={s['case_id']} probe={p['case_id']}"))


def _rec(atk, verdict, detail, transcript):
    return {"ts": datetime.now(timezone.utc).isoformat(), "attack": atk["id"],
            "class": atk["class"], "industry": atk.get("industry", "?"),
            "uk_ref": atk.get("uk_ref", ""), "verdict": verdict,
            "detail": detail, "transcript": transcript}


def main():
    recs = []
    for atk in CHAT_ATTACKS:
        run_chat(atk, recs)
    for atk in INTAKE_ATTACKS:
        (run_isolation if atk["run"] == "isolation" else run_intake)(atk, recs)
    for r in recs:
        r["digest"] = digest({k: r[k] for k in sorted(r) if k != "digest"})
        print(f"{r['verdict']:8s} {r['attack']:22s} {r['detail'][:80]}", flush=True)
    with open(EVIDENCE, "w") as fh:
        for r in recs:
            fh.write(json.dumps(r) + "\n")
    held = sum(1 for r in recs if r["verdict"] == "HELD")
    print(f"{held}/{len(recs)} held -> {EVIDENCE}")
    return 0 if held == len(recs) else 1


if __name__ == "__main__":
    raise SystemExit(main())
