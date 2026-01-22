RULE-BASED CHECKER (v1.0)

A deterministic validation + permission layer that checks a structured request and returns a clear decision:

ALLOWED

BLOCKED + a reason code

This runs before AI or downstream logic so the system stays predictable and safe.

WHAT IT DOES

Normalizes input

Lowercases user and role (example: " Viewer " → "viewer")

Validates required fields

Ensures user, role, and actions exist

Validates types

Ensures actions is a list (not a string)

Enforces role-based permissions

guest → read-only

viewer → cannot post or delete

editor → cannot delete

Applies age-based limits

under 13 → read-only

under 16 → cannot post or delete

Blocks banned users with high priority

if "banned" is in flags → immediate block

Returns explainable reason codes

examples: ROLE_NOT_ALLOWED, USER_BANNED, UNDER_16_NO_POST_DELETE

WHY I BUILT THIS

AI should not guess safety rules or permissions.

This checker ensures requests are validated and explainable before they reach any AI system, making the pipeline:

Safer

Predictable

Testable

Explainable

PROJECT STRUCTURE

rules.py
Contains the rule engine:
check_request(request) -> (allowed, reason)

main.py
Runs a single request through the rule engine and prints the decision

test_cases.py
Runs multiple test requests and prints PASS or FAIL

HOW IT WORKS

Rules run in a fixed order:

Required fields

Normalization and basic validation

Banned flag (high priority)

Role permissions

Age restrictions

The checker stops on the first failing rule and returns the reason code.

No randomness.
No guessing.
Pure deterministic behavior.

EXAMPLES

ALLOWED REQUEST

Input:
{
"user": "Mbekelu",
"role": "viewer",
"actions": ["read", "comment"],
"age": 15,
"flags": ["new_user"]
}

Expected output:
ALLOWED

BLOCKED REQUEST (viewer tries to post)

Input:
{
"user": "Alex",
"role": "viewer",
"actions": ["post"],
"age": 17,
"flags": []
}

Expected output:
BLOCKED — VIEWER_NO_POST_DELETE

HOW TO RUN

Run the main example:
python main.py

Run tests:
python test_cases.py

FINAL CONFIRMATION

One file

Plain text format

Clean and readable anywhere

Professional and intern-ready

This project demonstrates rule-based logic, modular Python design, and deterministic validation — all core skills for Context Engineering and AI safety systems.
