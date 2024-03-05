# Install the requirements if needed with: pip install fastapi uvicorn httpx
# Run the app using the command: uvicorn Extracting_bookmarks_from_Reddit:app --reload
# Access your local host at http://127.0.0.1:8000/reddit
# Give access to your Reddit account and visualize the contents of reddit_saved.csv


from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
import httpx
import os
from requests_oauthlib import OAuth2Session
from dotenv import load_dotenv
load_dotenv()
import praw
import prawcore
import csv
import codecs


REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")

REDIRECT_URI = 'http://127.0.0.1:8000/reddit/callback'
reddit_home_url = 'https://www.reddit.com'

app = FastAPI()

def reddit_authorization_token(request: Request):
    return request.cookies.get("reddit_refresh_token")

@app.get("/reddit", response_class=HTMLResponse)
def connect_to_reddit(request: Request, refresh_token: str = Depends(reddit_authorization_token)):
    if refresh_token:
        user_saved_items = get_user_saved_items(refresh_token)
        return user_saved_items
    else:
        return RedirectResponse(url="/reddit/authorize")
    

@app.get("/reddit/authorize")
def reddit_authorize():
    authorization_url = f"https://www.reddit.com/api/v1/authorize?" \
                        f"client_id={REDDIT_CLIENT_ID}&" \
                        f"response_type=code&" \
                        f"state=random_state&" \
                        f"redirect_uri={REDIRECT_URI}&" \
                        f"duration=permanent&" \
                        f"scope=identity,read,save,history"
    return RedirectResponse(url=authorization_url)

@app.get("/reddit/callback")
def reddit_callback(request: Request, code: str):
    tokens = get_tokens(code)
    response = RedirectResponse(url="/reddit")
    response.set_cookie(key="reddit_token", value=tokens["access_token"])
    response.set_cookie(key="reddit_refresh_token", value=tokens["refresh_token"])
    return response


# Functions

def get_reddit_instance(refresh_token):
    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        refresh_token=refresh_token,
        user_agent="testscript by Icy_Consideration415",
    )
    return reddit

def get_tokens(authorization_code: str):
    data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": REDIRECT_URI,
        "duration": "permanent",
        "scope": "identity,read,save,history",
    }
    response = httpx.post("https://www.reddit.com/api/v1/access_token", data=data, auth=(REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET))
    response.raise_for_status()
    return response.json()

def get_user_saved_items(refresh_token):
    reddit = get_reddit_instance(refresh_token)
    saved_models = reddit.user.me().saved(limit=None)
    reddit_saved_csv = codecs.open('reddit_saved.csv', 'w', 'utf-8')
    saved_csv_writer = csv.writer(reddit_saved_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    saved_csv_writer.writerow(['ID', 'Name', 'Subreddit', 'Type', 'URL', 'Content', 'NoSFW'])
    handle_saved_bookmarks(saved_models, saved_csv_writer)
    reddit_saved_csv.close()
    with open('reddit_saved.csv', 'r', encoding='utf-8') as file:
        return file.read()

def handle_saved_bookmarks(saved_models, saved_csv_writer):
    count = 1
    for model in saved_models:
        subreddit = model.subreddit
        subr_name = subreddit.display_name
        url = reddit_home_url + model.permalink

        if isinstance(model, praw.models.Submission):
            title = model.title
            submission_content = f"{model.author} posted: {model.selftext}"
            comments_content = '\n\n'.join(f"{comment.author} replied: {comment.body}" for comment in model.comments if comment.author)
            content = f"---Post:---\n{submission_content}\n\n---Comments:---\n\n{comments_content}"
            noSfw = str(model.over_18)
            model_type = "#Post"
        else:
            title = model.submission.title
            content = f"{model.author} commented: {model.body}"
            noSfw = str(model.submission.over_18)
            model_type = "#Comment"

        saved_csv_writer.writerow([str(count), title, subr_name, model_type, url, content, noSfw])
        count += 1