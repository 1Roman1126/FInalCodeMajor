from datetime import date, timedelta
import boto3
from nepseRequestParser import nepseReqParser
from responseParser import responseParser
import json

def lambda_handler(event, context):
    bucket_name = 'nepse-stock-data'  # Your S3 bucket name
    local_path = '/tmp/nepse_data.csv'  # Temporary path to save the file
    max_days_back = 5  # Limit the number of days to look back

    for i in range(max_days_back):
        _date = date.today() - timedelta(days=i)
        print(f"Trying to fetch data for date: {_date}")

        try:
            response = nepseReqParser(_date)
            print(f"Response length: {len(response.text)}")

            # If response is too small, market might be closed or no data for that date
            if len(response.text) < 300:
                print(f"No data for {_date}, trying the previous day...")
                continue  # Correctly using 'continue' inside the loop to try previous day
            else:
                # Process and upload the data to S3 if we get a valid response
                responseParser(response, _date, bucket_name, local_path)
                print(f"Data for {_date} processed and uploaded to {bucket_name}")
                break  # Exit loop once valid data is found
        except Exception as e:
            print(f"An error occurred while fetching data for {_date}: {str(e)}")
            continue  # Correct usage of 'continue' inside the loop

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda function executed successfully!')
    }
