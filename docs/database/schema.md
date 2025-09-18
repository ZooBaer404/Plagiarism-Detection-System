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

| Table Name                         | Purpose                                                                                  |
|------------------------------------|------------------------------------------------------------------------------------------|
| `admin`                            | Stores essential infomation about the 'superuser' of the system.                         |
| `university`                       | Stores information about registering university.                                         |
| `university_approval`              | Stores whether university's registration is approved by admin or not.                    |
| `university_login`                 | Stores university's login session.                                                       |
| `instructor`                       | Stores information about instructor registering for university.                          |
| `instructor_approval`              | Stores whether instructor's registration is approved by university or not.               |
| `instructor_login`                 | Stores instructor's login session.                                                       |
| `university_logout`                | Stores university's logout session information.                                          |
| `instructor_logout`                | Stores instructor's logout session information.                                          |
| `research_repository`              | Stores basic information about the research repository.                                  |
| `research_document_upload`         | Stores the documents uploaded as repository.                                             |
| `research_document`                | Stores basic information about the uploaded document.                                    |
| `research_document_upload_error`   | Stores any errors that occur while uploading research document.                          |
| `research_document_parse_text`     | Stores the parsed content from the research document.                                    |
| `research_document_references`     | Stores the references contained in the research document.                                |
| `research_document_parse_error`    | Stores any errors that occurred while parsing the research document.                     |
| `research_document_section_tokens` | Stores tokenized sections from parsed research documents.                                |
| `research_document_basic_stats`    | Stores basic statistics collected from research documents.                               |
| `research_document_images`         | Stores images extracted from research documents.                                         |
| `research_document_enhanced_text`  | Stores parsed, no-punctuation, lower-cased, sentence-and-paragraph-start-and-end-marked. |
| `research_document_text_vector`    | Stores the vector generated from text using SentenceBERT.                                |
| `checking_document_upload`         | Stores the documents uploaded as repository.                                             |
| `checking_document`                | Stores the data related to documents upload for checking.                                |
| `checking_document_upload_error`   | Stores any errors that occur while uploading checking document.                          |
| `checking_document_parse_text`     | Stores the parsed content from the research document.                                    |
| `checking_document_references`     | Stores the references contained in the research document.                                |
| `checking_document_parse_error`    | Stores any errors that occurred while parsing the checking document.                     |
| `checking_document_section_tokens` | Stores tokenized sections from parsed checking documents.                                |
| `checking_document_basic_stats`    | Stores basic statistics collected from checking documents.                               |
| `checking_document_enhanced_text`  | Stores parsed, no-punctuation, lower-cased, sentence-and-paragraph-start-and-end-marked. |
| `checking_document_text_vector`    | Stores the vector generated from text using SentenceBERT.                                |
| `checking_document_check_process`  | Stores the plagiarized content found in other research documents.                        |
| `checking_document_report`         | Stores the report generated while processing document for plagiarized content.           |

---

## Detailed Table Structures

### `admin`

| Column             | Type         | Constraints               | Description                               |
|--------------------|--------------|---------------------------|-------------------------------------------|
| `id`               | INTEGER      | PK                        | Unique identifier                         |
| `username`         | VARCHAR(255) | NOT NULL                  | User name of the admin                    |
| `password`         | VARCHAR(255) | NOT NULL                  | Admin's password                          |
| `created_at`       | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP | When the account was created              |
| `last_modified_at` | TIMESTAMP    |                           | When was the last time the table modified |

---

### `university`

| Column                   | Type         | Constraints               | Description                               |
|--------------------------|--------------|---------------------------|-------------------------------------------|
| `id`                     | INTEGER      | PK                        | Unique identifier                         |
| `university_name`        | VARCHAR(255) | NOT NULL                  | University's name                         |
| `password`               | VARCHAR(255) | NOT NULL                  | University account's password             |
| `university_certificate` | VARCHAR()    | NOT NULL                  | University's certificate for verification |
| `created_at`             | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP | When university's account was created     |
| `last_modified_at`       | TIMESTAMP    |                           | When was the last time the table modified |

---

### `university_approval`

| Column             | Type          | Constraints              | Description                               |
|--------------------|---------------|--------------------------|-------------------------------------------|
| `id`               | INTEGER       | PK                       | Unique identifier                         |
| `admin_id`         | INTEGER       | FK to admin(id)          | ID of admin who approved this university  |
| `is_approved`      | BOOLEAN       | DEFAULT FALSE            | Is university approved by the admin       |
| `message`          | VARCHAR(1000) | NOT NULL                 | Admin's message after review              |
| `created_at`       | TIMSTAMP      | DEFAULT CURRENT_TIMSTAMP | Timestamp of university approval          |
| `last_modified_at` | TIMESTAMP     |                          | When was the last time the table modified |

