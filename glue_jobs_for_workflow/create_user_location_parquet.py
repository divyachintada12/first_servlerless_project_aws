import boto3

client = boto3.client('athena')

# Refresh the table
queryStart = client.start_query_execution(
    QueryString = """
    CREATE TABLE user_location_weather_data_parquet WITH
    (external_location='s3://user-location-weather-data-parquet-bucket/',
    format='PARQUET',
    write_compression='SNAPPY',
    partitioned_by = ARRAY['time'])
    AS

    SELECT gender
       ,city
       ,country
       ,latitude
       ,longitude
       ,birth_date
       ,age
       ,first_name
       ,last_name
       ,row_ts
       ,(temp - 32) * (5.0/9.0) AS temp_C
       ,temp AS temp_F
       ,(substr(time,1,10)) as time
    FROM "de_project_database"."user_location_weather_datausers_data_random"

    ;
    """,
    QueryExecutionContext = {
        'Database': 'de_project_database'
    }, 
    ResultConfiguration = { 'OutputLocation': 's3://athena-results-dchintada'}
)

