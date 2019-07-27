import sqlite3
import json


def nest(rows):
    root = {}
    for row in rows:
        d = root
        for item in row[:-2]:
            d = d.setdefault(item, {})
        d[row[-2]] = row[-1]
    return root


def pureID(idString):
    # returns the 'pure' base 36 id of the input string, for example:
    # t3_3z2yhb = 3z2yhb
    output = idString.replace('t3_','')
    return output


def fetchSubmissionComments(submissionID):
    connection = sqlite3.connect(r"..\RedditArchive.db")
    cursor = connection.cursor()
    statement = """
SELECT 
       SUBSTR(ParentID,4) as ParentID,
       CommentID,
       CommentBody,
       datetime(CreationTime,'unixepoch') as Creation_Time 
    FROM comments
WHERE LinkID = ?
"""
    cursor.execute(statement, (submissionID,))    # need a comma with a blank after it to pass in a single string:
    # https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta
    # (Kind of looks like a bug to me, too...)
    results = cursor.fetchall()
    commentList = nest(results)
    # Output is nested JSON
    return json.dumps(commentList, sort_keys=True, indent=4)



def fetchSubmissionData(submissionID):
    connection = sqlite3.connect(r"..\RedditArchive.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cID = pureID(submissionID)
    statement = """
SELECT InternalID,
       FetchedTime,
       DownloadStatus,
       DownloadCount,
       RedditorID,
       datetime(CreationTime,'unixepoch') as Creation_Time,
       Distunguished,
       Edited,
       SubmissionID,
       PostLocked,
       NSFW,
       Permalink,
       Score,
       SelfText,
       Stickied,
       SubredditID,
       SubmissionTitle,
       UpvoteRatio,
       URL
  FROM submissions
  WHERE SubmissionID = ?
  LIMIT 1;
    """
    cursor.execute(statement, (cID,))  # need a comma with a blank after it to pass in a single string:
    # https://stackoverflow.com/questions/16856647/sqlite3-programmingerror-incorrect-number-of-bindings-supplied-the-current-sta
    # (Kind of looks like a bug to me, too...)
    temp = cursor.fetchone()
    results = dict(zip(temp.keys(),tuple(temp)))
    return results