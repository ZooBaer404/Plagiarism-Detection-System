<!--
START OF: requirements-specification.md
Purpose: This document defines and categorizes all project requirements, both functional and non-functional.
It is based on the structured processes recommended in *Software Project Management* by Bob Hughes et al.
Update Frequency:Update after every stakeholder meeting, feature discussion, or planning phase.
Location: docs/requirements-specification.md
-->

# Software Requirement Specification

## 1. Introduction

### 1.1 Purpose

The purpose of this document is to outline the requirements for Plagiarism Detection System, which is designed provide instructors with the ability to check for plagiarized content in student's research papers.

### 1.2 Scope

Plagiarism Detection System will support checking for plagiarized content, uploading repository to check against, saving history, crawling websites to index, and generating report based on every check.

### 1.3 Definitions, Acronyms, Abbreviations

<!-- word: definition -->
Plagiarism: The process or practice of using another person's ideas or work and pretending that it is your own.
Repository: A collection of research papers.
Report: To write or provide an account or summation of for publication or broadcast.

### 1.4 References

* Please refer to `/docs/research/README.md`

### 1.5 Overview

This document provides a detailed description of the system's functionality, performance, constraints, and other factors affecting the system.

---

## 2. Overall Description

### 2.1 Product Perspective

The Plagiarism Detection System(PDS) is a standalone system that interacts with external systems such as PDF and docx parsers and machine learning libraries.

### 2.2 Product Functions

Function: description

* Admin User Creation: System's admin is prompted to create user. This user has full control over the system.
* Register University: University institutions can register into PDS. As a result, a data directory is created with university's ID as its name which will house all the university-related data.
* Register Approval from Admin: Website admins are notified and they can decide on whether to accpet of reject university's registration.
* Login as University Admin: University administrators can login to the PDS.
* Register as University Instructor: University instructors can register into PDS.
* Register Approval from University Admin: University administrator is notified and they can decide on whether to accept or reject instructor's registration.
* Login as University Instructor: University instructors can login to the PDS.
* Upload Research Repository: University administrators can upload research papers as the basis to check against.
* Reporting Erroneous Documents During Upload: The documents that haven't been uploaded due to some issues are reported to the university administrator.
* Storing Documents: University documents will be stored as-is in the original format for backup purposes and stored in the upload table alongside its hash. An ID is assigned and the document is renamed to the ID.
* Parsing Document: The documents will be parsed. As of now, .pdf and .docx format are supported. The text will be extracted.
* Storing Document in Database: The document is registered in the database and an ID is assigned to it. The title and hash is stored and authors are either registered (if not existent in the database) or referenced. Other information such as Source Title, Publication Date, Location, and publication infomation (like publication title, publisher or editor, version of edition, and number).
* Reporting Erroneous Documents: The documents that can not be parsed are reported to the university administrator.
* Section Tokenization: The document text will be tokenized into multiple sections. Section tokenization might not be reliable but we need to extract the references section (which for us is the most important section).
* Store Basic Statistics about Document: Basic information that can not be changed are stored. Number of references, number of sentences, number of characters, number of words, size of the document, images in the document.
* Store Document References: Every reference in the document is stored. The style of citation, the authors are registered(if non-existent in the database) or referenced, if the Document's file is non-existent, the system will only store the information with the file reference set to null.
* Mark Start/End of Each Sentence and Paragraph: There should be symbols used for start and end of each sentence and paragraph.
* Store Content: Document's content is stored for later reference. Every sentence is stored as-is. It is used for later referencing.
* Remove Punctuation Marks: Remove punctuation marks from each sentence.
* Transform to Lower-Case: Make every word is lower-case.
* Transform Each Sentence into a Vector: Using SentenceBERT, we can generate a vector from each sentence.
* Upload Document for Checking: Document is uploaded for checking.
* Preprocess Document for Checking: Document is parsed, split, tokenized.
* Checking for Plagiarized Content: The tokens are checked against existing documents. If a token is found in other documents, they are registered, according to threshold, if a document keeps the streak, then it might be plagiarized.
* Generating Report: If matches are found, they are shown alongside with what percentage they kept the streak. If none are found, the research is either in another language or totally original. 
* Storing in Repo: The document is stored in the repository if the uploader gives the permission.
* Logout University: University can log out of their account.
* Logout Instructor: University instructors can log out of their accounts.
* Delete University: Universities can delete their account along with the repository they uploaded.
* Delete Instructor: Universities can delete their instructors' accounts.

