import time
import logging
import sqlite3
import datetime
import praw
import yaml
from prawcore import NotFound, RequestException, ResponseException, OAuthException, ServerError


stream = open(r"PowerBeeConfig.yaml", 'r')
try:
    config = yaml.safe_load(stream)
    redditConfig = config['reddit_config']

except yaml.YAMLError as exc:
    print(exc)
reddit = praw.Reddit(**redditConfig)

                     
def get_csv_rows(reddit, seq):
    """get csv rows.

    Args:
        reddit: reddit praw's instance
        seq (list): List of Reddit item.

    Returns:
        list: Parsed reddit item.
    """
    csv_rows = []
    plinks = []
    reddit_url = reddit.config.reddit_url

    # filter items for link
    for idx, i in enumerate(seq, 1):
        logging.info('processing item #{}'.format(idx))

        if not hasattr(i, 'title'):
            i.title = i.link_title

        # Fix possible buggy utf-8
        title = i.title.encode('utf-8').decode('utf-8')
        try:
            logging.info('title: {}'.format(title))
        except UnicodeEncodeError:
            logging.info('title: {}'.format(title.encode('utf8', 'ignore')))

        try:
            created = int(i.created)
        except ValueError:
            created = 0

        try:
            folder = str(i.subreddit).encode('utf-8').decode('utf-8')
        except AttributeError:
            folder = "None"

        if callable(i.permalink):
            permalink = i.permalink()
        else:
            permalink = i.permalink
        permalink = permalink.encode('utf-8').decode('utf-8')

        csv_rows.append([reddit_url + permalink, title, created, None, folder])
        plinks.append(reddit_url + permalink)

    return plinks 



connection = sqlite3.connect(r"RedditArchive.db")
cursor = connection.cursor()


cursor.execute("SELECT RunNumber FROM ApplicationStatus ORDER BY RunNumber DESC LIMIT 1")

runNumber = cursor.fetchone()[0]

print("Run Number ---> " + str(runNumber))

runNumber = runNumber + 1

cursor.execute("INSERT INTO ApplicationStatus ( LastRunStart, RunNumber ) VALUES ( ?, ? )",
               ( datetime.datetime.utcnow(), runNumber ) )
connection.commit()


# Add select statement for subreddits table here

cursor.execute("SELECT SubredditName FROM subreddits")

# Store the subreddits to a list

mySubreddits = cursor.fetchall()

#mysubs = ['MensLib', 'spacex', 'cyberpunk', 'DataHoarder' ]

submissionCount = 0
totalComments = 0



