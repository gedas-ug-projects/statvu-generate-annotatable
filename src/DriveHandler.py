import io
import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from tqdm import tqdm


def delete_auth():
    """Remove Google Auth token."""
    try:
        os.remove(" uth/token.json")
    except:
        print("No Token Found")


def set_auth():
    """TODO update authentication with service accounts"""
    creds = None

    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

    if os.path.exists("./src/auth/token.json"):
        creds = Credentials.from_authorized_user_file("./src/auth/token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "./src/auth/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("./src/auth/token.json", "w") as token:
            token.write(creds.to_json())


def reset_Auth():
    delete_auth()
    set_auth()

def validate_Auth() -> bool:
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

    if os.path.exists("./src/auth/token.json"):
        creds = Credentials.from_authorized_user_file("./src/auth/token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())

    return not (creds is None or not creds.valid)

def query(query: str) -> list[list[str]]:
    creds = Credentials.from_authorized_user_file("./src/auth/token.json")
    service = build("drive", "v3", credentials=creds)

    # Retrieve a list of files in the specified folder.
    nextPageToken = ""
    files = []
    while nextPageToken != None:
        results = (
            service.files()
            .list(
                q=query,
                fields="files(id, name, size), nextPageToken",
                spaces="drive",
                pageToken=nextPageToken,
                orderBy="name"
            )
            .execute()
        )
        files = files + results.get("files", [])
        nextPageToken = results.get("nextPageToken")

    # parse result into the following format: [name, id, size]
    dir_ids = []
    if not files:
        print("No files found.")
        return []
    else:
        for file in files:
            file_size = file.get("size") if file.get("size") is not None else 0
            dir_ids.append([file.get("name"), file.get("id"), int(file_size)])
    return dir_ids


def download_file(real_file_id, output_dir: str):
    """Downloads a file

    Args:
        real_file_id: ID of the file to download
        output_dir: dir to store downloaded file
    Returns : IO object with location.
    """
    creds = Credentials.from_authorized_user_file("./src/auth/token.json")

    try:
        # create drive api client
        service = build("drive", "v3", credentials=creds)

        file_id = real_file_id

        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        pbar = tqdm(total=100, desc=f"Downloading {real_file_id}")
        while done is False:
            status, done = downloader.next_chunk()
            pbar.reset()
            pbar.update(int(status.progress() * 100))
            pbar.refresh()
        # pbar.reset()
        # pbar.update(100)
        pbar.close()

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None
        return

    with open(output_dir, "wb") as f:
        f.write(file.getvalue())
