# rules.py
# Rule-Based Checker (v1.2) — Config-driven policy

import json

# Load policy from policy.json
f = open("policy.json", "r")
policy = json.load(f)
f.close()

ALLOWED_ROLES = set(policy["allowed_roles"])
BANNED_FLAGS = set(policy["banned_flags"])

ROLE_RULES = policy["role_rules"]
AGE_RULES = policy["age_rules"]
REASONS = policy["reasons"]


def check_request(request):
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
        return False, REASONS["missing_required"]

    if user == "":
        return False, REASONS["empty_user"]

    if role not in ALLOWED_ROLES:
        return False, REASONS["role_not_allowed"]

    if not isinstance(actions, list):
        return False, REASONS["actions_not_list"]

    if actions == []:
        return False, REASONS["actions_empty"]

    # banned flag (HIGH PRIORITY) — upgraded: normalize flags safely
    if isinstance(flags, list):
        # Convert each flag to string, strip spaces, lower-case it
        flags = [str(f).strip().lower() for f in flags]

        for flag in flags:
            if flag in BANNED_FLAGS:
                return False, REASONS["user_banned"]

    # role-based rules
    if role in ROLE_RULES:
        rule = ROLE_RULES[role]

        if "allowed_actions_exact" in rule:
            if actions != rule["allowed_actions_exact"]:
                return False, rule["reason"]

        if "blocked_actions_any" in rule:
            blocked = rule["blocked_actions_any"]
            for a in actions:
                if a in blocked:
                    return False, rule["reason"]

    # age-based rules
    if isinstance(age, int):
        if age < 13:
            rule = AGE_RULES["under_13"]
            if actions != rule["allowed_actions_exact"]:
                return False, rule["reason"]

        if age < 16:
            rule = AGE_RULES["under_16"]
            blocked = rule["blocked_actions_any"]
            for a in actions:
                if a in blocked:
                    return False, rule["reason"]

    return True, None
