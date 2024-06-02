import boto3
from datetime import datetime

# create a string with the current UTC datetime
# convert all special characters to underscores
# this will be used in the table name and in the bucket path in S3 where the table is stored
DATETIME_NOW_INT_STR = str(datetime.utcnow()).replace('-', '_').replace(' ', '_').replace(':', '_').replace('.', '_')

client = boto3.client('athena')

# Refresh the table
queryStart = client.start_query_execution(
    QueryString = f"""
    CREATE TABLE user_location_weather_data_parquet_PROD_{DATETIME_NOW_INT_STR} WITH
    (external_location='s3://parquet-user-weather-table-prod-1/{DATETIME_NOW_INT_STR}/',
    format='PARQUET',
    write_compression='SNAPPY',
    partitioned_by = ARRAY['time'])
    AS

    SELECT
        *
    FROM "de_proj_database"."user_location_weather_data_parquet"

    ;
    """,
    QueryExecutionContext = {
        'Database': 'de_proj_database'
    }, 
    ResultConfiguration = { 'OutputLocation': 's3://athena-results-dchintada/'}
)


