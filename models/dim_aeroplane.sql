{{ config(
    materialized="table",
    file_format="parquet",
    location_root="s3a://air-boltic-data-warehouse",
    table_properties={"parquet.compress" : "SNAPPY"}

) }}

SELECT
    an.aeroplane_id,
    an.aeroplane_manufacturer,
    an.aeroplane_model,
    an.engine_type,
    an.max_distance,
    an.max_seats,
    an.max_weight,
    CASE WHEN an.max_distance > 4000 THEN 'long_haul' ELSE 'short_haul' END as distance_type,
    CASE WHEN an.max_seats > 100 THEN 'big' ELSE 'small' END as aeroplane_size

FROM boltic.aeroplane_normal as an
