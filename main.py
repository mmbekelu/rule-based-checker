# Rule-Based Checker (v0.1)
# Deterministic validation of structured data

ALLOWED_ROLES = {"guest", "viewer", "editor", "admin"}
BANNED_FLAGS = {"banned"}

request = {
    "user": "Meshack",
    "role": "Viewer",
    "actions": ["read", "comment"],
    "age": 15,
    "flags": ["new_user"]
}

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

# banned flag check (HIGH PRIORITY)
elif isinstance(flags, list) and ("banned" in flags):
    allowed = False
    reason = "USER_BANNED"

# role-based action rules
elif role == "guest" and actions != ["read"]:
    allowed = False
    reason = "GUEST_ONLY_READ"

elif role == "viewer" and (("post" in actions) or ("delete" in actions)):
    allowed = False
    reason = "VIEWER_NO_POST_DELETE"

elif role == "editor" and ("delete" in actions):
    allowed = False
    reason = "EDITOR_NO_DELETE"

# age-based rules
elif isinstance(age, int) and age < 13 and actions != ["read"]:
    allowed = False
    reason = "UNDER_13_ONLY_READ"

elif isinstance(age, int) and age < 16 and (("post" in actions) or ("delete" in actions)):
    allowed = False
    reason = "UNDER_16_NO_POST_DELETE"

# Final decision
if allowed:
    print("ALLOWED ✅")
else:
    print("BLOCKED ❌ —", reason)
