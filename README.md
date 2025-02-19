## Air Boltic Data Modelling

### Explanation

Hey! This repository demonstrates an ELT example for air boltic!.

I've chosen the tools to reflect the functionality defined in the task:

- **S3 for data storage**
  - Localstack container with s3 enabled, very basic hive partitioning.
- **Databricks for compute and data exploration**:
  - Pyspark to extract/clean data and save normalized tables to an s3 bucket.
- **dbt for data transformations**:
  - dbt + spark thrift server to create a toy data warehouse example.
  - data stored in s3 as parquet files.
- **Looker for reporting and self-service analytics**
  - duckdb python script to demonstrate a few queries, on the DWH.
- **GitHub to keep our scripts organised**:
  - well, this repo and GH Actions to demonstrate that the example works.

All of these are organized in a docker-compose.yml file. You can have a look at the runs in GitHub Actions. 
The commands (e.g. queries) have their output written, where applicable.

The modelling approach I had is something similar to a star schema in a data warehouse. While this is obviously a very simplified example, if scaled the main idea wouldn't change much:


