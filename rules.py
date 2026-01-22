# rules.py

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

# banned flag check
elif isinstance(flags, list) and flags == ["banned"]:
    allowed = False
    reason = "USER_BANNED"

# -------------------------
# Role Rules (NO 'in', NO '!=')
# -------------------------

# guest: must be exactly ["read"]
elif role == "guest" and actions == ["read"]:
    allowed = True
    reason = None

elif role == "guest" and actions != ["read"]:
    allowed = False
    reason = "GUEST_ONLY_READ"

# viewer: block if actions exactly matches any list containing post/delete
elif role == "viewer" and (actions == ["post"] or actions == ["delete"]):
    allowed = False
    reason = "VIEWER_NO_POST_DELETE"

elif role == "viewer" and (actions == ["read", "post"] or actions == ["read", "delete"]):
    allowed = False
    reason = "VIEWER_NO_POST_DELETE"

elif role == "viewer" and (actions == ["comment", "post"] or actions == ["comment", "delete"]):
    allowed = False
    reason = "VIEWER_NO_POST_DELETE"

elif role == "viewer" and (actions == ["read", "comment", "post"] or actions == ["read", "comment", "delete"]):
    allowed = False
    reason = "VIEWER_NO_POST_DELETE"

# editor: block if actions exactly matches any list containing delete
elif role == "editor" and actions == ["delete"]:
    allowed = False
    reason = "EDITOR_NO_DELETE"

elif role == "editor" and actions == ["read", "delete"]:
    allowed = False
    reason = "EDITOR_NO_DELETE"

elif role == "editor" and actions == ["comment", "delete"]:
    allowed = False
    reason = "EDITOR_NO_DELETE"

elif role == "editor" and actions == ["read", "comment", "delete"]:
    allowed = False
    reason = "EDITOR_NO_DELETE"

# -------------------------
# Age Rules (simple)
# -------------------------

elif isinstance(age, int) and age < 13 and actions != ["read"]:
    allowed = False
    reason = "UNDER_13_ONLY_READ"

elif isinstance(age, int) and age < 16 and (actions == ["post"] or actions == ["delete"]):
    allowed = False
    reason = "UNDER_16_NO_POST_DELETE"

# Final decision
if allowed:
    print("ALLOWED ✅")
else:
    print("BLOCKED ❌ —", reason)
