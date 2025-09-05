<!--
START OF: data-analyzer.md
Purpose: Describes the tool that processes and analyzes log or telemetry data.
Update Frequency: Update when metrics or logic change significantly.
Location: docs/internal-tools/data-analyzer.md
-->

# Data Analyzer

## What It Does
This tool parses log files, extracts key metrics, and presents insights on system performance, error frequency, and usage patterns.

---

## Usage

```bash
python analyze.py --log logs/system.log
```
---

## Output

- Error frequency by module
- Latency distribution
- Request load vs time

Example:

```bash
[INFO] Average latency: 123ms
[ERROR] /auth/token - 401 errors: 42
```

---

## Configurable Parameters

| Flag              | Description                 | Default |
|-------------------|-----------------------------|---------|

---

## Dependencies

- Python 3.13+


---

## Developer Notes


<!-- END OF: data-analyzer.md -->
