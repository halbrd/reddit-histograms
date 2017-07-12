import json
import praw
from pprint import pprint

credentials = json.load(open("credentials.json", "r"))

reddit = praw.Reddit(
    client_id = credentials["client_id"],
    client_secret = credentials["client_secret"],
    username = credentials["user_name"],
    password = credentials["user_pass"],
    user_agent = "Histograms"
)

user = reddit.redditor(credentials["user_name"])

upvoted = list(user.upvoted(limit=None))[::-1]

def extract_info(submission):
    import datetime as dt
    r = {}

    direct_copy = ["archived", "author_flair_text", "id", "link_flair_text", "num_comments", "permalink", "post_hint", "preview", "saved", "score", "selftext", "title", "url"]
    for attr in direct_copy:
        r[attr] = getattr(submission, attr) if hasattr(submission, attr) else None

    r["author"] = str(submission.author)
    r["subreddit"] = str(submission.subreddit)
    r["created"] = dt.datetime.fromtimestamp(submission.created_utc)

    return r

upvoted = [extract_info(subm) for subm in upvoted]
