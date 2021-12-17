import slack
import urllib.request
import requests

client = slack.WebClient(token = 'xoxb-596484384067-2508309944515-moy3XWjuLDgvSjtv3tCOwShp')
client.files_upload(channels = '#sector-materials', file='./report_R.pdf')
