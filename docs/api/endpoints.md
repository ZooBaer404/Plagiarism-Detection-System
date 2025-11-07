<!--
START OF: endpoints.md
Purpose: List all public API endpoints and their descriptions.
Update Frequency: When a new endpoint is added, modified, or deprecated.
Location: docs/api/endpoints.md
-->

# API Endpoints Reference

| Method | Route                                 | Description                                                        | Auth Required                |
| ------ | ------------------------------------- | ------------------------------------------------------------------ | ---------------------------- |
| GET    | `/`                                   | Index page for new comers                                          | No                           |
| GET    | `/`                                   | Index page for admin                                               | yes (admin)                  |
| GET    | `/`                                   | Index page for university                                          | yes (university)             |
| GET    | `/`                                   | Index page for instructor                                          | yes (instructor)             |
| GET    | `/register/`                          | General registration                                               | no                           |
| POST   | `/register/`                          | Registration for university or instructor                          | no                           |
| GET    | `/admin/university/`                  | List of all university registrations                               | yes (admin)                  |
| GET    | `/admin/university/<uni-id>/`         | Information about university and approving or denying registration | yes (admin)                  |
| POST   | `/admin/university/<uni-id>/`         | Approval or denying university approval by admin                   | yes (admin)                  |
| GET    | `/university/instructor/`             | List of all instructor regiratrations                              | yes (university)             |
| GET    | `/university/instructor/<inst-id>/`   | Approval or denying instructor approval by university              | yes (university)             |
| POST   | `/university/instructor/<inst-id>/`   | Information about instructor and approving or denying registration | yes (university)             |
| GET    | `/login/`                             | Login form                                                         | no                           |
| POST   | `/login/`                             | Logging into system                                                | no                           |
| GET    | `/upload/`                            | Get form for uploading repo for university                         | yes (university)             |
| GET    | `/upload/`                            | Get form for uploading document for checking                       | yes (instructor)             |
| POST   | `/upload/`                            | Upload repo from university                                        | yes (university)             |
| GET    | `/repo/`                              | List all repository for university                                 | yes (university, admin)      |
| GET    | `/repo/<repo-id>/`                    | Get information about repo-id                                      | yes (university, admin)      |
| GET    | `/repo/<repo-id>/<doc-id>/`           | Get information about doc-id                                       | yes (university, admin)      |
| GET    | `/upload/error/`                      | See upload errors                                                  | yes (university, instructor) |
| POST   | `/upload/`                            | Upload document for checking from instructor                       | yes (instructor)             |
| GET    | `/upload/<doc-id>/`                   | Waiting room while upload is processing                            | yes (instructor)             |
| GET    | `/check/<doc-id>/`                    | Result page after checked document                                 | yes (instructor)             |
| GET    | `/check/<doc-id>/`                    | Result page after checked document                                 | yes (instructor)             |
| POST   | `/check/<doc-id>/references/`         | Decision from instructor whether it was plagiarized                | yes (instructor)             |
| GET    | `/check/<doc-id>/references/<ref-id>` | Information about found reference                                  | yes (instructor)             |
| GET    | `/error/`                             | Universal page for errors context passed down by Django            | optional                     |

<!-- END OF: endpoints.md -->
