from functools import reduce

from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_extract_all, lit, col, concat_ws

if __name__ == "__main__":
    spark = SparkSession.builder \
        .master("local[4]") \
        .appName("extract-boltic-air-data") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:4566") \
        .config("spark.hadoop.fs.s3a.access.key", "test") \
        .config("spark.hadoop.fs.s3a.secret.key", "test") \
        .config("spark.hadoop.fs.s3a.path.style.access", True) \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.sql.parquet.outputTimestampType", "TIMESTAMP_MILLIS") \
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262") \
        .getOrCreate()

    json_file = spark.read.option("multiline", "true").json("s3a://air-boltic/aeroplane_data/aeroplane_model.json")
    json_file.show()
    json_file.printSchema()

    df_list = []
    for manufacturer in json_file.schema.names:
        for model in json_file.select(f"{manufacturer}.*").schema.names:
            df_local = json_file.select(f"{manufacturer}.{model}.*")
            df_local = df_local.withColumn("aeroplane_manufacturer", lit(manufacturer))
            df_local = df_local.withColumn("aeroplane_model", lit(model))

            df_list.append(df_local)

    df_aeroplane_details = reduce(lambda x, y: x.union(y), df_list)
    df_aeroplane_details.show()

    df_aeroplane = (spark.read
                    .option("inferSchema", "true")
                    .option("header", "true")
                    .csv("s3a://air-boltic/air-boltic-data/aeroplane.csv"))
    df_aeroplane = df_aeroplane.select(col("Airplane ID").alias("aeroplane_id"),
                                       col("Airplane Model").alias("aeroplane_model"),
                                       col("Manufacturer").alias("aeroplane_manufacturer")
                                       )

    df_aeroplane = df_aeroplane.join(df_aeroplane_details,
                                     on=["aeroplane_manufacturer", "aeroplane_model"],
                                     how="left")
    df_aeroplane = df_aeroplane.withColumns(
        {
            "max_distance": col("max_distance").cast("int"),
            "max_seats": col("max_seats").cast("int"),
            "max_weight": col("max_weight").cast("int"),
        }
    )
    df_aeroplane.show()

    df_customer = (spark.read
                   .option("inferSchema", "true")
                   .option("header", "true")
                   .csv("s3a://air-boltic/air-boltic-data/customer.csv"))

    df_customer = df_customer.select(col("Customer ID").alias("customer_id"),
                                     col("Name").alias("customer_name"),
                                     col("Customer Group ID").alias("customer_group_id"),
                                     col("Email").alias("customer_email"),
                                     col("Phone Number").alias("customer_phone_number")).withColumn(
        "customer_phone_number", concat_ws("", regexp_extract_all("customer_phone_number", lit("([0-9+])+"), 0))
    )
    df_customer.show()

    df_customer_group = (spark.read
                         .option("inferSchema", "true")
                         .option("header", "true")
                         .csv("s3a://air-boltic/air-boltic-data/customer_group.csv"))
    df_customer_group = df_customer_group.select(col("ID").alias("customer_group_id"),
                                                 col("Type").alias("customer_group_type"),
                                                 col("Name").alias("customer_group_name"),
                                                 col("Registry number").alias("registry_number"))
    df_customer_group.show()

    df_order = (spark.read
    .option("inferSchema", "true")
    .option("header", "true")
    .csv(
        "s3a://air-boltic/air-boltic-data/order.csv"))

    df_order = df_order.select(col("Order ID").alias("order_id"),
                               col("Customer ID").alias("customer_id"),
                               col("Trip ID").alias("trip_id"),
                               col("Price (EUR)").alias("price_in_eur"),
                               col("Seat No").alias("seat_no"),
                               col("Status").alias("order_status"))
    df_order.show()

    df_trip = (spark.read
               .option("inferSchema", "true")
               .option("header", "true")
               .csv("s3a://air-boltic/air-boltic-data/trip.csv")
               )
    df_trip = df_trip.select(col("Trip ID").alias("trip_id"),
                             col("Origin City").alias("origin_city"),
                             col("Destination City").alias("destination_city"),
                             col("Airplane ID").alias("aeroplane_id"),
                             col("Start Timestamp").cast("timestamp_ntz").alias("trip_start_timestamp"),
                             col("End Timestamp").cast("timestamp_ntz").alias("trip_end_timestamp"),
                             )

    df_trip.show()

    df_aeroplane_details.write.mode("append").parquet("s3a://air-boltic-data-normalized/aeroplane_details/")
    df_aeroplane.write.mode("append").parquet("s3a://air-boltic-data-normalized/aeroplane/")
    df_customer.write.mode("append").parquet("s3a://air-boltic-data-normalized/customer/")
    df_customer_group.write.mode("append").parquet("s3a://air-boltic-data-normalized/customer_group/")
    df_order.write.mode("append").parquet("s3a://air-boltic-data-normalized/order/")
    df_trip.write.mode("append").parquet("s3a://air-boltic-data-normalized/trip/")
