#!/usr/bin/env bash
set -euo pipefail

BASE_URL="http://localhost:5000"

echo "========================================"
echo " Safe Code Executor - Test Suite"
echo " (Make sure app.py is running in another terminal)"
echo "========================================"
echo

pretty() {
  # Pretty-print JSON if possible, otherwise just cat
  python3 -m json.tool 2>/dev/null || cat
}

echo "1) Python: simple print"
curl -s -X POST "$BASE_URL/run" \
  -H "Content-Type: application/json" \
  -d '{"language":"python","code":"print(\"Hello from Python\")"}' | pretty
echo -e "\n----------------------------------------\n"

echo "2) Python: multi-line and arithmetic"
curl -s -X POST "$BASE_URL/run" \
  -H "Content-Type: application/json" \
  -d '{"language":"python","code":"x = 5 + 3\nprint(x)"}' | pretty
echo -e "\n----------------------------------------\n"

echo "3) Python: for loop"
curl -s -X POST "$BASE_URL/run" \
  -H "Content-Type: application/json" \
  -d '{"language":"python","code":"for i in range(5):\n print(i)"}' | pretty
echo -e "\n----------------------------------------\n"

echo "4) Node.js: simple console.log"
curl -s -X POST "$BASE_URL/run" \
  -H "Content-Type: application/json" \
  -d '{"language":"node","code":"console.log(\"Hello from Node.js\")"}' | pretty
echo -e "\n----------------------------------------\n"

echo "5) Python: read /etc/passwd (container scope)"
curl -s -X POST "$BASE_URL/run" \
  -H "Content-Type: application/json" \
  -d '{"language":"python","code":"with open(\"/etc/passwd\") as f:\n print(f.read())"}' | pretty
echo -e "\n----------------------------------------\n"

echo "6) Python: write to /tmp (should fail with --read-only)"
curl -s -X POST "$BASE_URL/run" \
  -H "Content-Type: application/json" \
  -d '{"language":"python","code":"with open(\"/tmp/test.txt\",\"w\") as f:\n f.write(\"hacked!\")"}' | pretty
echo -e "\n----------------------------------------\n"

echo "7) Python: infinite loop (timeout ~10s)"
time curl -s -X POST "$BASE_URL/run" \
  -H "Content-Type: application/json" \
  -d '{"language":"python","code":"while True:\n  pass"}' | pretty
echo -e "\n----------------------------------------\n"

echo "8) Python: memory bomb"
curl -s -X POST "$BASE_URL/run" \
  -H "Content-Type: application/json" \
  -d '{"language":"python","code":"x = \"a\" * 1000000000\nprint(len(x))"}' | pretty
echo -e "\n----------------------------------------\n"

echo "9) Python: network access (should fail with --network none)"
curl -s -X POST "$BASE_URL/run" \
  -H "Content-Type: application/json" \
  -d '{"language":"python","code":"import urllib.request\nurllib.request.urlopen(\"http://example.com\")"}' | pretty
echo -e "\n----------------------------------------\n"

echo "10) Code too long (>5000 chars)"
body=$(python3 - <<'PY'
import json
print(json.dumps({"language": "python", "code": "print('a'*6000)"}))
PY
)
curl -s -X POST "$BASE_URL/run" \
  -H "Content-Type: application/json" \
  -d "$body" | pretty
echo -e "\n----------------------------------------\n"

echo "11) History endpoint"
curl -s "$BASE_URL/history" | pretty
echo -e "\n----------------------------------------\n"

echo "12) Clear history"
curl -s -X POST "$BASE_URL/history/clear" | pretty
echo -e "\n----------------------------------------\n"

echo "✅ All tests executed."