for subreddit in mySubreddits:
    print("Checking on the " + subreddit[0] + " subreddit")
    cursor.execute("SELECT DownloadStatus, DownloadCount FROM subreddits "
                   "WHERE SubredditName = ?", (subreddit[0],))
    subredditRows = cursor.fetchone()

    #print('Rows:->', str(subredditRows))
    #sys.exit()
    if subredditRows[0] != 200:
        # Loop through subreddit, running this code for each one
        seq = reddit.user.me().saved(limit=1500, params={'sr':subreddit[0]})
        # Vary this line depending on the subreddit's name

        html_links = get_csv_rows(reddit, seq)

        for link in html_links:
            saved = reddit.submission(url=link)
            now = datetime.datetime.now()
            unow = datetime.datetime.utcnow()
            submission = saved
            comcount = 1

            try:
                # In case of a standard submission
                test = str(saved.url)
                submission = saved
                # Test if the submission has already been downloaded
                cursor.execute("SELECT DownloadStatus, DownloadCount FROM submissions "
                               "WHERE SubmissionID = ?", (submission.id,))
                submissionRows = cursor.fetchall()
                if submissionRows != []:
                    # If so, track it, but skip downloading it
                    submissionCount = submissionCount + 1
                    pass
                # If not, save submission and comments to DB
                else:
                    # Log the submission
                    cursor.execute( " INSERT INTO submissions "
                                    " ( FetchedTime, DownloadStatus, DownloadCount, " 
                                    " RedditorID, CreationTime, Distunguished, Edited, "
                                    " SubmissionID, PostLocked, NSFW, Permalink, Score, SelfText, "
                                    " Stickied, SubredditID, SubmissionTitle, UpvoteRatio, URL ) "
                                    " VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ",
                    ( str(unow), '0', '0', submission.author.id, submission.created_utc, submission.distinguished,
                      submission.edited, submission.id, submission.locked, submission.over_18,
                      submission.permalink, submission.score, submission.selftext, submission.stickied,
                      submission.subreddit_id, submission.title, submission.upvote_ratio, submission.url ))
                    connection.commit()
                    print('Title     -->' + submission.title)
                    print('Link      -->' + submission.permalink)
                    print('ID        -->' + submission.id)
                    print('At        -->' + str(now))
                    print('Sub No.   --#' + str(submissionCount))
                    submission.comment_sort = 'best'
                    submission.comments.replace_more(limit=None)
                    submissionCount = submissionCount + 1

                    # Log the submission's comments
                    for comment in submission.comments.list():
                        try:
                            unow = datetime.datetime.utcnow()
                            cursor.execute( " INSERT INTO comments "
                                            " (FetchedTime, RedditorID, CommentBody, CreationTime, Distunguished,"
                                            " Edited, CommentID, IsSubmitter, LinkID, ParentID, Permalink, Score,"
                                            " Stickied, SubredditID) "
                                            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ",
                            ( str(unow),comment.author.id, comment.body, comment.created_utc, comment.distinguished,
                              comment.edited, comment.id, comment.is_submitter, comment.link_id, comment.parent_id,
                              comment.permalink, comment.score, comment.stickied, comment.subreddit_id ))
                            comcount = comcount + 1
                            # Only download 1750 comments max
                            if comcount >= 1750:
                                print("---> Hit Comment Cap! Continuing to next submission...")
                                break
                            totalComments = totalComments + 1
                        except AttributeError:
                            pass
                        except NotFound:
                            time.sleep(2)
                            pass
                        except (RequestException,  ResponseException, OAuthException, ServerError ):
                            print('---- Reddit is busy. Waiting ----')
                            print('----> Starting 45 min sleep at ' + str(now) + ' <----')
                            time.sleep(2700)
                            print('---- Leaving sleep, resuming download ----')



            except AttributeError:
                try:
                    # In case of a saved comment, log the comment
                    test = str(saved.is_submitter)
                    comment = saved
                    cursor.execute( " INSERT INTO comments "
                            " (FetchedTime, RedditorID, CommentBody, CreationTime, Distunguished,"
                            " Edited, CommentID, IsSubmitter, LinkID, ParentID, Permalink, Score,"
                            " Stickied, SubredditID) "
                            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ",
                    ( str(now),comment.author.id, comment.body, comment.created_utc, comment.distinguished,
                      comment.edited, comment.id, comment.is_submitter, comment.link_id, comment.parent_id,
                      comment.permalink, comment.score, comment.stickied, comment.subreddit_id ))
                    comcount = comcount + 1
                    totalComments = totalComments + 1
                except AttributeError:
                    pass
                except NotFound:
                    time.sleep(2)
                    pass
                connection.commit()
            except NotFound:
                time.sleep(2)
                pass
            except ServerError:
                now = datetime.datetime.now()
                print('---- Reddit is busy (replace_more error). Waiting ----')
                print('----> Starting 45 min sleep at ' + str(now) + ' <----')
                time.sleep(2700)
                print('---- Leaving sleep, resuming download ----')

            now = datetime.datetime.now()

            #
            # Now that the submission is downloaded, mark that in the submission table
            #
            cursor.execute("""
    UPDATE submissions
    SET
       DownloadStatus = ?,
       DownloadCount = ?
    WHERE
       SubmissionID = ?""",
                           ('200', '1', submission.id))
            print('Last comment stored at ' + str(now))
            print('Stored ' + str(comcount) + ' comments, ' + str(totalComments) + ' in total.')
            print('######################################################')

        updateSubredditStatus = """
UPDATE subreddits
SET DownloadStatus = ?,
    DownloadCount = ?
WHERE 
    SubredditName = ?
"""
        cursor.execute(updateSubredditStatus, ('200', '1', str(subreddit[0])))
        print("================================================")
        print("Finished importing " + str(subreddit[0]))
        print("================================================")
        time.sleep(10)
    else:
        print("Downloaded " + subreddit[0] + " already.")
        pass


now = datetime.datetime.now()
unow = datetime.datetime.utcnow()

updateCommand = """
UPDATE ApplicationStatus 
SET LastRunEnd = ?,
	NumberOfComments = ?,
	NumberOfSubmissions = ?,
	NumberOfSubreddits = ?
WHERE
	RunNumber = ?
"""

cursor.execute(updateCommand,
               (str(unow), str(totalComments), str(submissionCount), str(len(mySubreddits)), str(runNumber))
               )

connection.commit()


connection.close()
