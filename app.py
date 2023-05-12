import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set up the OAuth client credentials
flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json",
    scopes=["https://www.googleapis.com/auth/drive"])
credentials = flow.run_local_server(port=0)

# Create a Drive API client object
service = build("drive", "v3", credentials=credentials)

# Define a function to save file uploads to a directory in Google Drive
def save_to_drive(file, folder_id):
    try:
        file_metadata = {"name": "one.pdf", "parents": [folder_id]}
        media = {"body": file}
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        st.success(f"File saved to Google Drive with ID: {file.get('id')}")
    except HttpError as error:
        st.error(f"An error occurred: {error}")


# Create a file uploader widget
file = st.file_uploader("Upload a file")

# Create a button to save the file to Google Drive
if file:
    folder_id = "1_RJzCJfdZZNMBAeIzJgtc2l-FDYvxMWO"
    if st.button("Save to Google Drive"):
        save_to_drive(file, folder_id)
