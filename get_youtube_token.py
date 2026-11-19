"""One-time YouTube OAuth token generator for Youtube-Automation-Agent.

Run once on your own machine (never on a public server):

    python get_youtube_token.py

It opens your browser for Google sign-in, asks you to allow YouTube
uploads for the channel you choose, and saves the resulting credentials
to ``token.json`` in this folder. The Streamlit dashboard reads that
file (upload it in Settings, or paste its contents there).

Requires:
- A ``client_secret.json`` in this folder (Google Cloud Console >
  APIs & Services > Credentials > Create Credentials > OAuth Client ID >
  Desktop App). See README section 5, Step A.
- ``google-auth-oauthlib`` (already in requirements.txt).

``token.json`` and ``client_secret.json`` are git-ignored. Never commit
them to a public repository.
"""

import json
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

BASE_DIR = Path(__file__).resolve().parent
CLIENT_SECRETS_FILE = BASE_DIR / "client_secret.json"
TOKEN_FILE = BASE_DIR / "token.json"

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def main() -> None:
    if not CLIENT_SECRETS_FILE.exists():
        raise SystemExit(
            "client_secret.json not found in the project folder.\n"
            "Create it first: Google Cloud Console > APIs & Services > "
            "Credentials > Create Credentials > OAuth Client ID > "
            "Desktop App, then download the JSON and save it as "
            "client_secret.json next to this script. See README section 5."
        )

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CLIENT_SECRETS_FILE), SCOPES
    )
    creds = flow.run_local_server(port=0)

    TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    print(f"Saved YouTube credentials to {TOKEN_FILE}")
    print("You can now close this window and start the dashboard:")
    print("    streamlit run app.py")


if __name__ == "__main__":
    main()
