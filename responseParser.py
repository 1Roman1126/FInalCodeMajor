import csv
import boto3
from io import StringIO, BytesIO

def responseParser(response, _date, bucket_name, local_path):
    if response.ok:
        print("Processing API response...")
        content = response.content.decode('utf-8')
        lines = content.splitlines()
        csv_reader = csv.reader(lines)

        output = StringIO()
        csv_writer = csv.writer(output)
        
        headers = next(csv_reader)  # Capture headers
        csv_writer.writerow(headers)
        
        for row in csv_reader:
            csv_writer.writerow(row)
        
        # Convert StringIO content to BytesIO for S3 upload
        output.seek(0)  # Rewind to the beginning of StringIO
        bytes_output = BytesIO(output.read().encode('utf-8'))  # Encode string to bytes
        
        # Save to local file system in Lambda's /tmp directory
        with open(local_path, 'w') as f:
            f.write(output.getvalue())
        
        # Upload to S3 from BytesIO
        s3 = boto3.client('s3')
        try:
            bytes_output.seek(0)  # Important: rewind to the beginning!
            print(f"Uploading file to S3 bucket: {bucket_name}")
            s3.upload_fileobj(bytes_output, bucket_name, f'nepse_data_{_date}.csv')
            print(f"File successfully uploaded to S3: nepse_data_{_date}.csv")
        except Exception as e:
            print(f"Error uploading file to S3: {str(e)}")
        
        bytes_output.close()
        output.close()
    else:
        print(f"Failed to fetch data from API. Status code: {response.status_code}")
