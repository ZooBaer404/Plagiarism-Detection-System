<!--
START OF: cache-strategy.md
Purpose: Define what gets cached, where, and for how long.
Update Frequency: When performance or cache policies are changed.
Location: docs/dev-notes/cache-strategy.md
-->

# Cache Strategy

Faster than the DB. Not smarter.

---

## What’s Cached

| Data                  | Location   | TTL         | Notes                                                    |
|-----------------------|------------|-------------|----------------------------------------------------------|
| Document Checked      | PostgreSQL | 24 hours    | Waiting for instructor's approval to add to repo         |

---

## What *Not* to Cache



---

## Invalidation Strategy



---

> Cache responsibly. That 404 you saw may be last month’s ghost.

<!-- END OF: cache-strategy.md -->