### 2.3 User Classes and Characteristics

User Classes and Characteristics: "The primary users are university institutions."

### 2.4 Operating Environment

The Plagiarism Detection system will work on the web browser.

### 2.5 Design and Implementation Constraints

* Use of open-source libraries for cost efficiency.

### 2.6 Assumptions and Dependencies

* Users have internet access.
* Users have basic understanding of what plagiarism means. The ultimate decision on whether a paper is plagiarized is dependent on them.

---

## 3. System Features

### 3.1 Functional Requirements

#### F#01: Register University

* Description: University institutions can register into PDS. As a result, a data directory is created with university's ID as its name which will house all the university-related data.
* Input: University Name, Location, Certification (as proof), and password.
* Output: The university is notified that they should login once the admin has accepted their request.

#### F#02: Register Approval from Admin

* Description: Website admins are notified and they can decide on whether to accpet of reject university's registration.
* Input: The admin accepts or rejects the university's registration offer.
* Output: The university can now log in.

#### F#03: Login as University Admin

* Description: University administrators can login to the PDS.
* Input: University's name and password.
* Output: University is now logged into PDS.

#### F#04: Register as University Instructor

* Description: University instructors can register into PDS.
* Input: Instructor's full name, id, faculty name, date joined, and password.
* Output: The instructor is notified that they should login once the admin has accepted their request.

#### F#05: Register Approval from University Admin

* Description: University administrator is notified and they can decide on whether to accept or reject instructor's registration.
* Input: The university admin accepts or rejects the university's registration offer.
* Output: The university can now log in.

#### F#06: Login as University Instructor

* Description: University instructors can login to the PDS.
* Input: Instructor's name, ID, and password.
* Output: The instructor is now logged into PDS.

#### F#07: Upload Research Repository

* Description: University administrators can upload research papers as the basis to check against.
* Input: PDF, Docx files.
* Output: The files are uploaded and stored in the university's data directory.

#### F#08: Reporting Erroneous Documents During Upload

* Description: The documents that haven't been uploaded due to some issues are reported to the university administrator.
* Input: If any errors during upload, they will be recorded and reported to the university admin.
* Output: The university admin is notified of the errors in a different page.

#### F#09: Storing Documents

* Description: University documents will be stored as-is in the original format for backup purposes and stored in the upload table alongside its hash. An ID is assigned and the document is renamed to the ID.
* Input: The uploaded file.
* Output: The file is stored and recorded.

#### F#10: Parsing Document

* Description: The documents will be parsed. As of now, .pdf and .docx format are supported. The text will be extracted.
* Input: The stored file.
* Output: The extracted text from the document.

#### F#11: Storing Document in Database

* Description: The document is registered in the database and an ID is assigned to it. The title and hash is stored and authors are either registered (if not existent in the database) or referenced. Other information such as Source Title, Publication Date, Location, and publication infomation (like publication title, publisher or editor, version of edition, and number).
* Input: The document's data, source title, publication date, location, and publication information.
* Output: Return true if no issues occur.

#### F#12: Reporting Erroneous Documents

* Description: The documents that can not be parsed are reported to the university administrator.
* Input: Document's errors.
* Output: Reporting to the university admin.

#### F#13: Section Tokenization

* Description: The document text will be tokenized into multiple sections. Section tokenization might not be reliable but we need to extract the references section (which for us is the most important section).
* Input: Document's extracted text.
* Output: A two dimensional array containing the title and text of each section.

#### F#14: Store Basic Statistics about Document

* Description: Basic information that can not be changed are stored. Number of references, number of sentences, number of characters, number of words, size of the document, images in the document.
* Input: Document's text. Number of references, number of sentences, number of characters, number of words, size of the document in bytes, number of characters.
* Output: Return true if there are no issues.

#### F#15: Store Document References

* Description: Every reference in the document is stored. The style of citation, the authors are registered(if non-existent in the database) or referenced, if the Document's file is non-existent, the system will only store the information with the file reference set to null.
* Input: A list of references in the document.
* Output: Return true if not errors occur.

#### F#16: Mark Start/End of Each Sentence and Paragraph

* Description: There should be symbols used for start and end of each sentence and paragraph.
* Input: Document's text.
* Output: Text with sentences and paragraphs' start and ending marked.

