# test_cases.py
# Tests for the rule-based checker

from rules import check_request

tests = [
    # (request, expected_allowed, expected_reason)

    ({"user": "Alex", "role": "viewer", "actions": ["read"], "age": 15, "flags": []},
     True, None),

    ({"user": "Alex", "role": "viewer", "age": 15, "flags": []},
     False, "MISSING_REQUIRED_FIELD"),

    ({"user": "", "role": "viewer", "actions": ["read"], "age": 15, "flags": []},
     False, "EMPTY_USER"),

    ({"user": "Alex", "role": "king", "actions": ["read"], "age": 15, "flags": []},
     False, "ROLE_NOT_ALLOWED"),

    ({"user": "Alex", "role": "viewer", "actions": "read", "age": 15, "flags": []},
     False, "ACTIONS_NOT_A_LIST"),

    ({"user": "Alex", "role": "viewer", "actions": [], "age": 15, "flags": []},
     False, "ACTIONS_EMPTY"),

    ({"user": "Alex", "role": "admin", "actions": ["delete"], "age": 17, "flags": ["banned"]},
     False, "USER_BANNED"),

    ({"user": "Alex", "role": "guest", "actions": ["comment"], "age": 17, "flags": []},
     False, "GUEST_ONLY_READ"),

    ({"user": "Alex", "role": "viewer", "actions": ["post"], "age": 17, "flags": []},
     False, "VIEWER_NO_POST_DELETE"),

    ({"user": "Alex", "role": "editor", "actions": ["delete"], "age": 17, "flags": []},
     False, "EDITOR_NO_DELETE"),

    ({"user": "Kid", "role": "viewer", "actions": ["comment"], "age": 12, "flags": []},
     False, "UNDER_13_ONLY_READ"),

    ({"user": "Teen", "role": "viewer", "actions": ["post"], "age": 15, "flags": []},
     False, "UNDER_16_NO_POST_DELETE"),
]

for i, test in enumerate(tests, start=1):
    request, expected_allowed, expected_reason = test

    allowed, reason = check_request(request)

    if allowed == expected_allowed and reason == expected_reason:
        print("Test", i, "PASS ✅")
    else:
        print("Test", i, "FAIL ❌")
        print(" expected:", expected_allowed, expected_reason)
        print(" got:     ", allowed, reason)
