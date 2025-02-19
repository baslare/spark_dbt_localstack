## Air Boltic Data Modelling

### Explanation

Hey! This repository demonstrates an ETL example.

I've chosen the tools to reflect the functionality defined in the task:

- **S3 for data storage**
  - Localstack container with s3 enabled, very basic hive partitioning.
- **Databricks for compute and data exploration**:
  - Pyspark to extract/clean data and save normalized tables.
- **dbt for data transformations**:
  - dbt + spark thrift server to create a toy data warehouse example.
- **Looker for reporting and self-service analytics**
  - duckdb python script to demonstrate a few queries, on the DWH.
- **GitHub to keep our scripts organised**:
  - well, this repo and GH Actions to demonstrate that the example works.

