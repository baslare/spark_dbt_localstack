import boto3
import glob

if __name__ == "__main__":
    s3_client = boto3.client('s3',
                             endpoint_url="http://localhost:4566",
                             aws_access_key_id="test",
                             aws_secret_access_key="test",
                             region_name="eu-west-1")

    s3_client.create_bucket(Bucket="air-boltic",
                            CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'}
                            )

    with open("data/aeroplane_model.json", "rb") as f:
        s3_client.put_object(Bucket="air-boltic",
                             Key="aeroplane_data/aeroplane_model.json",
                             Body=f,
                             ContentType='application/json')

    csv_file_list = glob.glob("data/*.csv")

    for csv_file in csv_file_list:
        with open(csv_file, "rb") as f:
            s3_client.put_object(Bucket="air-boltic",
                                 Key=f"air-boltic-data/{csv_file.replace('data/', '')}",
                                 Body=f,
                                 ContentType='text/csv')

    s3_client.create_bucket(Bucket="air-boltic-data-normalized",
                            CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})

    s3_client.create_bucket(Bucket="air-boltic-data-warehouse",
                            CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})
