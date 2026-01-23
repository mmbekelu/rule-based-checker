# main.py
# Runs a single request through the rule engine (demo)

from rules import check_request


def is_minimally_valid_request(req) -> tuple[bool, str]:
    """
    Minimal sanity check (NOT full validation):
    - Ensures the request is a non-empty dict.
    Returns: (ok, error_reason)
    """
    if not isinstance(req, dict):
        return False, "REQUEST_NOT_DICT"
    if not req:
        return False, "REQUEST_EMPTY"
    return True, ""


def run_demo() -> None:
    # Example request (local testing / demo)
    request = {
        "user": "Meshack",
        "role": "Viewer",
        "actions": ["read", "comment"],
        "age": 15,
        "flags": ["new_user"],
    }

    ok, error = is_minimally_valid_request(request)
    if not ok:
        print("ERROR ⚠️ —", error)
        return

    # check_request returns:
    # - allowed (bool): True if request passes rules, False otherwise
    # - reason (str): short reason code/message explaining a block (or "" if allowed)
    allowed, reason = check_request(request)

    if allowed:
        print("ALLOWED ✅")
    else:
        print("BLOCKED ❌ —", reason)


if __name__ == "__main__":
    run_demo()
