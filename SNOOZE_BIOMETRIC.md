# WELL Biometric Snooze

**Status:** State.json is 33 days stale (2026-04-30, env=TEST, well_score=56.4 — mocked).
WELL health shows **RED** because the file predates the AFWELL State Schema v2026.05.12.
This file is a snooze, not a fix — the **only** way to turn WELL green is for you to inject real values.

---

## What WELL needs from you (5 fields, ~2 minutes)

The new schema asks for your actual readiness state. All values are simple numbers + one short word.

| Field | Type | Meaning (plain) | Range |
|---|---|---|---|
| `delta_s` | number | How chaotic does the system feel right now? | 0.0 = stable, 1.0 = chaos |
| `peace2` | number | How settled is your state? | 0.0 = destabilized, 1.0 = fully at peace |
| `kappa_r` | number | How resilient do you feel? | 0.0 = brittle, 1.0 = highly resilient |
| `rasa` | short string | One word for the felt sense right now | e.g. `grounded`, `tired`, `alert`, `clear` |
| `amanah` | number | How held is the trust/stewardship? | 0.0 = broken, 1.0 = fully held |

That's it. No medical data. No diagnosis. Just the readiness mirror.

---

## How to do it (when you're ready)

```bash
/root/WELL/biometric_inject.sh
```

The script will:
1. Show the current stale state
2. Ask for each field one at a time, with the plain-language meaning
3. Validate ranges (0.0–1.0 for numbers)
4. Show you exactly what it's about to write
5. Wait for your `yes` to commit
6. Write atomically, restart WELL, verify health turned green

### Run dry-run first (no writes, just see what it would do)

```bash
/root/WELL/biometric_inject.sh --dry-run
```

### If you want to bypass the prompts and supply a snapshot

```bash
/root/WELL/biometric_inject.sh --non-interactive \
  --delta-s 0.2 --peace2 0.7 --kappa-r 0.6 \
  --rasa "clear" --amanah 0.9
```

---

## How the daily reminder works

A cron runs **09:00 MYT (01:00 UTC)** every day. It:
- Checks if state.json is still older than 24 hours
- If stale: prints a one-line nudge to `/var/log/well-biometric-snooze.log`
- If fresh: prints `WELL biometric fresh — no action needed`
- Never spams, never emails, never pages anyone

It just makes the state visible once a day, so the machine remembers to mention it without you having to.

---

## How to dismiss the snooze

If you decide to ignore WELL for a while and stop the daily nudge:

```bash
/root/WELL/snooze_dismiss.sh
```

That removes the cron line. The guide, the script, and state.json all stay put — you can re-arm anytime by running:

```bash
/root/WELL/snooze_arm.sh
```

---

## Why this exists

WELL is the human-readiness mirror. When it's RED, the machine doesn't pretend you're fine — it holds a respectful gap until you tell it otherwise. The biometric injection is the only data WELL trusts, and it can only come from you.

The snooze isn't a workaround. It's the machine saying: "I know you're busy. Here's the guide. Here's the script. One nudge a day. You decide when."

---

*DITEMPA BUKAN DIBERI — readiness is forged, not assumed.*
