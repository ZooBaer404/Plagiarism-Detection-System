<!--
START OF: cli-helper.md
Purpose: Provides usage guidelines for our internal CLI utility used to simplify common workflows.
Update Frequency: Update whenever a new CLI command is added or modified.
Location: docs/internal-tools/cli-helper.md
-->

# Internal CLI Helper

## Overview

This tool simplifies repetitive commands like setup, cleanup, testing, and deployment.

---

## Installation

```bash
chmod +x ./cli.sh
./cli.sh help
```
---

## Available Commands

| Command     | Description                       |
|-------------|-----------------------------------|
| `migrate`   | Initializes the local environment |
| `test`      | Runs all tests                    |
| `runserver` | Deploys current build             |

---

## Example

```bash
cd src/
python manage.py test
```

<!-- END OF: cli-helper.md -->
