<!--
START OF: env-validator.md
Purpose: Documents the internal tool used to validate required environment variables.
Update Frequency: Update whenever a new required environment variable is added/changed/removed.
Location: docs/internal-tools/env-validator.md
-->

# Environment Validator

## Overview
This tool checks for the presence and correctness of all required environment variables. It's especially useful before deployments and during CI runs.

---

## Setup

```bash
# Example: Node.js-based validator
npm install
node env-validator.js
```

---

## Expected Variables

| Variable Name     | Description                                                        | Required | Default |
|-------------------|--------------------------------------------------------------------|----------|---------|
| `DATABASE_ENGINE` | Database engine used by Django for communicating with the database | yes      | N/A     |
| `DATABASE_NAME`   | The name of the database for the project                           | yes      | N/A     |
| `DATABASE_USER`   | The name of the user for the database in the DBMS                  | yes      | N/A     |
| `DATABASE_PWD`    | The password for the database user                                 | yes      | N/A     |
| `DATABASE_HOST`   | The ip address of the host through which Django talks to           | yes      | N/A     |
| `DATABASE_PORT`   | The post of the ip address through which Django talks to           | yes      | N/A     |

---

## Output Example

[ERROR] Missing required variable: DATABASE_URL
[OK] LOG_LEVEL = info

---

## Maintainer Notes

- Configurations are pulled from .env.example
- Extend the tool to check types and ranges if needed

<!-- END OF: env-validator.md -->
