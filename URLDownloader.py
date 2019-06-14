import sqlite3
import datetime
from pywebcopy import save_webpage
import yaml

# pywebcopy docs found at: https://github.com/rajatomar788/pywebcopy

stream = open(r"PowerBeeConfig.yaml", 'r')
try:
    config = yaml.safe_load(stream)
    downloaderConfig = config['downloader_config']
    print(config)
except yaml.YAMLError as exc:
    print(exc)



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

# Folder paths for pywebcopy must be absolute paths.
# RE: https://github.com/rajatomar788/pywebcopy/issues/13
#
prefix = r'H:\Python\PowerBee\Hive\Data'
prefix = downloaderConfig['download_root']
count = 0
while count <= 10:
    count += 1
    results = cursor.fetchone()
    if results == None:
        break
    print(results)
    (SubredditID, SubmissionID, SubmissionTitle, URL) = results
    kwargs = {'project_name': ''}

    save_webpage(
        url=URL,
        project_folder=prefix + r'\\' + SubredditID + r'\\' + SubmissionID,
        **kwargs
    )

