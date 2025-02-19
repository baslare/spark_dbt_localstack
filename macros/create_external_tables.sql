{% macro create_trips_external_tables() %}
    {% set create_db %}
    CREATE DATABASE IF NOT EXISTS boltic;
    {%  endset %}


    {%  set create_table_trip_normal %}

    CREATE TABLE IF NOT EXISTS boltic.trip_normal(
            trip_id int,
            origin_city char(30),
            destination_city char(30),
            airplane_id int,
            trip_start_timestamp TIMESTAMP,
            trip_end_timestamp TIMESTAMP

    )
    USING PARQUET
    LOCATION 's3a://air-boltic-data-normalized/trip/';

    {% endset %}

    {%  set create_table_order_normal %}

    CREATE TABLE IF NOT EXISTS boltic.order_normal(
            order_id int,
            customer_id int,
            trip_id int,
            price_in_eur int,
            seat_no char(5),
            order_status char(30)

    )
    USING PARQUET
    LOCATION 's3a://air-boltic-data-normalized/order/';

    {% endset %}

    {%  set create_table_customer_group_normal %}

    CREATE TABLE IF NOT EXISTS boltic.customer_group_normal(
            customer_group_id int,
            customer_group_type char(50),
            customer_group_name char(50),
            customer_group_name char(50)

    )
    USING PARQUET
    LOCATION 's3a://air-boltic-data-normalized/customer_group/';

    {% endset %}

    {%  set create_table_customer_normal %}

    CREATE TABLE IF NOT EXISTS boltic.customer_normal(
            customer_id int,
            customer_name char(50),
            customer_group_id int,
            customer_email char(50),
            customer_phone_number char(50)

    )
    USING PARQUET
    LOCATION 's3a://air-boltic-data-normalized/customer/';

    {% endset %}

        {%  set create_table_aeroplane_normal %}

    CREATE TABLE IF NOT EXISTS boltic.aeroplane_normal(
            aeroplane_id int,
            aeroplane_manufacturer char(50),
            aeroplane_model char(50),
            engine_type char(50),
            max_distance int,
            max_seats int,
            max_weight int

    )
    USING PARQUET
    LOCATION 's3a://air-boltic-data-normalized/aeroplane/';

    {% endset %}

    {% do log("Creating external tables in Spark...", info=True) %}
    {% do run_query(create_db) %}
    {% do run_query(create_table_trip_normal) %}
    {% do run_query(create_table_order_normal) %}
    {% do run_query(create_table_customer_group_normal) %}
    {% do run_query(create_table_customer_normal) %}
    {% do run_query(create_table_aeroplane_normal) %}
    {% do log("Finished creating external tables in Spark.", info=True) %}
{% endmacro %}
