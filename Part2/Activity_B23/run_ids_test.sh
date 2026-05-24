#!/usr/bin/env bash
# =============================================================
# run_ids_test.sh — Run Suricata IDS against synthetic PCAPs
# and collect all evidence for B23.
# =============================================================
set -euo pipefail

BASE="$(cd "$(dirname "$0")" && pwd)"
PCAP_DIR="$BASE/pcaps"
RULES="$BASE/rules/custom.rules"
LOG_DIR="$BASE/logs"
EVIDENCE="$BASE/evidence"

# Colours
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

echo "============================================================="
echo "  CITS2006 B23 — Suricata IDS Detection Test"
echo "============================================================="
echo ""

# ---- Step 0: Check Suricata -----------------------------------
if ! command -v suricata &>/dev/null; then
    echo -e "${RED}[ERROR] Suricata not found. Install with: brew install suricata${NC}"
    exit 1
fi
SURICATA_VER=$(suricata --build-info 2>&1 | head -1)
echo -e "${CYAN}IDS Engine:${NC} $SURICATA_VER"
echo ""

# ---- Step 1: Generate test PCAPs ------------------------------
echo -e "${YELLOW}[Step 1] Generating synthetic attack PCAPs...${NC}"
python3 "$BASE/generate_test_traffic.py"
echo ""

# ---- Step 2: Run Suricata on each PCAP ------------------------
echo -e "${YELLOW}[Step 2] Running Suricata against each PCAP...${NC}"
echo ""

PCAPS=("port_scan" "icmp_flood" "ssh_bruteforce" "http_scanner" "dns_exfil" "combined_attacks")
TOTAL_ALERTS=0

for name in "${PCAPS[@]}"; do
    pcap="$PCAP_DIR/${name}.pcap"
    run_log="$LOG_DIR/${name}"

    if [ ! -f "$pcap" ]; then
        echo -e "  ${RED}[SKIP] $pcap not found${NC}"
        continue
    fi

    rm -rf "$run_log"
    mkdir -p "$run_log"

    echo -e "  ${CYAN}--- Testing: ${name}.pcap ---${NC}"

    # Run Suricata in offline (PCAP) mode
    suricata -c /opt/homebrew/etc/suricata/suricata.yaml \
             -S "$RULES" \
             -r "$pcap" \
             -l "$run_log" \
             --set "outputs.0.fast.enabled=yes" \
             --set "app-layer.protocols.http.enabled=yes" \
             2>&1 | grep -v "^$" | head -5

    # Count and display alerts
    FAST_LOG="$run_log/fast.log"
    if [ -f "$FAST_LOG" ] && [ -s "$FAST_LOG" ]; then
        alert_count=$(wc -l < "$FAST_LOG" | tr -d ' ')
        TOTAL_ALERTS=$((TOTAL_ALERTS + alert_count))
        echo -e "  ${GREEN}  => $alert_count alert(s) triggered${NC}"
        # Show first 3 alerts
        head -3 "$FAST_LOG" | while IFS= read -r line; do
            echo "     $line"
        done
        if [ "$alert_count" -gt 3 ]; then
            echo "     ... ($((alert_count - 3)) more)"
        fi
    else
        echo -e "  ${RED}  => 0 alerts (no detection)${NC}"
    fi

    # Check for eve.json too
    EVE="$run_log/eve.json"
    if [ -f "$EVE" ]; then
        eve_alerts=$(grep -c '"event_type":"alert"' "$EVE" 2>/dev/null || echo 0)
        echo -e "  ${GREEN}  => eve.json: $eve_alerts structured alert records${NC}"
    fi

    echo ""
done

# ---- Step 3: Summary ------------------------------------------
echo "============================================================="
echo -e "${GREEN}  RESULTS SUMMARY${NC}"
echo "============================================================="
echo ""
echo -e "  Total alerts across all PCAPs: ${GREEN}${TOTAL_ALERTS}${NC}"
echo ""
echo "  Detection breakdown by PCAP:"
for name in "${PCAPS[@]}"; do
    FAST_LOG="$LOG_DIR/${name}/fast.log"
    if [ -f "$FAST_LOG" ] && [ -s "$FAST_LOG" ]; then
        cnt=$(wc -l < "$FAST_LOG" | tr -d ' ')
        echo -e "    ${GREEN}[DETECTED]${NC}  ${name}.pcap  — $cnt alert(s)"
    else
        echo -e "    ${RED}[MISSED]${NC}    ${name}.pcap  — 0 alerts"
    fi
done

echo ""
echo "  Suricata log files saved to: $LOG_DIR/"
echo ""

# ---- Step 4: Consolidate evidence ------------------------------
echo -e "${YELLOW}[Step 3] Consolidating evidence...${NC}"

# Merge all fast.log files into one evidence file
{
    echo "# Suricata IDS Alert Log — Consolidated"
    echo "# Generated: $(date '+%Y-%m-%d %H:%M:%S %Z')"
    echo "# Engine: $SURICATA_VER"
    echo ""
    for name in "${PCAPS[@]}"; do
        FAST_LOG="$LOG_DIR/${name}/fast.log"
        if [ -f "$FAST_LOG" ] && [ -s "$FAST_LOG" ]; then
            echo "=== ${name}.pcap ==="
            cat "$FAST_LOG"
            echo ""
        fi
    done
} > "$EVIDENCE/all_alerts.txt"

echo "  -> $EVIDENCE/all_alerts.txt"

# Write the full test output for terminal-screenshot rendering
echo ""
echo "============================================================="
echo "  All evidence saved. Run complete."
echo "============================================================="
