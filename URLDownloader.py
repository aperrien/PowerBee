import sqlite3
import datetime

from pywebcopy import WebPage, config
import pywebcopy
import yaml
import os.path

# pywebcopy docs found at: https://github.com/rajatomar788/pywebcopy

stream = open(r"PowerBeeConfig.yaml", 'r')
try:
    PBconfig = yaml.safe_load(stream)
except yaml.YAMLError as exc:
    print(exc)

downloaderConfig = PBconfig['downloader_config']

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
  AND 
  s.URL not LIKE '%reddit%'
  AND 
  s.URL not LIKE '%imgur%'

  ORDER BY RANDOM()
LIMIT 20;
"""

cursor.execute(statement)

results = cursor.fetchall()

# Folder paths for pywebcopy must be absolute paths.
# RE: https://github.com/rajatomar788/pywebcopy/issues/13
# Incorporated rajatomar788's fix, 15 Jun 2019, thanks!
#

fetchDownloadStatusStatment = """
SELECT 
       LastDownloadAttempted,
       LastDownloadCompleted,
       DownloadStatus,
       DownloadAttemptCount,
       LinkControl,
       ServerReply,
       LocalAbsoluteFilePath
    FROM Downloads
    WHERE SubredditID = ? AND 
       SubmissionID = ? 
"""


updateDownloadsStatement = """
UPDATE Downloads
   SET 
       LastDownloadAttempted = ?,
       LastDownloadCompleted = ?,
       DownloadStatus = ?,
       DownloadAttemptCount = ?,
       LinkControl = ?,
       ServerReply = ?,
       LocalAbsoluteFilePath = ?
    WHERE SubredditID = ? AND 
       SubmissionID = ? 
"""


prefix = os.path.normpath(downloaderConfig['download_root'])

count = 0

# TODO: Locate index.html file from pywebcopy download
# TODO: Add cases for other utilities to download, like youtube-dl, Newspaper3k, twitter-text-python
# TODO: Add logins for spacific web sites, like imgur, nytimes, etc.



for result in results:
    if result == None:
        print('No more records from DB!')
        break
    print(result)
    (SubredditID, SubmissionID, SubmissionTitle, URL) = result

    save_folder = os.path.join(prefix, SubredditID, SubmissionID)
    startDownloadTime = datetime.datetime.utcnow()
    config.setup_config(URL, save_folder, 'pb')
    wp = WebPage()
    try:
        wp.get(URL)
        wp.save_complete()
    except pywebcopy.exceptions.AccessError:
        DownloadStatus = 'Bad'

    endDownloadTime = datetime.datetime.utcnow()
    print('HTML folder:' + str(wp.file_path))

    (LastDownloadAttempted,
     LastDownloadCompleted,
     DownloadStatus,
     DownloadAttemptCount,
     LinkControl,
     ServerReply,
     LocalAbsoluteFilePath
     ) = cursor.execute(fetchDownloadStatusStatment, (SubredditID, SubmissionID))

    LastDownloadAttempted = str(startDownloadTime)
    LastDownloadCompleted = str(endDownloadTime)
    LocalAbsoluteFilePath = str(wp.file_path)

    cursor.execute(updateDownloadsStatement,
                (LastDownloadAttempted,
                 LastDownloadCompleted,
                 DownloadStatus,
                 DownloadAttemptCount,
                 LinkControl,
                 ServerReply,
                 LocalAbsoluteFilePath,
                 SubredditID,
                 SubmissionID
                 )
    )







