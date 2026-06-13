# Customer Pipeline

Pipeline Name: Customer Pipeline

Owner: Data Engineering Team

Source System: PostgreSQL CRM Database

Destination: customer_master table in Snowflake

Frequency: Every 6 hours

Purpose:
The pipeline ingests customer records from the CRM system and prepares them for analytics and reporting.

Transformations:

* Remove duplicate customers
* Standardize email formats
* Validate phone numbers
* Generate customer segmentation attributes

Expected Runtime:
15 minutes

SLO:
Pipeline must complete successfully within 30 minutes.

Monitoring:
Prometheus dashboards monitor pipeline execution and failures.
