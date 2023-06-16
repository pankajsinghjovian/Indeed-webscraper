from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os 



slack_scrapper_token = os.getenv('slack_scraper_token')
channel =os.getenv("channel_id")


# Set the path to the file you want to send
file_path = r"JOBS.CSV"

# #Setting up an Automated Text
message ="Here is the Indeed scrapped Jobs"

# Initialize the Slack WebClient
client = WebClient(token=slack_scrapper_token)

#Function to send the file
def send_file():
     response =client.files_upload_v2(
     channel = channel,
     file= file_path,
         )
     if response['ok']:
        print (f"File sent successful")
    
     else:
        print(f"Error sending file ")
    


