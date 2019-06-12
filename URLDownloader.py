import sqlite3
import datetime
from pywebcopy import save_webpage

# pywebcopy docs found at: https://github.com/rajatomar788/pywebcopy

connection = sqlite3.connect(r"RedditArchive.db")
cursor = connection.cursor()

# Select URL from Downloads where DownloadStatus != 'DONE'

statement = """
SELECT d.SubredditID,
       d.SubmissionID,
       s.SubmissionTitle,
       s.URL
  FROM Downloads d
  INNER JOIN submissions s ON (d.SubredditID = s.SubredditID) and (d.SubmissionID = s.SubmissionID)
LIMIT 10;
"""

cursor.execute(statement)

prefix = 'Hive/Data'
count = 0
while count <= 10:
    count += 1
    results = cursor.fetchone()
    if results == None:
        break
    print(results)
    (SubredditID, SubmissionID, SubmissionTitle, URL) = results
    kwargs = {'project_name': 'PowerBee'}
    savePath = SubredditID + '/' + SubmissionID
    save_webpage(
        url=URL,
        project_folder=savePath,
        **kwargs
    )

