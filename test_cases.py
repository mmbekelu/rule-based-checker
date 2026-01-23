# test_cases.py
# Upgraded tests for the rule-based checker (junior-friendly)

from rules import check_request

tests = [
    # ───────────────
    # VALID (happy path)
    # ───────────────
    (
        {"user": "Alex", "role": "viewer", "actions": ["read"], "age": 15, "flags": []},
        True,
        None
    ),

    # ───────────────
    # SCHEMA / REQUIRED FIELDS
    # ───────────────
    (
        {"user": "Alex", "role": "viewer", "age": 15, "flags": []},
        False,
        "MISSING_REQUIRED_FIELD"
    ),
    (
        {"user": "", "role": "viewer", "actions": ["read"], "age": 15, "flags": []},
        False,
        "EMPTY_USER"
    ),

    # ───────────────
    # TYPE VALIDATION
    # ───────────────
    (
        {"user": "Alex", "role": "viewer", "actions": "read", "age": 15, "flags": []},
        False,
        "ACTIONS_NOT_A_LIST"
    ),
    (
        {"user": "Alex", "role": "viewer", "actions": [], "age": 15, "flags": []},
        False,
        "ACTIONS_EMPTY"
    ),
    (
        {"user": "Alex", "role": "viewer", "actions": ["read"], "age": 17, "flags": "banned"},
        False,
        "FLAGS_NOT_A_LIST"
    ),

    # ───────────────
    # ROLE VALIDATION
    # ───────────────
    (
        {"user": "Alex", "role": "king", "actions": ["read"], "age": 15, "flags": []},
        False,
        "ROLE_NOT_ALLOWED"
    ),
    (
        {"user": "Alex", "role": "guest", "actions": ["comment"], "age": 17, "flags": []},
        False,
        "GUEST_ONLY_READ"
    ),
    (
        {"user": "Alex", "role": "viewer", "actions": ["post"], "age": 17, "flags": []},
        False,
        "VIEWER_NO_POST_DELETE"
    ),
    (
        {"user": "Alex", "role": "editor", "actions": ["delete"], "age": 17, "flags": []},
        False,
        "EDITOR_NO_DELETE"
    ),

    # ───────────────
    # ACTION VALUE VALIDATION
    # ───────────────
    (
        {"user": "Alex", "role": "viewer", "actions": ["hack"], "age": 17, "flags": []},
        False,
        "ACTION_NOT_ALLOWED"
    ),

    # ───────────────
    # FLAGS / BANS
    # ───────────────
    (
        {"user": "Alex", "role": "admin", "actions": ["delete"], "age": 17, "flags": ["banned"]},
        False,
        "USER_BANNED"
    ),

    # ───────────────
    # AGE RULES
    # ───────────────
    (
        {"user": "Kid", "role": "viewer", "actions": ["comment"], "age": 12, "flags": []},
        False,
        "UNDER_13_ONLY_READ"
    ),
    (
        {"user": "Teen", "role": "viewer", "actions": ["post"], "age": 15, "flags": []},
        False,
        "UNDER_16_NO_POST_DELETE"
    ),

    # ───────────────
    # PRIORITY / MULTIPLE VIOLATIONS
    # ───────────────
    (
        {"user": "", "role": "king", "actions": [], "age": 10, "flags": ["banned"]},
        False,
        "EMPTY_USER"  # first rule should win
    ),
]

for i, test in enumerate(tests, start=1):
    request, expected_allowed, expected_reason = test
    allowed, reason = check_request(request)

    if allowed == expected_allowed and reason == expected_reason:
        print(f"Test {i}: PASS ✅")
    else:
        print(f"Test {i}: FAIL ❌")
        print(" expected:", expected_allowed, expected_reason)
        print(" got:     ", allowed, reason)
