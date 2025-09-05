<!--
START OF: docs/database/README.md

Purpose: Explain the structure, design, and rationale of the database.

Update Frequency: When schema or relationships change.

Location: docs/database/README.md
-->

# Database Documentation

## Overview

This module documents the structure, design decisions, and key components of the database used by the system. It includes schema diagrams, table descriptions, relationships, and performance considerations.

---

## Database Type & Engine

- **Engine**: PostgreSQL / SQLite
- **Rationale**: PostgreSQL and SQLite are both performant and meet our basic needs.

---

## Schema Structure
> Diagrams can be added later in `schema/` directory or linked via `.png/.svg`.

Refer to [schema.md](schema.md).

---

## Seed & Migration

- Migrations are handled via: Django's builtin migration.
- Seed command:
```bash
  python manage.py migrate
```

- Reset:
```bash
    python manage.py __app_name__ __migration_version__
```

## Security

- Sensitive fields (e.g., passwords) are hashed using bcrypt/scrypt

## Known Issues / TODOs

- [ ] Todo

## How to Use


1. [ ] **Database Schema** ([schema.md](schema.md))
   _Purpose:_ Describe the logical and physical structure of the database.
   _Update frequency:_ When new tables, columns, or relationships are added/modified.

2. [ ] **Indexes** ([indexes.md](indexes.md))
   _Purpose:_ Document indexing strategies to support performance and query optimization.
   _Update frequency:_ When indexes are added, changed, or removed.

3. [ ] **Seeding** ([seeding.md](seeding.md))
   _Purpose:_ Document how the database is seeded with initial/test data.
   _Update frequency:_ When new seed data scripts or strategies are added.

4. [ ] **Migrations** ([migrations.md](migrations.md))
   _Purpose:_ Document database schema migration approach.
   _Update frequency:_ When new migrations are introduced or policies change.

5. [ ] **Data Governance** ([data-governance.md](data-governance.md))
   _Purpose:_ Define rules and responsibilities for maintaining clean, compliant, and secure data.
   _Update frequency:_ As compliance or internal policies evolve.

6. [ ] **Entity-Relationship Diagrams** ([er-diagram.md](er-diagram.md))
   _Purpose:_ Entity-relationship diagram's history is located here. All of it.
   _Update frequency:_ When schema or relationships change.

<!-- END OF: docs/database/README.md -->