#### F#17: Split Document into Words

* Description: The document is split into words and stored according to their index in the database(for backup purposes and later processing).
* Input: Text with sentences and paragraphs' start and ending marked.
* Output: Array of words or tokens.

#### F#18: Store Content

* Description: Document's content is stored for later reference. Every sentence is stored as-is. It is used for later referencing.
* Input: Text with sentences and paragraphs' start and ending marked.
* Output: Return true if no errors occur.

#### F#19: Remove Punctuation Marks

* Description: Remove punctuation marks from each sentence.
* Input: Array of tokens.
* Output: Array of tokens with punctuation marks removed.

#### F#20: Transform to Lower-Case

* Description: Make every word is lower-case.
* Input: Array of tokens with punctuation marks removed.
* Output: Array of tokens with lower case text.

#### F#21: Transform Each Sentence into a Vector

* Description: Using SentenceBERT, we can generate a vector from each sentence.
* Input: Array of tokens with lower case text.
* Output: Array of four-word sequential tokens.

#### F#22: Upload Document for Checking

* Description: Document is uploaded for checking.
* Input: Document file (PDF or docx).
* Output: Redirect to the results page.

#### F#23: Preprocess Document for Checking

* Description: Document is parsed, split, tokenized.
* Input: The document file.
* Output: Array of four-word sequential tokens.

#### F#24: Checking for Plagiarized Content

* Description: The tokens are checked against existing documents. If a token is found in other documents, they are registered, according to threshold, if a document keeps the streak, then it might be plagiarized.
* Input: Array of four-word sequential tokens.
* Output: Results of the process. How much of it was plagiarized.

#### F#25: Generating Report

* Description: If matches are found, they are shown alongside with what percentage they kept the streak. If none are found, the research is either in another language or totally original. 
* Input: Results of the process.
* Output: Report showing every bit of the process. Which documents it was matched to and how much and which parts.

#### F#26: Storing in Repo

* Description: The document is stored in the repository if the uploader gives the permission.
* Input: Instructor's permission.
* Output: Notifying the instructor if there are any issues.

#### F#27: Logout University

* Description:  University can log out of their account.
* Input: University Logout request.
* Output: The university is logged out.

#### F#28: Logout Instructor

* Description: University instructors can log out of their accounts.
* Input: Instructor logout request.
* Output: The instructor is logged out.

#### F#29: Delete University

* Description: Universities can delete their account along with the repository they uploaded.
* Input: University delete request.
* Output: The university is warned and the account is deleted.

---

### 3.2 Non-functional Requirements

#### Performance

* The system should support more than 1000 documents in the repository.

#### Security

* User's data must be protected. It should not be accessible by everyone.

#### Usability

* The system should be intuitive and easy to use for all user classes.

#### Reliability

* The system should have 80% uptime.

#### Scalibility

* The system should be able to scale to 3000 documents.

---

## 4. External Interface Requirements

### 4.1 User Interfaces

* Web Interface: Responsive design for all devices.

### 4.2 Hardware Interfaces

* User Desktops: It will run on modern browsers and provide solid performance.

### 4.3 Software Interfaces

* PostgreSQL: Main database
* Java: Backend Language
* Spring Boot: Backend framework
* Javascript: Frontend Language
* React: Frontend framework

### 4.4 Communication Interfaces

* Protocols: HTTPS for secure communication.

---

## 5. Other Non-functional Requirements

### 5.1 Performance Requirements

* Response time for any action should be less than 5 seconds.

### 5.2 Safety Requirements

* Proper backups should be taken to prevent data loss.

### 5.3 Security Requirements

* User's data should not be shared with others.

### 5.4 Software Quality Attributes

* Maintainability: The codebase should be modular and well-documented.
* Portability: The system should be deployable on different OS platforms.

### 5.5 Business Rules

* The content provided must adhere to business standards.

---

## 6. Appendices

### 6.1 Glossary

* API: Application Programming Interface

### 6.2 Analysis Models

* Use Case Diagrams: Illustrating user interactions with the system.
* ER Diagrams: Database structure. Use Case Diagrams, ER Diagrams, Sequence Diagrams, UML Diagrams

---

## References

- [product-vision.md](product-vision.md)
- [design-decision.md](design-decision.md)
- [risk-management.md](risk-management.md)
- [manual-tests.md](../qa/manual-tests.md)

<!-- END OF: requirements-specification.md -->