---

### `university_login`

| Column             | Type        | Constraints               | Description                               |
|--------------------|-------------|---------------------------|-------------------------------------------|
| `id`               | INTEGER     | PK                        | Unique identifier                         |
| `ip_address`       | VARCHAR(16) |                           | University's computer's IP address        |
| `created_at`       | TIMSTAMP    | DEFAULT CURRENT_TIMESTAMP | When the university logged in             |
| `last_modified_at` | TIMESTAMP   |                           | When was the last time the table modified |

---

### `instructor`

| Column             | Type          | Constraints               | Description                               |
|--------------------|---------------|---------------------------|-------------------------------------------|
| `id`               | INTEGER       | PK                        | Unique identifier                         |
| `first_name`       | VARCHAR(255)  | NOT NULL                  | Instructor's first name                   |
| `last_name`        | VARCHAR(255)  | NOT NULL                  | Instructor's last name                    |
| `password`         | VARCHAR(255)  | NOT NULL                  | Account's password                        |
| `email`            | VARCHAR(320)  | UNIQUE, NOT NULL          | Login email                               |
| `university_id`    | INTEGER       | FK to university(id)      | ID of university instructor works at      |
| `certificate`      | VARCHAR(1000) | NOT NULL                  | Instructor's certificate path             |
| `field`            | VARCHAR(100)  | NOT NULL                  | Instructor's field of study               |
| `created_at`       | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP | Timestamp of registration                 |
| `last_modified_at` | TIMESTAMP     |                           | When was the last time the table modified |

---

### `instructor_approval`

| Column             | Type          | Constraints              | Description                                   |
|--------------------|---------------|--------------------------|-----------------------------------------------|
| `id`               | INTEGER       | PK                       | Unique identifier                             |
| `university_id`    | INTEGER       | FK to university(id)     | ID of university who approved this instructor |
| `is_approved`      | BOOLEAN       | DEFAULT FALSE            | Is instructor approved by the university      |
| `message`          | VARCHAR(1000) | NOT NULL                 | university's message after review             |
| `created_at`       | TIMSTAMP      | DEFAULT CURRENT_TIMSTAMP | Timestamp of instructor approval              |
| `last_modified_at` | TIMESTAMP     |                          | When was the last time the table modified     |

---

### `instructor_login`

| Column             | Type        | Constraints               | Description                               |
|--------------------|-------------|---------------------------|-------------------------------------------|
| `id`               | INTEGER     | PK                        | Unique identifier                         |
| `ip_address`       | VARCHAR(16) |                           | Instructor's computer's IP address        |
| `created_at`       | TIMSTAMP    | DEFAULT CURRENT_TIMESTAMP | When the instructor logged in             |
| `last_modified_at` | TIMESTAMP   |                           | When was the last time the table modified |

---


### `university_logout`

| Column             | Type      | Constraints               | Description                               |
|--------------------|-----------|---------------------------|-------------------------------------------|
| `id`               | INTEGER   | PK                        | Unique identifier                         |
| `university_id`    | INTEGER   | FK to university(id)      | University's ID                           |
| `created_at`       | TIMSTAMP  | DEFAULT CURRENT_TIMESTAMP | When the university logged out            |
| `last_modified_at` | TIMESTAMP |                           | When was the last time the table modified |

---

### `instructor_logout`

| Column             | Type      | Constraints               | Description                               |
|--------------------|-----------|---------------------------|-------------------------------------------|
| `id`               | INTEGER   | PK                        | Unique identifier                         |
| `instructor_id`    | INTEGER   | FK to instructor(id)      | Instructor's ID                           |
| `created_at`       | TIMSTAMP  | DEFAULT CURRENT_TIMESTAMP | When the instructor logged out            |
| `last_modified_at` | TIMESTAMP |                           | When was the last time the table modified |

---

### `research_repository`

| Column             | Type         | Constraints               | Description                               |
|--------------------|--------------|---------------------------|-------------------------------------------|
| `id`               | INTEGER      | PK                        | Unique identifier                         |
| `repo_name`        | VARCHAR(255) | NOT NULL                  | Respository's name after upload           |
| `university_id`    | INTEGER      | FK to university(id)      | ID of the uploader university             |
| `created_at`       | TIMSTAMP     | DEFAULT CURRENT_TIMESTAMP | When the repository was uploaded          |
| `last_modified_at` | TIMESTAMP    |                           | When was the last time the table modified |

