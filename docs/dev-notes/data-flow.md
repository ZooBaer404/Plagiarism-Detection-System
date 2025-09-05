<!--
START OF: data-flow.md
Purpose: Show how data moves across the system — from input to final output.
Update Frequency: On major architecture or I/O changes.
Location: docs/dev-notes/data-flow.md
-->

# Data Flow Overview

From user's click to DB writes and API responses, this doc tracks the *life journey* of your data.

---

## High-Level Flow

```txt
[User Input]
     ↓
[Frontend Validation]
     ↓
[API Gateway] --> [Auth Layer]
     ↓
[Business Logic]
     ↓
[Database and Memory]
     ↓
[Result Returned]
```

## Component-Wise Flow

Example: Plagiarism Submission

```txt
Document Upload → FileProcessor
               → Preprocessing
               → Result to SimilarityService
               → Save to DB → ReturnResult
```


## Realtime Events

- File Uploads → Async processing queue
- Detection Result → WebSocket / webhook for admins

> Visual diagrams live in [docs/design-assets/diagrams/] for fancier views.

<!-- END OF: data-flow.md -->
