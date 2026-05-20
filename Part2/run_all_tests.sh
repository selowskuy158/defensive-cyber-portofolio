#!/usr/bin/env bash
# Convenience runner: executes the B19/B24/B25/B30 test suites in order
# so a marker can verify everything with a single command.
#
#   bash Part2/run_all_tests.sh
#
set -e
cd "$(dirname "$0")/.."

bold() { printf "\n\033[1;36m=== %s ===\033[0m\n" "$*"; }

bold "B19 - XSS exploit + 3-layer patch verification"
python3 Part2/Activity_B19/test_xss.py

bold "B24 - Flask RBAC permission matrix"
python3 Part2/Activity_B24/test_rbac.py

bold "B25 - Threat-intel aggregator (offline mode, malicious IP)"
python3 Part2/Activity_B25/threatintel.py --offline 185.220.101.1

bold "B30 - LSB watermark survivability test"
python3 Part2/Activity_B30/watermark.py test Part2/Activity_B30/evidence/watermarked.png 2>&1 \
    | grep -v DeprecationWarning | grep -v "img.getdata"

printf "\n\033[1;32mAll four B-activity test suites finished.\033[0m\n"
