import os
import json
from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

class YouTubeUploader:
    def __init__(self, client_secrets_file: Path, token_file: Path):
        self.client_secrets_file = client_secrets_file
        self.token_file = token_file

    def get_authenticated_service(self):
        creds = None
        if self.token_file.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(self.token_file), SCOPES)
            except Exception as e:
                print(f"[YouTube] Token load error: {e}")

        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                with open(self.token_file, 'w', encoding='utf-8') as f:
                    f.write(creds.to_json())
            except Exception as e:
                print(f"[YouTube] Token refresh error: {e}")
                creds = None

        if not creds or not creds.valid:
            raise RuntimeError(
                "YouTube authentication token (token.json) is missing or expired. "
                "Please upload your 'token.json' in the Settings tab on the Web UI."
            )

        return build('youtube', 'v3', credentials=creds)

    def upload_video(self, video_file: Path, title: str, description: str, tags: list, category_id: str = "28", privacy_status: str = "public") -> dict:
        if not video_file.exists():
            raise FileNotFoundError(f"Video file not found: {video_file}")

        youtube = self.get_authenticated_service()

        body = {
            'snippet': {
                'title': title[:100],
                'description': description,
                'tags': tags,
                'categoryId': str(category_id)
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }

        media = MediaFileUpload(str(video_file), mimetype='video/mp4', resumable=True, chunksize=1024*1024*10)
        request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)

        print(f"[YouTube] Uploading '{title}'...")
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"[YouTube] Upload progress: {int(status.progress() * 100)}%")

        video_id = response.get('id')
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"[YouTube] Upload complete: {video_url}")

        return {
            "status": "success",
            "video_id": video_id,
            "video_url": video_url,
            "privacy_status": privacy_status,
            "title": title
        }
