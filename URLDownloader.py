import sqlite3
import datetime
from pywebcopy import save_webpage
import yaml
import os.path

# pywebcopy docs found at: https://github.com/rajatomar788/pywebcopy

stream = open(r"PowerBeeConfig.yaml", 'r')
try:
    config = yaml.safe_load(stream)
except yaml.YAMLError as exc:
    print(exc)

downloaderConfig = config['downloader_config']

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
  WHERE s.URL is not NULL 
  ORDER BY RANDOM()
LIMIT 20;
"""

cursor.execute(statement)

# Folder paths for pywebcopy must be absolute paths.
# RE: https://github.com/rajatomar788/pywebcopy/issues/13
# Incorporated rajatomar788's fix, 15 Jun 2019, thanks!
#

prefix = os.path.normpath(downloaderConfig['download_root'])

count = 0

# TODO: Locate index.html file from pywebcopy download
# TODO: Add cases for other utilities to download, like youtube-dl, Newspaper3k, twitter-text-python
# TODO: Add logins for spacific web sites, like imgur, nytimes, etc.


while count <= 20:
    count += 1
    results = cursor.fetchone()
    if results == None:
        break
    print(results)
    (SubredditID, SubmissionID, SubmissionTitle, URL) = results
    kwargs = {'project_name': ''}

    save_webpage(
        url=URL,
        # Use builtin path module for path manipulation
        project_folder=os.path.join(prefix, SubredditID, SubmissionID),
        **kwargs
    )

