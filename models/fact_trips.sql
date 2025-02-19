{{ config(
    materialized="table",
    file_format="parquet",
    location_root="s3a://air-boltic-data-warehouse/fact_trips",
    table_properties={"parquet.compress" : "SNAPPY"},
    spark_conf={
        "spark.sql.sources.outputFileExtension": ".parquet"
    },
    hive_custom_properties={
        "stored.as": "PARQUET",
        "input.format": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
        "output.format": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
        "serde.lib": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe"
    }

) }}

SELECT
    t.trip_id,
    t.origin_city,
    t.destination_city,
    t.airplane_id,
    t.trip_start_timestamp,
    t.trip_end_timestamp
FROM boltic.trip_normal as t