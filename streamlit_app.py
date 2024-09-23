import streamlit as st
import os
import base64
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define a function to decode the base64 encoded service account JSON
def get_service_account():
    sa_value_encoded = os.getenv("SA_VALUE")
    if not sa_value_encoded:
        st.error("SA_VALUE environment variable not found!")
        return None

    try:
        sa_value_decoded = base64.b64decode(sa_value_encoded).decode('utf-8')
        service_account_info = json.loads(sa_value_decoded)
        return service_account_info
    except Exception as e:
        st.error(f"Failed to decode SA_VALUE: {str(e)}")
        return None

# Create a Google Sheet using the gspread module
def create_google_sheet(service_account_info):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
        client = gspread.authorize(credentials)

        # Create a new Google Sheet
        sheet = client.create('Streamlit Test Sheet')

        # Share it with the service account's email so it's accessible
        sheet.share(service_account_info['client_email'], perm_type='user', role='writer')

        return sheet.url
    except Exception as e:
        st.error(f"Error creating Google Sheet: {str(e)}")
        return None

# Streamlit UI
st.title("Google Sheets Creator with Service Account")

# Fetch the service account credentials from the environment variable
service_account_info = get_service_account()

if service_account_info:
    sheet_url = create_google_sheet(service_account_info)
    
    if sheet_url:
        st.success("Google Sheet successfully created!")
        st.write(f"Sheet URL: [Open Sheet]({sheet_url})")
else:
    st.error("Failed to load service account credentials. Check the SA_VALUE environment variable.")
