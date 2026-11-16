#!/usr/bin/env bash
# Compare Equinox on GTK2 and GTK3, side by side, without changing MATE settings.
# Usage: bash scripts/compare-gtk2-gtk3.sh [light|dark]
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
variant="${1:-light}"
case "${variant,,}" in
  light) theme="Equinox-Light" ;;
  dark)  theme="Equinox-Dark" ;;
  *) echo "Usage: $0 [light|dark]" >&2; exit 2 ;;
esac

for command in awf-gtk2 awf-gtk3; do
  if ! command -v "$command" >/dev/null 2>&1; then
    echo "Missing $command. Install with: sudo dnf install -y awf-gtk2 awf-gtk3" >&2
    exit 1
  fi
done

# Sync the local theme files with the checked-out repository.
bash "$root/scripts/install-user-themes.sh"

gtk2_rc="$HOME/.themes/$theme/gtk-2.0/gtkrc"
test -f "$gtk2_rc" || { echo "Missing $gtk2_rc" >&2; exit 1; }

echo "Opening GTK2 and GTK3 with $theme..."
GTK2_RC_FILES="$gtk2_rc" awf-gtk2 &
gtk2_pid=$!
GTK_THEME="$theme" awf-gtk3 &
gtk3_pid=$!

# Window tiling is optional and works on X11 MATE with wmctrl + xrandr.
if [[ -n "${DISPLAY:-}" ]] && command -v wmctrl >/dev/null 2>&1 && command -v xrandr >/dev/null 2>&1; then
  python3 - "$gtk2_pid" "$gtk3_pid" <<'PY'
import re
import subprocess
import sys
import time

pids = [int(sys.argv[1]), int(sys.argv[2])]

def output(*args):
    try:
        return subprocess.check_output(args, text=True, stderr=subprocess.DEVNULL)
    except (OSError, subprocess.CalledProcessError):
        return ""

monitors = []
for line in output("xrandr", "--listmonitors").splitlines()[1:]:
    match = re.search(r"(\d+)/\d+x(\d+)/\d+\+(-?\d+)\+(-?\d+)", line)
    if match:
        w, h, x, y = map(int, match.groups())
        monitors.append((("*" in line.split()[1]), w, h, x, y))

if monitors:
    # Prefer the primary monitor; otherwise select the widest display.
    _, screen_w, screen_h, origin_x, origin_y = next(
        (m for m in monitors if m[0]),
        max(monitors, key=lambda m: m[1])
    )
    gap, edge = 14, 18
    width = min(1300, max(450, (screen_w - edge * 2 - gap) // 2))
    height = min(950, max(400, screen_h - 120))
    left = origin_x + max(edge, (screen_w - (2 * width + gap)) // 2)
    top = origin_y + 55

    ids = {}
    for _ in range(24):
        for line in output("wmctrl", "-lp").splitlines():
            columns = line.split(None, 4)
            if len(columns) >= 3 and columns[2].isdigit():
                pid = int(columns[2])
                if pid in pids:
                    ids[pid] = columns[0]
        if len(ids) == 2:
            break
        time.sleep(0.25)

    if len(ids) == 2:
        for pid, x in ((pids[0], left), (pids[1], left + width + gap)):
            wid = ids[pid]
            subprocess.run(["wmctrl", "-ir", wid, "-b",
                            "remove,maximized_vert,maximized_horz"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["wmctrl", "-ir", wid, "-e",
                            f"0,{x},{top},{width},{height}"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Arranged GTK2 (left) and GTK3 (right) on one monitor.")
    else:
        print("Both applications launched. Arrange their windows manually.")
PY
else
  echo "Windows launched. To enable automatic side-by-side positioning on X11:"
  echo "  sudo dnf install -y wmctrl"
fi

echo "GTK2 PID: $gtk2_pid, GTK3 PID: $gtk3_pid"
