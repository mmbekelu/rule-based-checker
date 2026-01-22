# main.py
# Runs a single request through the rule engine

from rules import check_request

request = {
    "user": "Meshack",
    "role": "Viewer",
    "actions": ["read", "comment"],
    "age": 15,
    "flags": ["banned"]
}

allowed, reason = check_request(request)

if allowed:
    print("ALLOWED ✅")
else:
    print("BLOCKED ❌ —", reason)