---

### `research_document_upload`

| Column                   | Type          | Constraints                   | Description                                          |
|--------------------------|---------------|-------------------------------|------------------------------------------------------|
| `id`                     | INTEGER       | PK                            | Unique identifier                                    |
| `research_repository_id` | INTEGER       | FK to research_repository(id) | Respository's ID which the uploaded too place to.    |
| `research_document_name` | VARCHAR(255)  | NOT NULL                      | Document's name which was uploaded to the repository |
| `research_document_path` | VARCHAR(1000) | NOT NULL                      | Document's location for access by the preprocessor   |
| `is_upload_complete`     | BOOLEAN       | DEFAULT FALSE                 | Whether the uploaded is completed or not             |
| `created_at`             | TIMSTAMP      | DEFAULT CURRENT_TIMESTAMP     | When the repository was uploaded                     |
| `last_modified_at`       | TIMESTAMP     |                               | When was the last time the table modified            |

---

### `research_document`

| Column                        | Type          | Constraints                        | Description                                               |
|-------------------------------|---------------|------------------------------------|-----------------------------------------------------------|
| `id`                          | INTEGER       | PK                                 | Unique identifier                                         |
| `research_document_name`      | VARCHAR(500)  |                                    | Document's name after upload                              |
| `research_document_path`      | VARCHAR(1000) | NOT NULLL                          | The path of the research document                         |
| `university_id`               | INTEGER       | FK to university(id)               | University's ID whom uploaded the document                |
| `research_repository_id`      | INTEGER       | FK to research_repository(id)      | Research repository to which the document was uploaded to |
| `research_document_upload_id` | INTEGER       | FK to research_document_upload(id) | Research document which was uploaded to the repository    |
| `created_at`                  | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP          | When the document was proprocessed                        |
| `last_modified_at`            | TIMESTAMP     |                                    | When was the last time the table modified                 |

---

### `research_document_upload_error`

| Column                        | Type      | Constraints                        | Description                                    |
| ----------------------------- | --------- | ---------------------------------- | ---------------------------------------------- |
| `id`                          | INTEGER      | PK                                 | Unique identifier                              |
| `research_document_upload_id` | INTEGER      | FK to research_document_upload(id) | ID of the uploaded document to the repository  |
| `error_message`               | VARCHAR(1000) | NOT NULL                           | Stating what happened while uploading the file |
| `created_at`                  | TIMSTAMP  | DEFAULT CURRENT_TIMSTAMP           | When the error was recorded                    |
| `last_modified_at` | TIMESTAMP |  | When was the last time the table modified |

---

### `research_repository_parse_text`

| Column                 | Type           | Constraints                 | Description                               |
|------------------------|----------------|-----------------------------|-------------------------------------------|
| `id`                   | INTEGER        | PK                          | Unique identifier                         |
| `research_document_id` | INTEGER        | FK to research_document(id) | ID of the research document               |
| `parse_text`           | VARCHAR(50000) |                             | Content of the parsed text                |
| `created_at`           | TIMSTAMP       | DEFAULT CURRENT_TIMESTAMP   | When the parsed text was recorded         |
| `last_modified_at`     | TIMESTAMP      |                             | When was the last time the table modified |

---

### `research_document_references`

| Column                 | Type          | Constraints                 | Description                                  |
|------------------------|---------------|-----------------------------|----------------------------------------------|
| `id`                   | INTEGER       | PK                          | Unique identifier                            |
| `research_document_id` | INTEGER       | FK to research_document(id) | ID of the research document                  |
| `index`                | INTEGER       | DEFAULT -1                  | In which index the reference was encountered |
| `reference_text`       | VARCHAR(2000) |                             | Text of the reference encountered            |
| `created_at`           | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP   | When the reference was recorded              |
| `last_modified_at`     | TIMESTAMP     |                             | When was the last time the table modified    |

---

### `research_document_parse_error`

| Column                 | Type           | Constraints                 | Description                                     |
|------------------------|----------------|-----------------------------|-------------------------------------------------|
| `id`                   | INTEGER        | PK                          | Unique identifier                               |
| `research_document_id` | INTEGER        | FK to research_document(id) | The ID of the research document                 |
| `parse_text`           | VARCHAR(50000) | NOT NULL                    | The parsed text                                 |
| `error_message`        | VARHCHAR(1000) | NOT NULL                    | Stating the error that occurred while uploading |
| `created_at`           | TIMESTAMP      | DEFAULT CURRENT_TIMESTAMP   | When the error was recorded                     |
| `last_modified_at`     | TIMESTAMP      |                             | When was the last time the table modified       |

