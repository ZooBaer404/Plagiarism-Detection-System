<!--
START OF: git-hooks.md
Purpose: Outlines the Git hooks in use and their responsibilities.
Update Frequency: Update this when a new hook is added or behavior is modified.
Location: docs/internal-tools/git-hooks.md
-->

# Git Hooks

## Purpose

Automate checks and enforce standards before Git operations are completed (e.g., before commits or pushes).

---

## Active Hooks

| Hook         | Trigger Event       | Function                                    |
|--------------|---------------------|---------------------------------------------|

---

## Setup

<!-- ```bash
./setup-git-hooks.sh
Hooks are installed into .git/hooks and symlinked to our hooks/ directory.
``` -->

---

## Commit Message Format

[type]([module]): short description

[optional longer description]

Valid types: feat, fix, docs, refactor, chore, test

---

## Notes


<!-- END OF: git-hooks.md -->
