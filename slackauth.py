import slack
import urllib.request
import requests
import os
from dotenv import load_dotenv

load_dotenv('.env')
client = slack.WebClient(token = os.getenv('SLACK_TOKEN')) 
client.files_upload(channels = os.getenv('CHANNEL_NAME', file='./report_R.pdf')
