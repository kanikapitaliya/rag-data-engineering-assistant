# Customer Pipeline Failure Runbook

Step 1:
Check Airflow logs for pipeline failures.

Step 2:
Verify PostgreSQL source database connectivity.

Step 3:
Validate that required source tables are available.

Step 4:
Restart failed tasks.

Step 5:
If the issue persists, notify the on-call Data Engineer.

Escalation:
[data-engineering-oncall@company.com](mailto:data-engineering-oncall@company.com)
