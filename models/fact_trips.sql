{{ config(
    materialized="table",
    file_format="parquet",
    location_root="s3a://air-boltic-data-warehouse",
    table_properties={"parquet.compress" : "SNAPPY"}

) }}

SELECT
    t.trip_id,
    t.origin_city,
    t.destination_city,
    t.aeroplane_id,
    t.trip_start_timestamp,
    t.trip_end_timestamp,
    an.aeroplane_model,
    an.max_seats

FROM boltic.trip_normal as t
LEFT JOIN boltic.aeroplane_normal as an ON t.aeroplane_id = an.aeroplane_id