---

### `research_document_section_tokens`

| Column                 | Type          | Constraints                   | Description                               |
|------------------------|---------------|-------------------------------|-------------------------------------------|
| `id`                   | INTEGER       | PK                            | Unique identifier                         |
| `research_document_id` | INTEGER       | FK to research_repository(id) | The ID of the research document           |
| `section_index`        | INT           | NOT NULL                      | In which order it was encountered         |
| `section_title`        | VARCHAR(1000) | NOT NULL                      | Section title encountered                 |
| `section_description`  | VARCHAR(5000) | NOT NULL                      | Text of the section                       |
| `created_at`           | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP     | When section tokens were recorded         |
| `last_modified_at`     | TIMESTAMP     |                               | When was the last time the table modified |

---

### `research_document_basic_stats`

| Column                 | Type      | Constraints                 | Description                                       |
|------------------------|-----------|-----------------------------|---------------------------------------------------|
| `id`                   | INTEGER   | PK                          | Unique identifier                                 |
| `research_document_id` | INTEGER   | FK to research_document(id) | The ID of the research document                   |
| `no_of_references`     | INT       |                             | The number of references found in the document    |
| `no_of_sentences`      | INT       |                             | The number of sentences detected in the document  |
| `no_of_characters`     | INT       |                             | The number of characters detected in the document |
| `no_of_words`          | INT       |                             | The number of words detected in the document      |
| `size_of_document`     | INT       |                             | The size of the document in bytes                 |
| `no_of_images`         | INT       | DEFAULT 0                   | The number of images detected in the document     |
| `created_at`           | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP   | When the basic statistics were saved              |
| `last_modified_at`     | TIMESTAMP |                             | When was the last time the table modified         |

---

### `research_document_images`

| Column                 | Type          | Constraints                 | Description                               |
|------------------------|---------------|-----------------------------|-------------------------------------------|
| `id`                   | INTEGER       | PK                          | Unique identifier                         |
| `research_document_id` | INTEGER       | FK to research_document(id) | The ID of the research document           |
| `image_path`           | VARCHAR(1000) | NOT NULL                    | Relative path of the image stores         |
| `created_at`           | TIMESTAMP     | DEFAULT TIMESTAMP           | When the image were recorded              |
| `last_modified_at`     | TIMESTAMP     |                             | When was the last time the table modified |

---

### `research_document_enhanced_text`

| Column                   | Type           | Constraints                 | Description                                  |
|--------------------------|----------------|-----------------------------|----------------------------------------------|
| `id`                     | INTEGER        | PK                          | Unique identifier                            |
| `research_document_id`   | INTEGER        | FK to research_document(id) | The ID of the research document              |
| `sentence_index`         | INT            | Index of the sentence       |                                              |
| `sentence_enhanced_text` | VARCHAR(50000) | NOT NULL                    | The enhanced text                            |
| `created_at`             | TIMESTAMP      | DEFAULT CURRENT_TIMESTAMP   | When the enhanced sentence text was recorded |
| `last_modified_at`       | TIMESTAMP      |                             | When was the last time the table modified    |

---

### `research_document_text_vector`

| Column                               | Type      | Constraints                               | Description                                                         |
|--------------------------------------|-----------|-------------------------------------------|---------------------------------------------------------------------|
| `id`                                 | INTEGER   | PK                                        | Unique identifier                                                   |
| `research_document_id`               | INTEGER   | FK to research_document(id)               | The ID of the research document                                     |
| `research_document_enhanced_text_id` | INTEGER   | FK to research_document_enhanced_text(id) | The ID of the sentence stored in the database                       |
| `text_vector`                        | INTEGER[] | NOT NULL                                  | The extracted text vector of each sentence in the research document |
| `created_at`                         | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP                 | When the sentence text vector was recorded.                         |
| `last_modified_at`                   | TIMESTAMP |                                           | When was the last time the table modified                           |

---

### `checking_document_upload`

