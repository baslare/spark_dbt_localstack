import duckdb


if __name__ == "__main__":

    duckdb.sql(
                    "CREATE SECRET("
                    "TYPE S3, "
                    "KEY_ID 'localstack',"
                    "SECRET localstack123, "
                    "REGION 'eu-west-1', "
                    "ENDPOINT 'localhost:4566', "
                    "URL_STYLE 'path', "
                    "USE_SSL 'false'"
                    ");"
                )


    duckdb.sql(f"CREATE TABLE dim_aeroplane AS SELECT * FROM read_parquet('s3://air-boltic-data-warehouse/dim_aeroplane/*.parquet')")
    duckdb.sql(f"CREATE TABLE dim_customers AS SELECT * FROM read_parquet('s3://air-boltic-data-warehouse/dim_customers/*.parquet')")
    duckdb.sql(f"CREATE TABLE fact_orders AS SELECT * FROM read_parquet('s3://air-boltic-data-warehouse/fact_orders/*.parquet')")
    duckdb.sql(f"CREATE TABLE fact_trips AS SELECT * FROM read_parquet('s3://air-boltic-data-warehouse/fact_trips/*.parquet')")

    # Orders and revenue per customer
    result = duckdb.query("SELECT "
                          " dc.customer_id, "
                          " COUNT(fo.customer_id) as number_of_orders, "
                          " SUM(fo.price_in_eur) as revenue "
                          "FROM dim_customers as dc "
                          "LEFT JOIN fact_orders as fo on dc.customer_id = fo.customer_id "
                          "GROUP BY dc.customer_id")

    result.show()
    # Trips and revenue per aeroplane model
    result = duckdb.query("SELECT "
                          " ft.aeroplane_id,"
                          " COUNT(fo.trip_id) as number_of_trips, "
                          " SUM(fo.price_in_eur) as revenue "
                          "FROM fact_trips as ft "
                          "LEFT JOIN fact_orders as fo on ft.trip_id = fo.trip_id "
                          "GROUP BY ft.aeroplane_id")

    result.show()


    # Customer Activity

    result = duckdb.query("SELECT fo.customer_id, "
                          "max(ft.trip_end_timestamp) as last_flight,"
                          "count(fo.customer_id) as number_of_trips,  "
                          "FROM fact_trips as ft "
                          "LEFT JOIN fact_orders as fo on ft.trip_id = fo.trip_id "
                          "GROUP BY fo.customer_id "
                          "HAVING fo.customer_id is not NULL "
                          "ORDER BY last_flight")

    result.show()



