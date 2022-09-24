from google.cloud import storage
import datetime
import json
from google.oauth2 import service_account
from google.cloud import secretmanager
import pygsheets
import pandas as pd
import pytz
  

        
#function that uploads requests content into a file object in a bucket
def upload_blob(bucket_name, blob_text, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(blob_text)

    print('CONTENT {} uploaded to {}.'.format(
        blob_text,
        destination_blob_name))

def access_secret_version():
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """
    
    
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/1039731898168/secrets/medidor-ita/versions/1"
    
    # Access the secret version.
    response = client.access_secret_version(request={"name": name})
    
    # Verify payload checksum.
    #crc32c = google_crc32c.Checksum()
    #crc32c.update(response.payload.data)
    #if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
    #    print("Data corruption detected.")
    #    return response

    # Print the secret payload.
    #
    # WARNING: Do not print the secret in a production environment - this
    # snippet is showing how to access the secret material.
    #payload = json.loads(response.payload.data.decode("UTF-8"))


    SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')
    service_account_info = json.loads(response.payload.data.decode("UTF-8"))
    
    
    my_credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    
    return my_credentials

def save_data_to_sheets (secret_info,data_request):
    
    
    sheets_access = pygsheets.authorize(custom_credentials=secret_info)
    
    invokation_data = json.dumps(data_request.decode('utf-8')).strip('\"')
    content = invokation_data.replace("'",'"')
    sheet_content = json.loads(content)
        
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1BMOClJJt3SjKobsfJGYRbZaIJ1C3dTu97hTKKvSnE5U"

    #data = gc.sheet.get("1BMOClJJt3SjKobsfJGYRbZaIJ1C3dTu97hTKKvSnE5U")
    sheet = sheets_access.open("controle-energia-ita")
    work = sheet.worksheet_by_title('Página2')
    

    work.cols # To view the number of columns
    work.rows # To view the number of rows
    print(f"There are {work.cols} columns in the googlesheet!")
    print(f"There are {work.rows} rows in the googlesheet!")

    sensor_values = list(sheet_content.values())
    timezone = pytz.timezone('America/Sao_Paulo')
    current_time = datetime.datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%I:%M%p on %B %d, %Y")
    sensor_values.append(current_time)
    

    #current_database = work.get_as_df()
    #print(len(current_database))
    
    
    
    #print(new_line_index)
    #current_database.loc[new_line_index] = sensor_values
    #current_database.head(n=12)
    work.insert_rows(work.rows, number=1,values=sensor_values,inherit=True)


def log_data_sw(request):
        
    request_content = request.data
    current_time = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    BUCKET_NAME = 'my-first-bucket-rafa-pde'
    BLOB_NAME = 'test-blob_' + current_time
    BLOB_STR = request_content
    
    #creates a file object on the project bucket
    upload_blob(BUCKET_NAME, BLOB_STR, BLOB_NAME)
    sheet_credentials =access_secret_version()
    results = save_data_to_sheets(sheet_credentials,BLOB_STR)
    return f'Success!'
