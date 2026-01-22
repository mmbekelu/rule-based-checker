# Rule-Based Checker (v1.0)

A deterministic **validation + permission layer** that checks a structured request and returns a clear decision:

- ✅ `ALLOWED`
- ❌ `BLOCKED` + a **reason code**

This runs **before AI or downstream logic** so the system stays predictable and safe.

---

## ✨ What It Does

- **Normalizes input**
  - Lowercases `user` and `role` (`" Viewer "` → `"viewer"`)
- **Validates required fields**
  - Ensures `user`, `role`, and `actions` exist
- **Validates types**
  - Ensures `actions` is a list (not a string)
- **Enforces role-based permissions**
  - `guest` → read-only
  - `viewer` → cannot post/delete
  - `editor` → cannot delete
- **Applies age-based limits**
  - under 13 → read-only
  - under 16 → cannot post/delete
- **Blocks banned users with high priority**
  - if `"banned"` is in `flags` → immediate block
- **Returns explainable reason codes**
  - e.g. `ROLE_NOT_ALLOWED`, `USER_BANNED`, `UNDER_16_NO_POST_DELETE`

---

## 🧠 Why I Built This

AI should not “guess” safety rules or permissions.

This checker ensures requests are **validated and explainable** before they reach any AI system, which makes the pipeline:

- Safer ✅
- Predictable ✅
- Testable ✅
- Explainable ✅

---

## 🗂 Project Structure

- `rules.py`  
  Contains the rule engine: `check_request(request) -> (allowed, reason)`

- `main.py`  
  Runs a single request through the rule engine and prints the decision

- `test_cases.py`  
  Runs multiple test requests and prints PASS/FAIL (basic test harness)

---

## ⚙️ How It Works

Rules run in a fixed order:

1. Required fields
2. Normalization + basic validation
3. Banned flag (high priority)
4. Role permissions
5. Age restrictions

The checker stops on the **first failing rule** and returns the reason code.

No randomness. No guessing. Pure deterministic behavior.

---

## ✅ Example

### Allowed Request

```json
{
  "user": "Mbekelu",
  "role": "viewer",
  "actions": ["read", "comment"],
  "age": 15,
  "flags": ["new_user"]
}
Expected output:

ALLOWED ✅

Blocked Request (viewer tries to post)
{
  "user": "Alex",
  "role": "viewer",
  "actions": ["post"],
  "age": 17,
  "flags": []
}
Expected output:

BLOCKED ❌ — VIEWER_NO_POST_DELETE

▶️ How To Run
Run the main example
python main.py
Run tests
python test_cases.py
