{{ config(
    materialized="table",
    file_format="parquet",
    location_root="s3a://air-boltic-data-warehouse",
    table_properties={"parquet.compress" : "SNAPPY"}

) }}

SELECT
    ct.customer_id,
    ct.customer_name,
    ct.customer_group_id,
    ct.customer_email,
    ct.customer_phone_number,
    cg.customer_group_type,
    cg.customer_group_name,
    cg.registry_number,
    CASE WHEN ct.customer_group_id IS NULL THEN false ELSE true END as customer_has_group,
    CASE WHEN ct.customer_email IS NULL THEN false ELSE true END as customer_has_email,
    CASE WHEN ct.customer_phone_number = '' THEN false ELSE true END as customer_has_phone_number
FROM boltic.customer_normal as ct
LEFT JOIN boltic.customer_group_normal as cg on ct.customer_group_id = cg.customer_group_id