| Column                   | Type          | Constraints               | Description                                          |
|--------------------------|---------------|---------------------------|------------------------------------------------------|
| `id`                     | INTEGER       | PK                        | Unique identifier                                    |
| `checking_document_name` | VARCHAR(500)  | NOT NULL                  | Document's name which was uploaded to the repository |
| `checking_document_path` | VARCHAR(1000) | NOT NULL                  | Document's location for access by the preprocessor   |
| `is_upload_complete`     | BOOLEAN       | DEFAULT FALSE             | Whether the uploaded is completed or not             |
| `created_at`             | TIMSTAMP      | DEFAULT CURRENT_TIMESTAMP | When the repository was uploaded                     |
| `last_modified_at`       | TIMESTAMP     |                           | When was the last time the table modified            |

---

### `checking_document`

| Column                        | Type          | Constraints                        | Description                                                 |
|-------------------------------|---------------|------------------------------------|-------------------------------------------------------------|
| `id`                          | INTEGER       | PK                                 | Unique identifier                                           |
| `checking_document_name`      | VARCHAR(500)  |                                    | Document's name after upload                                |
| `checking_document_path`      | VARCHAR(1000) | NOT NULL                           | The path of the checking document                           |
| `instructor_id`               | INTEGER       | FK to instructor(id)               | Instructor's ID whom uploaded the document                  |
| `checking_document_upload_id` | INTEGER       | FK to checking_document_upload(id) | Checking document's ID which was uploaded to the repository |
| `created_at`                  | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP          | When the document was proprocessed                          |
| `last_modified_at`            | TIMESTAMP     |                                    | When was the last time the table modified                   |

---

### `checking_document_upload_error`

| Column                        | Type          | Constraints                        | Description                                        |
|-------------------------------|---------------|------------------------------------|----------------------------------------------------|
| `id`                          | INTEGER       | PK                                 | Unique identifier                                  |
| `checking_document_upload_id` | INTEGER       | FK to checking_document_upload(id) | ID of the uploaded document for checking           |
| `error_message`               | VARCHAR(1000) | NOT NULL                           | Stating what happened while uploading the document |
| `created_at`                  | TIMSTAMP      | DEFAULT CURRENT_TIMSTAMP           | When the error was recorded                        |
| `last_modified_at`            | TIMESTAMP     |                                    | When was the last time the table modified          |

---

### `checking_document_parse_text`

| Column                 | Type           | Constraints                 | Description                               |
|------------------------|----------------|-----------------------------|-------------------------------------------|
| `id`                   | INTEGER        | PK                          | Unique identifier                         |
| `checking_document_id` | INTEGER        | FK to checking_document(id) | ID of the checking document               |
| `parse_text`           | VARCHAR(50000) | NOT NULL                            | Content of the parsed text                |
| `created_at`           | TIMSTAMP       | DEFAULT CURRENT_TIMESTAMP   | When the parsed text was recorded         |
| `last_modified_at`     | TIMESTAMP      |                             | When was the last time the table modified |

---

### `checking_document_references`

| Column                 | Type          | Constraints                 | Description                                  |
|------------------------|---------------|-----------------------------|----------------------------------------------|
| `id`                   | INTEGER       | PK                          | Unique identifier                            |
| `checking_document_id` | INTEGER       | FK to checking_document(id) | ID of the checking document                  |
| `index`                | int           | DEFAULT -1                  | In which index the reference was encountered |
| `reference_text`       | VARCHAR(1000) | NOT NULL                    | Text of the reference encountered            |
| `created_at`           | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP   | When the reference was recorded              |
| `last_modified_at`     | TIMESTAMP     |                             | When was the last time the table modified    |

---

### `checking_document_parse_error`

| Column                 | Type           | Constraints                 | Description                               |
|------------------------|----------------|-----------------------------|-------------------------------------------|
| `id`                   | INTEGER        | PK                          | Unique identifier                         |
| `checking_document_id` | INTEGER        | FK to checking_document(id) | ID of the checking document               |
| `parse_text`           | VARCHAR(50000) |  NOT NULL                           | Content of the parsed text                |
| `error_message`        | VARCHAR(1000)  | NOT NULL                    | The error message                         |
| `created_at`           | TIMSTAMP       | DEFAULT CURRENT_TIMESTAMP   | When the parsed text was recorded         |
| `last_modified_at`     | TIMESTAMP      |                             | When was the last time the table modified |

---

### `checking_document_section_tokens`

