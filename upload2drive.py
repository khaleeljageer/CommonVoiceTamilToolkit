import os
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# =====================================================
# CONFIGURATION
# =====================================================

CSV_DIR = "csv_output"

# Replace with your Google Drive folder ID
DRIVE_FOLDER_ID = "1b3NLjnNcmqKApU55f2zSoIuYnna8Wq8a"

# Failed upload report file
FAILED_REPORT_FILE = "failed_uploads.txt"

# Google Drive API scope
SCOPES = ['https://www.googleapis.com/auth/drive.file']

# =====================================================
# AUTHENTICATION
# =====================================================

flow = InstalledAppFlow.from_client_secrets_file(
    'credentials.json',
    SCOPES
)

creds = flow.run_local_server(port=0)

service = build('drive', 'v3', credentials=creds)

# =====================================================
# GET CSV FILES
# =====================================================

csv_files = list(Path(CSV_DIR).glob("*.csv"))

print(f"Found {len(csv_files)} CSV files")
print("-" * 60)

# =====================================================
# TRACKING
# =====================================================

uploaded_count = 0
failed_count = 0

failed_files = []

# =====================================================
# UPLOAD FILES
# =====================================================

for index, file_path in enumerate(csv_files, start=1):

    try:
        print(f"[{index}/{len(csv_files)}] Uploading: {file_path.name}")

        file_metadata = {
            'name': file_path.name,
            'parents': [DRIVE_FOLDER_ID]
        }

        media = MediaFileUpload(
            str(file_path),
            mimetype='text/csv',
            resumable=True
        )

        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        uploaded_count += 1

        print(f"SUCCESS: {file_path.name}")
        print(f"File ID: {uploaded_file.get('id')}")
        print("-" * 60)

    except Exception as e:

        failed_count += 1

        error_message = str(e)

        failed_files.append(
            f"{file_path.name} -> {error_message}"
        )

        print(f"FAILED: {file_path.name}")
        print(f"Reason: {error_message}")
        print("-" * 60)

# =====================================================
# SAVE FAILED REPORT
# =====================================================

with open(FAILED_REPORT_FILE, "w", encoding="utf-8") as f:

    f.write("FAILED FILE UPLOAD REPORT\n")
    f.write("=" * 60 + "\n\n")

    for item in failed_files:
        f.write(item + "\n")

# =====================================================
# FINAL REPORT
# =====================================================

print("\n")
print("=" * 60)
print("UPLOAD SUMMARY")
print("=" * 60)

print(f"Total Files       : {len(csv_files)}")
print(f"Successfully Uploaded : {uploaded_count}")
print(f"Failed Uploads    : {failed_count}")

print("\nFailed report saved to:")
print(FAILED_REPORT_FILE)

print("=" * 60)