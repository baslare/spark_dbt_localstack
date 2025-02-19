{{ config(
    materialized="table",
    file_format="parquet",
    location_root="s3a://air-boltic-data-warehouse",
    table_properties={"parquet.compress" : "SNAPPY"}

) }}

SELECT
    o.order_id,
    o.customer_id,
    o.trip_id,
    t.origin_city,
    t.destination_city,
    o.price_in_eur,
    o.seat_no,
    o.order_status
FROM boltic.order_normal as o
LEFT JOIN boltic.trip_normal as t on o.trip_id = t.trip_id

