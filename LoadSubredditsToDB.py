import sqlite3
import datetime
import praw
import yaml

stream = open(r"H:\Python\PowerBeeConfig.yml",'r')
try:
    config = yaml.safe_load(stream)
    redditConfig = config['reddit_config']

except yaml.YAMLError as exc:
    print(exc)
reddit = praw.Reddit(**redditConfig)

connection = sqlite3.connect(r"RedditArchive.db")
cursor = connection.cursor()


print("Start Time->" + str(datetime.datetime.now()))


subgen = reddit.user.subreddits(limit=None)
subcount = 1
for sub in subgen:
    cutc = str(datetime.datetime.fromtimestamp(sub.created_utc))

    cursor.execute("INSERT INTO subreddits "
                   "( SubredditName, SubredditID, CreationTime, NSFW, "
                   "Description, DescriptionHTML, PublicDescription, Rules, DownloadStatus, DownloadCount)"
                   " VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   ( sub.display_name, sub.fullname, cutc, sub.over18,
                     sub.description, sub.description_html, sub.public_description, str(sub.rules()), '0', '0'
                     )
                   )
    print('Inserted #' + str(subcount) + ' ' + sub.display_name)
    subcount += 1

    


connection.commit()
print("Stop Time->" + str(datetime.datetime.now()))

connection.close()
