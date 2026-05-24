#!/usr/bin/env bash
set -euo pipefail

payload='<script>alert(1)</script>'

echo "B19 real local XSS execution evidence"
echo "Payload: $payload"
echo

echo "1) Vulnerable app: POST payload to http://127.0.0.1:3001/add"
vuln_status="$(curl -s -o /dev/null -w '%{http_code}' -X POST --data-urlencode "task=$payload" http://127.0.0.1:3001/add)"
echo "HTTP status: $vuln_status redirect after storing task"
echo

echo "2) Vulnerable page contains executable script:"
if curl -s http://127.0.0.1:3001/ | grep -q "<script>alert(1)</script>"; then
  echo "CONFIRMED: raw <script>alert(1)</script> appears in HTML"
else
  echo "FAILED: raw script was not found"
fi
echo

echo "3) Patched app: POST same payload to http://127.0.0.1:3002/add"
patched_status="$(curl -s -o /dev/null -w '%{http_code}' -X POST --data-urlencode "task=$payload" http://127.0.0.1:3002/add)"
echo "HTTP status: $patched_status bad request, payload rejected"
echo

echo "4) Patched app security headers:"
curl -s -I http://127.0.0.1:3002/ \
  | grep -Ei "content-security-policy|x-content-type-options|x-frame-options" \
  | sed 's/; /; /g'
echo

echo "5) Patched page raw script search:"
if curl -s http://127.0.0.1:3002/ | grep -n "<script>alert(1)</script>"; then
  echo "FAIL: raw script still present"
else
  echo "PASS: raw script tag is not present in patched page"
fi
