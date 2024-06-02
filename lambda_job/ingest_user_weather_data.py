import json
import boto3
import urllib3
import datetime
import logging
logger = logging.getLogger()
logger.setLevel("INFO")
# REPLACE WITH YOUR DATA FIREHOSE NAME
FIREHOSE_NAME = 'PUT-S3-uKmQp'

def lambda_handler(event, context):
    
    http = urllib3.PoolManager()

    r = http.request("GET", "https://randomuser.me/api/?results=50")

    # turn it into a dictionary
    r_dict = json.loads(r.data.decode(encoding='utf-8', errors='strict'))
    results = r_dict['results']
    # extract pieces of the dictionary
    processed_records = []
    for i in range(len(results)):
      single_result = results[i]
      processed_dict = {}
      processed_dict['gender'] = single_result['gender']
      processed_dict['city'] = single_result['location']['city']
      processed_dict['country'] = single_result['location']['country']
      processed_dict['latitude'] = single_result['location']['coordinates']['latitude']
      processed_dict['longitude'] = single_result['location']['coordinates']['longitude']
      processed_dict['birth_date'] = single_result['dob']['date']
      processed_dict['age'] = single_result['dob']['age']
      processed_dict['first_name'] = single_result['name']['first']
      processed_dict['last_name'] = single_result['name']['last']



      http = urllib3.PoolManager()
      logger.info(f"Connecting to https://api.open-meteo.com/v1/forecast?latitude={processed_dict['latitude']}&longitude={processed_dict['longitude']}&current=temperature_2m&temperature_unit=fahrenheit&timezone=America%2FNew_York")
      weather_response = http.request("GET", f"https://api.open-meteo.com/v1/forecast?latitude={processed_dict['latitude']}&longitude={processed_dict['longitude']}&current=temperature_2m&temperature_unit=fahrenheit&timezone=America%2FNew_York")

      # turn it into a dictionary
      weather_dict = json.loads(weather_response.data.decode(encoding='utf-8', errors='strict'))

      # extract pieces of the dictionary
      processed_dict['latitude'] = weather_dict['latitude']
      processed_dict['longitude'] = weather_dict['longitude']
      processed_dict['time'] = weather_dict['current']['time']
      processed_dict['temp'] = weather_dict['current']['temperature_2m']
      processed_dict['row_ts'] = str(datetime.datetime.now())
      msg = str(processed_dict) + '\n'

      processed_records.append({'Data': msg})

    fh = boto3.client('firehose')
    
    # send batch of records
    reply = fh.put_record_batch(
        DeliveryStreamName=FIREHOSE_NAME,
        Records=processed_records
    )

    return reply