import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials

WAITTIME = 60
DEFAULT_PASS="housingtecaji"
# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("MojeZnanje stranke - dostop do videoteke").sheet1
Pre_Emails = sheet.col_values(1)
#Pre_Passowrds=sheet.col_values(2)
login_imports = ""
while(True):
    try:
        sheet = client.open("MojeZnanje stranke - dostop do videoteke").sheet1
        New_Email = sheet.col_values(1)
    except gspread.exceptions.SpreadsheetNotFound :
        print("Spread Sheet not found")
        exit(0)
    Email_diff = set(Pre_Emails) - set(New_Email)
    for emails in Email_diff:
        login_imports + emails + ":" + DEFAULT_PASS +"\n"
    print(login_imports)
    Pre_Emails = New_Email
    time.sleep(WAITTIME)
