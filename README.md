# PowerBee
PowerBee is a reddit downloader, allowing you to save submissions, comments, and content.
*Theis is still alpha code!* but it is useful. 


Usage:
After unpacking and installing dependencies, you will need to create an clientID and client secret (OAuth2 tokens) for reddit. You can do that by following the directions given here:
https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps

After you have those, enter those values into your PowerBeeConfig.yaml file, replacing the placeholder values.
Initialize the main SQLite database by running the BuildMainDB.sql file. (There will be an automated process for this soon)

Now you can begin dowloading from reddit. To start, run "LoadSubredditsToDB.py". This will load the database with all your subscribed subreddits.
This process may take a while, depending on reddit's server load.

Next, you can run the "RedditCommentExtractor003.py" script. This script iterates through all your saved subreddits, searching for saved submissions. It will then download up to 1750 of the "best" comments per submission.
Note that this can can take a very long time, if you follow a lot of subreddits, and they are very active. For example, I have downloaded  40,099 submissions, from 733 subreddits, totaling some 8,975,214 comments.
This took about six *months* to do, however since PowerBee doesn't repeat itself on downlaods, subsequent scheduled runs are now relatively fast.


Dependencies:
Python 3
praw
pywebcopy
pyyaml (Should be in most distributions)
