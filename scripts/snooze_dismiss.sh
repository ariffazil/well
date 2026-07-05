#!/usr/bin/env bash
# Dismiss the daily WELL biometric snooze — removes the cron line.
# Guide, inject script, and state.json all stay put.
# Re-arm anytime with: /root/WELL/snooze_arm.sh

set -euo pipefail

CRON_LINE='0 1 * * * /root/WELL/snooze_check.sh >> /var/log/well-biometric-snooze.log 2>&1'

NEW_CRON="$(crontab -l 2>/dev/null | grep -v '/root/WELL/snooze_check.sh' || true)"
echo "$NEW_CRON" | crontab -

if crontab -l 2>/dev/null | grep -q 'snooze_check.sh'; then
  echo "  ✗ still present — check: crontab -l"
  exit 1
fi

echo "  ✓ snooze dismissed — daily reminder stopped"
echo ""
echo "Guide and inject script remain at:"
echo "  /root/WELL/SNOOZE_BIOMETRIC.md"
echo "  /root/WELL/biometric_inject.sh"
echo ""
echo "Re-arm with: /root/WELL/snooze_arm.sh"
