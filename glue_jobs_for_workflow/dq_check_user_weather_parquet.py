import sys
import awswrangler as wr

# this check counts the number of NULL rows in the temp_C column
# if any rows are NULL, the check returns a number > 0
NULL_DQ_CHECK = f"""
SELECT 
    SUM(CASE WHEN temp_C IS NULL THEN 1 ELSE 0 END) AS res_col
FROM "de_project_database"."user_location_weather_data_parquet"
;
"""

# run the quality check
df = wr.athena.read_sql_query(sql=NULL_DQ_CHECK, database="de_project_database")

# exit if we get a result > 0
# else, the check was successful
if df['res_col'][0] > 0:
    sys.exit('Results returned. Quality check failed.')
else:
    print('Quality check passed.')
