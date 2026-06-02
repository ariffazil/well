#!/usr/bin/env bash
# Arm the daily WELL biometric snooze — adds the cron line back.
# Idempotent: safe to run when already armed.

set -euo pipefail

CRON_LINE='0 1 * * * /root/WELL/snooze_check.sh >> /var/log/well-biometric-snooze.log 2>&1'

EXISTING="$(crontab -l 2>/dev/null || true)"
if echo "$EXISTING" | grep -q 'snooze_check.sh'; then
  echo "  ✓ already armed — nothing to do"
  exit 0
fi

{ echo "$EXISTING"; echo "$CRON_LINE"; } | crontab -

if crontab -l 2>/dev/null | grep -q 'snooze_check.sh'; then
  echo "  ✓ snooze armed — daily reminder at 09:00 MYT (01:00 UTC)"
  echo ""
  echo "Dismiss with: /root/WELL/snooze_dismiss.sh"
else
  echo "  ✗ failed to install cron line"
  exit 1
fi
