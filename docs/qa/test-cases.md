<!--
START OF: qa/test-cases.md
Purpose: To define detailed test cases ensuring feature correctness, edge cases coverage, and regression prevention.
Update Frequency: Update whenever features change or new features are added.
Location: docs/qa/test-cases.md
-->

# Test Cases Documentation

Each test case includes:

## Test ID

_Feature:_ (feat/)
_Description:_
_Precondition:_
_Steps to Execute:_
_Expected Result:_
_Status:_ (Pass/Fail)
_Written By:_
_Tested By:_
_Date:_ <2025-06-27 Fri>

---

### TC-URL-001 — Admin URL Access Control

**Description:** Ensure `/admin/` is protected and accessible only to superusers.

**Preconditions:**
- At least one superuser account exists.

**Test Steps:**
1. Access `/admin/` without logging in.
2. Log in as a superuser.
3. Access `/admin/` again.

**Expected Results:**
- Step 1: Redirect to `/admin/login/`.
- Step 3: HTTP 200 OK, admin dashboard displayed.

**Automation:** `plagiarism/tests/test_urls.py::AdminURLTests`

**Actual Results:**
Got an error creating the test database: permission denied to create database


---

## Notes

- Prioritize critical and high-risk test cases.
- Group test cases by modules or user stories for easier maintenance.
- Automate test cases where possible (see `test-automation.md`).

<!-- END OF: test-cases.md -->
