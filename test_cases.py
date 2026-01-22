# test_cases.py
# Runs MANY requests and prints PASS/FAIL

ALLOWED_ROLES = {"guest", "viewer", "editor", "admin"}
BANNED_FLAGS = {"banned"}

tests = [
    # (request, expected_allowed, expected_reason)

    # 1) normal viewer
    ({"user": "Alex", "role": "viewer", "actions": ["read"], "age": 15, "flags": []},
     True, None),

    # 2) missing required field
    ({"user": "Alex", "role": "viewer", "age": 15, "flags": []},
     False, "MISSING_REQUIRED_FIELD"),

    # 3) empty user
    ({"user": "", "role": "viewer", "actions": ["read"], "age": 15, "flags": []},
     False, "EMPTY_USER"),

    # 4) role not allowed
    ({"user": "Alex", "role": "king", "actions": ["read"], "age": 15, "flags": []},
     False, "ROLE_NOT_ALLOWED"),

    # 5) actions not a list
    ({"user": "Alex", "role": "viewer", "actions": "read", "age": 15, "flags": []},
     False, "ACTIONS_NOT_A_LIST"),

    # 6) actions empty
    ({"user": "Alex", "role": "viewer", "actions": [], "age": 15, "flags": []},
     False, "ACTIONS_EMPTY"),

    # 7) banned flag (should block)
    ({"user": "Alex", "role": "admin", "actions": ["delete"], "age": 17, "flags": ["banned"]},
     False, "USER_BANNED"),

    # 8) guest tries comment (blocked)
    ({"user": "Alex", "role": "guest", "actions": ["read", "comment"], "age": 17, "flags": []},
     False, "GUEST_ONLY_READ"),

    # 9) viewer tries post (blocked)
    ({"user": "Alex", "role": "viewer", "actions": ["read", "post"], "age": 17, "flags": []},
     False, "VIEWER_NO_POST_DELETE"),

    # 10) editor tries delete (blocked)
    ({"user": "Alex", "role": "editor", "actions": ["delete"], "age": 17, "flags": []},
     False, "EDITOR_NO_DELETE"),

    # 11) under 13 tries comment (blocked)
    ({"user": "Kid", "role": "viewer", "actions": ["read", "comment"], "age": 12, "flags": []},
     False, "UNDER_13_ONLY_READ"),

    # 12) under 16 tries post (blocked)
    ({"user": "Teen", "role": "viewer", "actions": ["post"], "age": 15, "flags": []},
     False, "UNDER_16_NO_POST_DELETE"),
]

for i, test in enumerate(tests, start=1):
    request = test[0]
    expected_allowed = test[1]
    expected_reason = test[2]

    # --- RULE CHECK (copy of rules logic) ---
    allowed = True
    reason = None

    user = request.get("user")
    role = request.get("role")
    actions = request.get("actions")
    age = request.get("age")
    flags = request.get("flags")

    # normalize
    if isinstance(user, str):
        user = user.strip().lower()

    if isinstance(role, str):
        role = role.strip().lower()

    # required fields
    if user is None or role is None or actions is None:
        allowed = False
        reason = "MISSING_REQUIRED_FIELD"

    elif user == "":
        allowed = False
        reason = "EMPTY_USER"

    elif role not in ALLOWED_ROLES:
        allowed = False
        reason = "ROLE_NOT_ALLOWED"

    elif not isinstance(actions, list):
        allowed = False
        reason = "ACTIONS_NOT_A_LIST"

    elif actions == []:
        allowed = False
        reason = "ACTIONS_EMPTY"

    elif isinstance(flags, list) and ("banned" in flags):
        allowed = False
        reason = "USER_BANNED"

    elif role == "guest" and actions != ["read"]:
        allowed = False
        reason = "GUEST_ONLY_READ"

    elif role == "viewer" and (("post" in actions) or ("delete" in actions)):
        allowed = False
        reason = "VIEWER_NO_POST_DELETE"

    elif role == "editor" and ("delete" in actions):
        allowed = False
        reason = "EDITOR_NO_DELETE"

    elif isinstance(age, int) and age < 13 and actions != ["read"]:
        allowed = False
        reason = "UNDER_13_ONLY_READ"

    elif isinstance(age, int) and age < 16 and (("post" in actions) or ("delete" in actions)):
        allowed = False
        reason = "UNDER_16_NO_POST_DELETE"
    # --- END RULE CHECK ---

    pass_allowed = (allowed == expected_allowed)
    pass_reason = (reason == expected_reason)

    if pass_allowed and pass_reason:
        print("Test", i, "PASS ✅")
    else:
        print("Test", i, "FAIL ❌")
        print("  expected:", expected_allowed, expected_reason)
        print("  got:     ", allowed, reason)
