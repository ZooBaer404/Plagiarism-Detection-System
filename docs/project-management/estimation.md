<!--
START OF: estimation.md
Purpose: This document provides a detailed outline of estimation techniques used for cost, effort, and time in the project.
Based on principles from Software Project Management by Bob Hughes et al.
Update Frequency: Whenever a major estimation is performed or recalibrated during planning or re-planning phases.
Location: docs/project-management/estimation.md
-->


# Project Estimation

## Overview

This file describes how the team estimates effort, cost, and time for features and milestones.
It includes techniques used, assumptions made, and records of past estimations.

---

## Estimation Techniques

| Technique                | Description                                 | Use Case              |
|--------------------------|---------------------------------------------|-----------------------|
| Expert Judgment          | Based on team’s domain expertise            | Feature complexity    |
| Function Point Analysis  | Measures functionality from the user’s view | Business applications |
| Analogy-based Estimation | Compares with previous similar projects     | Reusable modules      |
| Delphi Method            | Consensus through multiple expert rounds    | High-risk components  |
| COCOMO II                | Cost model estimating person-months         | Large-scale planning  |

---

## Time Breakdown Table

Module-wise or task-wise breakdown (include diagrams or Gantt chart if needed).

| Task/Feature             | Estimated Time (hrs) | Allocated Time (hrs) | Start Date       | End Date         |
|--------------------------|----------------------|----------------------|------------------|------------------|
| Requirements Engineering | 50                   | 70                   | <2025-08-10 Sun> | <2025-08-16 Sat> |
| UI Prototype Design      | 20                   | 25                   | <2025-08-10 Sun> | <2025-08-16 Sat> |
| Authentication Flow      | 30                   | 35                   | <2025-09-07 Sun  | <2025-09-14 Sun> |
| Input Pipeline           | 100                  | 150                  | <2025-08-23 Sat> | <2025-09-07 Sun> |
| Building Core Engine     | 100                  | 150                  | <2025-09-14 Sun> | <2025-10-12 Sun> |
| Bug Fixing Sprint 1      | 20                   | 25                   | <2025-10-12 Sun> | <2025-11-3 Mon>  |
| Building UI              | 50                   | 60                   | <2025-09-07 Sun> | <2025-09-21 Sun> |
| Assuring Quality         | 50                   | 60                   | <2025-10-12 Sun> | <2025-11-02 Sun> |
| Closure                  | 100                  | 150                  | <2025-11-02 Sun> | <2025-11-30 Sun> |

---

## Effort Estimate

In person-hours or person-months. Mention the allocation of devs, testers, PMs.


| Feature/Module           | Estimated Effort (hrs) | Actual Effort (hrs) | Variance |
|--------------------------|------------------------|---------------------|----------|
| Requirements Engineering | 50                     |                     |          |
| UI Prototype Design      | 20                     |                     |          |
| Authentication Flow      | 30                     |                     |          |
| Input Pipeline           | 100                    |                     |          |
| Building Core Engine     | 100                    |                     |          |
| Bug Fixing Sprint 1      | 20                     |                     |          |
| Building UI              | 50                     |                     |          |
| Assuring Quality         | 50                     |                     |          |
| Closure                  | 100                    |                     |          |

---

## Notes

- Round all time to the nearest 5 hours for planning simplicity
- Use confidence intervals (best, worst, most likely) for risky components

---

## References

- [milestones.md](milestones.md)
- [design-decision.md](design-decision.md)
- [Project Management](README.md)

<!-- END OF: estimation.md -->
