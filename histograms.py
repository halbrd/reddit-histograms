import praw
import json
from pprint import pprint
import datetime as dt
import plotly.offline as ply
import plotly.graph_objs as go

credentials = json.load(open("credentials.json", "r"))

reddit = praw.Reddit(
    client_id = credentials["client_id"],
    client_secret = credentials["client_secret"],
    username = credentials["user_name"],
    password = credentials["user_pass"],
    user_agent = "Histograms"
)

user = reddit.redditor(credentials["user_name"])

user = {
    "comments": [vars(comment) for comment in user.comments.new(limit=None)][::-1],
    "downvoted": [vars(subm) for subm in user.downvoted(limit=None)][::-1],
    "saved": [vars(content) for content in user.saved(limit=None)][::-1],
    "submissions": [vars(subm) for subm in user.submissions.new(limit=None)][::-1],
    "upvoted": [vars(subm) for subm in user.upvoted(limit=None)][::-1]
}

###########

dates = [dt.datetime.fromtimestamp(int(subm["created_utc"])) for subm in user["upvoted"]]
titles = [subm["title"] for subm in user["upvoted"]]

data = [
    go.Scatter(
        x=dates,
        y=list(range(len(dates))),
        text=titles,
        mode="markers"
    ),
    # go.Scatter(
    #     x=dates,
    #     y=list(range(len(dates)))
    # )
]

ply.plot(data, filename='hist')
