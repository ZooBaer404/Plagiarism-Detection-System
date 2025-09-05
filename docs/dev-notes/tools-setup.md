<!--
START OF: tools-setup.md
Purpose: Document development environment setup, tools configurations, and useful utilities.
Update Frequency: Update when environment or tools change.
Location: docs/dev-notes/tools-setup.md
-->

# Tools & Setup

---

## Tool/Setup [#1] - Database System

**Date:** <2025-08-24 Sun>
**Author:** Zubair A. Rooghwall

Description:
Database is used for storing all the data for efficient query and backup.

Setup Instructions:
- Install your database system of choice.
- Create a user or role.
- Create a database.
- Create `.env` file in `src/` directory.
- Fill in the following variables.
  ```env
    DATABASE_ENGINE=''
    DATABASE_NAME=''
    DATABASE_USER=''
    DATABASE_PWD=''
    DATABASE_HOST=''
    DATABASE_PORT=''
  ```
  Note: Here `DATABASE_ENGINE` is specific to Django.
- Run the following command:
    ```bash
    python manage.py migrate
    ```
- If anything went wrong, please ensure you have followed each step or contact us.


Tips: -

---

## Tool/Setup [#2] - Project Setup

**Date:** <2025-08-24 Sun>
**Author:** Zubair A. Rooghwall

Description:
How to run the project.

Setup Instructions:
- Go to the `src/` directory and 
- Create a virtual environment.
- Activate the vertual environment.
- Run the following command: `pip install -r requirements.txt`
- Run the following command: `python manage.py runserver` 
- If anything went wrong, please ensure you have followed each step or contact us.

Tips: -


---

## Notes

- Keep instructions reproducible.
- Link to official docs or scripts.

<!-- END OF: tools-setup.md -->
