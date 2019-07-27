import sqlite3
import datetime
import yaml
import json

# This is a testbed for the eventual web interface. The goal is to take a nested submission from the database
# and output it as a nested JSON file, which will eventually be fed into a jquery/bootstrap frontend.
# Still deciding on the middle web serving component.

# In this case, the test is submission ID t3_3z2yhb, otherwise known by this link:
# /r/Futurology/comments/3z2yhb/i_was_born_deaf_and_i_had_just_received_my_first/
#

def nest(rows):
    root = {}
    for row in rows:
        d = root
        for item in row[:-2]:
            d = d.setdefault(item, {})
        d[row[-2]] = row[-1]
    return root


# Open a submission, store it's comments in a nested dictionary

stream = open(r"PowerBeeConfig.yaml", 'r')
try:
    PBconfig = yaml.safe_load(stream)
except yaml.YAMLError as exc:
    print(exc)

downloaderConfig = PBconfig['downloader_config']

connection = sqlite3.connect(r"RedditArchive.db")
cursor = connection.cursor()



statement = """
SELECT 
       SUBSTR(ParentID,4) as ParentID,
       CommentID,
       CommentBody,
       datetime(CreationTime,'unixepoch') as Creation_Time 
    FROM comments
WHERE LinkID = 't3_3z2yhb'
"""

cursor.execute(statement)

results = cursor.fetchall()

commentList = nest(results)


# Output is nested JSON
print(json.dumps(commentList, sort_keys=True, indent=4))