# PowerBee
PowerBee is a reddit downloader, allowing you to save submissions, comments, and content.
*This is still alpha code!* but it is useful.


### Usage:
1. After cloning the repository, install the dependencies by running `pip install -r requirements.txt`.
2. In order for the application to work, you will need to create an clientID and client secret (OAuth2 tokens) for reddit. You can do that by following the directions given here:
   - https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps
3. After you have those, enter those values into your `PowerBeeConfig.yaml` file, replacing the placeholder values.
4. Initialize the main SQLite database by running `python3 InitalizeDatabase.py`.
5. Now you can begin downloading from reddit. To start, run `python3 LoadSubredditsToDB.py`. This will load the database with all your subscribed subreddits.
!Note: This process may take a while, depending on reddit's server load.

6. Next, you can run the "RedditCommentExtractor003.py" script by running `python3 RedditCommentExtractor003.py`. This script iterates through all your saved subreddits, searching for saved submissions. It will then download up to 1750 of the "best" comments per submission.
!Note that this can can take a very long time, if you follow a lot of subreddits, and they are very active. For example, I have downloaded  40,099 submissions, from 733 subreddits, totaling some 8,975,214 comments.
This took about six *months* to do, however since PowerBee doesn't repeat itself on downloads, subsequent scheduled runs are now relatively fast.


### Dependencies:
- Python 3
- praw
- pywebcopy
- pyyaml
