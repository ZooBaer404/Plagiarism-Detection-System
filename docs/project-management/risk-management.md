<!--
START OF: risk-management.md
Purpose: This document outlines the risk identification, analysis, mitigation, and review processes across the project lifecycle. It is aligned with the methodology described in "Software Project Management" by Bob Hughes, Mike Cotterell, and Rajib Mall.
Update Frequency: Reviewed bi-weekly during sprint planning, milestone evaluations, or if any critical risk arises.
Location: docs/project-management/risk-management.md
-->

# Risk Management Strategy

Defines how project threats will be identified, analyzed, mitigated, and monitored.

---

## Risk Identification

> "If it has failed in someone else's project, it can fail in yours too. Learn, don't guess."

| Risk ID | Category  | Description    | Likelihood | Impact | Owner        |
|--------:|-----------|----------------|------------|--------|--------------|
| RSK-001 | Technical | Skill shortage | High       | High   | Backend Lead |

---

## Risk Analysis Matrix

| Likelihood → / Impact ↓ | Low      | Medium   | High             | Critical         |
|-------------------------|----------|----------|------------------|------------------|
| Low                     | Ignore   | Monitor  | Monitor          | Escalate         |
| Medium                  | Monitor  | Mitigate | Escalate         | Escalate         |
| High                    | Escalate | Escalate | Immediate Action | Immediate Action |

---

## Mitigation Strategies

| Risk ID | Mitigation Plan             | Status      |
|--------:|-----------------------------|-------------|
| RSK-001 | Set aside time for training | In Progress |

---

## Historical Risk Reviews

| Date             | Reviewed By     | New Risks Found | Major Updates Made        |
|------------------|-----------------|-----------------|---------------------------|
| <2025-08-10 Sun> | Project Manager | Skill shortage  | Initial structure created |

---

## Responsibilities

- **Backend Team**: Overall engine, risk documentation, tracking, escalation.
- **QA Lead**: Report recurring defects as project risks.
- **Frontend Team**: Create UI for project.

---

## Key Risk Indicators (KRIs)

| Indicator Name | Description                                         | Threshold | Tool |
|----------------|-----------------------------------------------------|-----------|------|
| Skill Shortage | Shortage of critial skills for building the project | 4 monts   |      |

---

## Risk Review Process

> “Plan for risk. If it doesn’t show up — great. If it does — you’re not screwed.”

| Step                 | Description                                                 |
|----------------------|-------------------------------------------------------------|
| 1. Identification    | Risks logged in `risk-register.md` by any contributor       |
| 2. Classification    | Categorized by likelihood and impact                        |
| 3. Response Planning | Mitigation, contingency, and communication steps drafted    |
| 4. Monitoring        | KPIs and KRIs tracked (see above)                           |
| 5. Escalation        | Triggered based on matrix or owner recommendation           |
| 6. Retrospective     | Add to [lessons-learned.md](lessons-learned.md) if critical |

---

## References

- [monitoring-control.md](monitoring-control.md)
- [roles-and-assignees.md](roles-and-assignees.md)
- [closure.md](closure.md)
- [risk-register.md](risk-register.md)

<!-- END OF risk-management.md -->
