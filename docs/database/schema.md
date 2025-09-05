<!--
START OF: schema.md
Purpose: Describe the logical and physical structure of the database.
Update Frequency: When new tables, columns, or relationships are added/modified.
Location: docs/database/schema.md
-->

# Database Schema Documentation

This document outlines the structure of the system's primary data storage — aka, the tables you’ll break when you forget a foreign key constraint.

---

## Table Overview

| Table Name                                | Purpose                                                                                          |
|-------------------------------------------|--------------------------------------------------------------------------------------------------|
| `admin`                                   | Stores essential infomation about the 'superuser' of the system.                                 |
| `university`                              | Stores information about registering university.                                                 |
| `university_approval`                     | Stores whether university's registration is approved by admin or not.                            |
| `university_login`                        | Stores university's login session.                                                               |
| `instructor`                              | Stores information about instructor registering for university.                                  |
| `instructor_approval`                     | Stores whether instructor's registration is approved by university or not.                       |
| `instructor_login`                        | Stores instructor's login session.                                                               |
| `research_repository_upload`              | Stores the documents uploaded as repository.                                                     |
| `research_document`                       | Stores basic information about the uploaded document.                                            |
| `research_repository_upload_error`        | Stores any errors that occur while uploading research document.                                  |
| `research_document_parse_text`            | Stores the parsed content from the research document.                                            |
| `research_document_references`            | Stores the references contained in the research document.                                        |
| `research_document_parse_error`           | Stores any errors that occurred while parsing the research document.                             |
| `research_document_section_tokens`        | Stores tokenized sections from parsed research documents.                                        |
| `research_document_basic_stats`           | Stores basic statistics collected from research documents.                                       |
| `research_document_enhanced_text`         | Stores parsed, no-punctuation, lower-cased, sentence-and-paragraph-start-and-end-marked.         |
| `research_document_text_vector`           | Stores the vector generated from text using SentenceBERT.                                        |
| `upload_checking_document_upload`         | Stores the documents uploaded as repository.                                                     |
| `upload_checking_document`                | Stores the data related to documents upload for checking.                                        |
| `upload_checking_document_upload_error`   | Stores any errors that occur while uploading checking document.                                  |
| `upload_checking_document_parse_text`     | Stores the parsed content from the research document.                                            |
| `upload_checking_document_references`     | Stores the references contained in the research document.                                        |
| `upload_checking_document_parse_error`    | Stores any errors that occurred while parsing the checking document.                             |
| `upload_checking_document_section_tokens` | Stores tokenized sections from parsed checking documents.                                        |
| `upload_checking_document_basic_stats`    | Stores basic statistics collected from checking documents.                                       |
| `upload_checking_document_enhanced_text`  | Stores parsed, no-punctuation, lower-cased, sentence-and-paragraph-start-and-end-marked.         |
| `upload_checking_document_text_vector`    | Stores the vector generated from text using SentenceBERT.                                        |
| `upload_checking_document_report`         | Stores the report generated while processing document for plagiarized content.                   |
| `university_logout`                       | Stores university's logout session information.                                                  |
| `instructor_logout`                       | Stores instructor's logout session information.                                                  |
| `university_delete_account`               | Stores university's delete account information.                                                  |
| `instructor_delete_account`               | Stores instructor's delete account information.                                                  |
|----------------------------------------------------------------------------------------------------------------------------------------------|

---

## Detailed Table Structures

### `admin`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `university`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `instructor`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |
| `first_name`    | VARCHAR()    | NOT NULL                  | Instructor's first name              |
| `last_name`     | VARCHAR()    | NOT NULL                  | Instructor's last name               |
| `password`      | VARCHAR()    | NOT NULL                  | Account's password                   |
| `email`         | VARCHAR(255) | UNIQUE, NOT NULL          | Login email                          |
| `university_id` | UUID         | FK to university(id)      | ID of university instructor works at |
| `created_at`    | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP | Timestamp of registration            |

---

### `university_approval`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `university_login`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `instructor`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `instructor_approval`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `instructor_login`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `research_repository_upload`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `research_document`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `research_repository_upload_error`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `research_repository_parse_text`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `research_document_references`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `research_document_parse_error`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `research_document_section_tokens`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `research_document_basic_stats`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `research_document_enhanced_text`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `research_document_text_vector`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `upload_checking_document_upload`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `upload_checking_document`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `upload_checking_document_upload_error`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `upload_checking_document_parse_text`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `upload_checking_document_references`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `upload_checking_document_parse_error`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `upload_checking_document_section_tokens`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `upload_checking_document_basic_stats`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `upload_checking_document_enhanced_text`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `upload_checking_document_text_vector`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `upload_checking_document_report`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `university_logout`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `instructor_logout`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `university_delete_account`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

### `instructor_delete_account`

| Column          | Type         | Constraints               | Description                          |
|-----------------|--------------|---------------------------|--------------------------------------|
| `id`            | UUID         | PK                        | Unique identifier                    |

---

> Don’t forget: Normalize first, cry later.

<!-- END OF: schema.md -->
