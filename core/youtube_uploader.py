from pathlib import Path
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
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
            except Exception:
                pass

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(str(self.client_secrets_file), SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())

        return build('youtube', 'v3', credentials=creds)

    def upload_video(self, video_file: Path, title: str, description: str, tags: list, category_id: str = "28", privacy_status: str = "public") -> dict:
        youtube = self.get_authenticated_service()
        body = {
            'snippet': {
                'title': title[:100],
                'description': description,
                'tags': tags,
                'categoryId': str(category_id)
            },
            'status': {'privacyStatus': privacy_status, 'selfDeclaredMadeForKids': False}
        }
        media = MediaFileUpload(str(video_file), mimetype='video/mp4', resumable=True)
        request = youtube.videos().insert(part=','.join(body.keys()), body=body, media_body=media)
        
        response = None
        while response is None:
            status, response = request.next_chunk()

        video_id = response.get('id')
        return {
            "status": "success",
            "video_id": video_id,
            "video_url": f"https://www.youtube.com/watch?v={video_id}",
            "privacy_status": privacy_status
        }