| Column                 | Type          | Constraints                   | Description                               |
|------------------------|---------------|-------------------------------|-------------------------------------------|
| `id`                   | INTEGER       | PK                            | Unique identifier                         |
| `checking_document_id` | INTEGER       | FK to checking_repository(id) | The ID of the checking document           |
| `section_index`        | INT           | NOT NULL                      | In which order it was encountered         |
| `section_title`        | VARCHAR(1000) | NOT NULL                      | Section title encountered                 |
| `section_description`  | VARCHAR(5000) | NOT NULL                      | Text of the section                       |
| `created_at`           | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP     | When section tokens were recorded         |
| `last_modified_at`     | TIMESTAMP     |                               | When was the last time the table modified |

---

### `checking_document_basic_stats`

| Column                 | Type      | Constraints                 | Description                                       |
|------------------------|-----------|-----------------------------|---------------------------------------------------|
| `id`                   | INTEGER   | PK                          | Unique identifier                                 |
| `checking_document_id` | INTEGER   | FK to checking_document(id) | The ID of the checking document                   |
| `no_of_references`     | INT       |                             | The number of references found in the document    |
| `no_of_sentences`      | INT       |                             | The number of sentences detected in the document  |
| `no_of_characters`     | INT       |                             | The number of characters detected in the document |
| `no_of_words`          | INT       |                             | The number of words detected in the document      |
| `size_of_document`     | INT       |                             | The size of the document in bytes                 |
| `no_of_images`         | INT       | DEFAULT 0                   | The number of images detected in the document     |
| `created_at`           | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP   | When the basic statistics were saved              |
| `last_modified_at`     | TIMESTAMP |                             | When was the last time the table modified         |

---

### `checking_document_enhanced_text`

| Column                   | Type          | Constraints                 | Description                                  |
|--------------------------|---------------|-----------------------------|----------------------------------------------|
| `id`                     | INTEGER       | PK                          | Unique identifier                            |
| `checking_document_id`   | INTEGER       | FK to checking_document(id) | The ID of the checking document              |
| `sentence_index`         | INT           | Index of the sentence       |                                              |
| `sentence_enhanced_text` | VARCHAR(1000) | NOT NULL                    | The enhanced text                            |
| `created_at`             | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP   | When the enhanced sentence text was recorded |
| `last_modified_at`       | TIMESTAMP     |                             | When was the last time the table modified    |

---

### `checking_document_text_vector`

| Column                               | Type      | Constraints                               | Description                                                         |
|--------------------------------------|-----------|-------------------------------------------|---------------------------------------------------------------------|
| `id`                                 | INTEGER   | PK                                        | Unique identifier                                                   |
| `checking_document_id`               | INTEGER   | FK to checking_document(id)               | The ID of the checking document                                     |
| `checking_document_enhanced_text_id` | INTEGER   | FK to checking_document_enhanced_text(id) | The ID of the sentence stored in the database                       |
| `text_vector`                        | INTEGER[] | NOT NULL                                  | The extracted text vector of each sentence in the checking document |
| `created_at`                         | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP                 | When the sentence text vector was recorded.                         |
| `last_modified_at`                   | TIMESTAMP |                                           | When was the last time the table modified                           |

---

### `checking_document_check_process`

| Column                             | Type      | Constraints                             | Description                                                                 |
|------------------------------------|-----------|-----------------------------------------|-----------------------------------------------------------------------------|
| `id`                               | INTEGER   | PK                                      | Unique identifier                                                           |
| `checking_document_id`             | INTEGER   | FK to checking_document(id)             | The ID of the checking document                                             |
| `checking_document_text_vector_id` | INTEGER   | FK to checking_document_text_vector(id) | The ID of the text vector in the checking document                          |
| `research_document_text_vector_id` | INTEGER   | FK to research_document_text_vector(id) | The ID of the text vector that is similar to the checking document's vector |
| `similarity`                       | DECIMAL   | NOT NULL                                | What percent are the vectors similar                                        |
| `created_at`                       | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP               | When the similarity was recorded.                                           |
| `last_modified_at`                 | TIMESTAMP |                                         | When was the last time the table modified                                   |

---

### `checking_document_report`

| Column                 | Type      | Constraints                 | Description                                           |
|------------------------|-----------|-----------------------------|-------------------------------------------------------|
| `id`                   | INTEGER   | PK                          | Unique identifier                                     |
| `checking_document_id` | INTEGER   | FK to checking_document(id) | The ID of the checking document                       |
| `report_result`        | DECIMAL   | NOT NULL                    | The result of the report. What percentage plagiarized |
| `created_at`           | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP   | When the report was recorded                          |
| `last_modified_at`     | TIMESTAMP |                             | When was the last time the table modified             |

---

> Don’t forget: Normalize first, cry later.

<!-- END OF: schema.md -->
