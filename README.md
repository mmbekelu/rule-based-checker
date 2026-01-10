Rule-Based Checker (v0.1)

This program checks a structured request and decides if it is ALLOWED or BLOCKED based on clear rules.

What it does

Normalizes input (lowercases user and role)

Checks required fields (user, role, actions)

Blocks empty or invalid values

Enforces role-based permissions

Blocks banned users immediately

Applies age-based action limits

Returns a clear reason when blocked

Why I made this

AI should not decide safety or permissions by itself.
This checker blocks unsafe or invalid requests before they reach AI or other logic.

It makes systems:

safer

predictable

explainable

How it works

The program checks rules in order.

If a rule fails → the request is BLOCKED

The first failure decides the reason

If no rules fail → the request is ALLOWED

No loops.
No guessing.
Only explicit logic.

Example

Input

{
    "user": "Meshack",
    "role": "viewer",
    "actions": ["read", "comment"],
    "age": 15,
    "flags": ["new_user"]
}


Output

ALLOWED ✅


Input

{
    "user": "Alex",
    "role": "viewer",
    "actions": ["post"]
}


Output

BLOCKED ❌ — VIEWER_NO_POST_DELETE
