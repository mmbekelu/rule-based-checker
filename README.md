# 🧱 **Rule-Based Checker (v0.1)**

This program checks a **structured request** and decides whether it is **ALLOWED** or **BLOCKED** using clear, deterministic rules.

---

## ✅ **What It Does**

* **Normalizes input**

  * Lowercases `user` and `role`
* **Checks required fields**

  * Ensures `user`, `role`, and `actions` exist
* **Blocks invalid values**

  * Empty fields
  * Invalid roles or actions
* **Enforces role-based permissions**

  * Prevents unauthorized actions
* **Blocks banned users immediately**
* **Applies age-based limits**

  * Restricts actions based on age
* **Returns a clear reason when blocked**

  * No vague errors or guessing

---

## 🧠 **Why I Made This**

AI should **not** decide safety or permissions by itself.

This checker blocks **unsafe or invalid requests** *before* they reach AI or downstream logic.

It makes systems:

* **Safer**
* **Predictable**
* **Explainable**

---

## ⚙️ **How It Works**

* Rules are checked **in a fixed order**
* If **any rule fails** → the request is **BLOCKED**
* The **first failed rule** determines the reason
* If **no rules fail** → the request is **ALLOWED**

**No loops.**
**No guessing.**
**Only explicit logic.**

---

## 📌 **Examples**

### ✔️ Allowed Request

**Input**

```json
{
    "user": "Meshack",
    "role": "viewer",
    "actions": ["read", "comment"],
    "age": 15,
    "flags": ["new_user"]
}
```

**Output**

```
ALLOWED ✅
```

---

### ❌ Blocked Request

**Input**

```json
{
    "user": "Alex",
    "role": "viewer",
    "actions": ["post"]
}
```

**Output**

```
BLOCKED ❌ — VIEWER_NO_POST_DELETE
```
