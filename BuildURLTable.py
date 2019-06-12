import sqlite3
import datetime
import pywebcopy

# pywebcopy docs found at: https://github.com/rajatomar788/pywebcopy




connection = sqlite3.connect(r"RedditArchive.db")
cursor = connection.cursor()



# INSERT INTO Downloads(SubredditID, SubmissionID) SELECT SubredditID, SubmissionID FROM submissions

