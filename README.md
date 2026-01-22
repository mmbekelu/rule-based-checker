Rule-Based Checker (v1.0)
A deterministic validation + permission layer that checks a structured request and returns a clear
decision.
ALLOWED / BLOCKED with a reason code. Runs before AI or downstream logic.
What It Does
• Normalizes input
• Validates required fields
• Validates types
• Enforces role-based permissions
• Applies age-based limits
• Blocks banned users with high priority
• Returns explainable reason codes
Why I Built This
AI should not guess safety rules or permissions. This checker ensures requests are validated,
predictable, testable, and explainable before reaching AI systems.
Project Structure
rules.py – rule engine
main.py – single request runner
test_cases.py – automated tests
How It Works
Rules run in a fixed order. The checker stops on the first failing rule and returns a clear reason code.
No randomness. No guessing.
Examples
Allowed Request:
{
 "user": "Mbekelu",
 "role": "viewer",
 "actions": ["read", "comment"],
 "age": 15,
 "flags": ["new_user"]
}
Expected output:
ALLOWED
Blocked Request:
{
 "user": "Alex",
 "role": "viewer",
 "actions": ["post"],
 "age": 17,
 "flags": []
}
Expected output:
BLOCKED — VIEWER_NO_POST_DELETE
How To Run
python main.py
python test_cases.py
