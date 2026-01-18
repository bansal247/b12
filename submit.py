import json
import hmac
import hashlib
from datetime import datetime, timezone
import sys
import urllib.request
import os


GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "your/repository")
GITHUB_RUN_ID = os.environ.get("GITHUB_RUN_ID", "run_id")
SUBMISSION_URL = "https://b12.io/apply/submission"
SIGNING_SECRET = b"hello-there-from-b12"

repository_link = f"https://github.com/{GITHUB_REPOSITORY}"
action_run_link = f"https://github.com/{GITHUB_REPOSITORY}/actions/runs/{GITHUB_RUN_ID}"
print("Repository Link:", repository_link)
print("Action Run Link:", action_run_link)

payload = {
    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
    "name": "Shashwat Bansal",
    "email": "shashwatbansal247@gmail.conm",
    "resume_link": "https://drive.google.com/file/d/1ubNxmi1de8A1-XE6L-KoiKaDC-EsPwC3/view?usp=sharing",
    "repository_link": repository_link,
    "action_run_link": action_run_link,
}

body = json.dumps(
    payload,
    separators=(",", ":"), ## Removes whitespace
    sort_keys=True, ## for HMAC-SHA256
).encode("utf-8")

digest = hmac.new(
    SIGNING_SECRET,
    body,
    hashlib.sha256
).hexdigest()

headers = {
    "Content-Type": "application/json",
    "X-Signature-256": f"sha256={digest}",
}

request = urllib.request.Request(
    SUBMISSION_URL,
    data=body,
    headers=headers,
    method="POST",
)

try:
    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")
        print("Status:", response.status)
        print("Response:", response_body)

        if response.status != 200:
            sys.exit(1)

except Exception as e:
    print("Error:", str(e))
    sys.exit(1)
