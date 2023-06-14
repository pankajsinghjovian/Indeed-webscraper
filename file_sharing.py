from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os 


slack_token = os.getenv('slack_token')
slack_scrapper_token = os.getenv('slack_scraper_token')
print(slack_token)
print(slack_scrapper_token)


# Set the path to the file you want to send
file_path = r"JOBS.CSV"


# #Setting up an Automated Text
message ="Here is the scrapped Jobs"

# Initialize the Slack WebClient
client = WebClient(token=slack_scrapper_token)
channel =os.getenv("channel_id")
#Function to send the file
def send_file():
     response =client.files_upload_v2(
    
        channel = channel,
        file= file_path
    )
    

     if response['ok']:
        print (f"File sent successful")
    
     else:
        print(f"Error sending file ")
    


