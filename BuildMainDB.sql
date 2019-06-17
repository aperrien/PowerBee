--
-- File generated with SQLiteStudio v3.2.1 on Sun Jun 16 21:50:55 2019
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: ApplicationStatus
DROP TABLE IF EXISTS ApplicationStatus;

CREATE TABLE ApplicationStatus (
    LastRunStart        DATETIME,
    LastRunEnd          DATETIME,
    RunNumber           INTEGER,
    NumberOfComments    BIGINT,
    NumberOfSubmissions BIGINT,
    NumberOfSubreddits  BIGINT
);


-- Table: comments
DROP TABLE IF EXISTS comments;

CREATE TABLE comments (
    InternalID    BIGINT,
    FetchedTime   DATETIME,
    RedditorID    VARCHAR (25),
    CommentBody   TEXT,
    CreationTime  DATETIME,
    Distunguished VARCHAR (25),
    Edited        BOOLEAN,
    CommentID     VARCHAR (25),
    IsSubmitter   BOOLEAN,
    LinkID        VARCHAR (25),
    ParentID      VARCHAR (25),
    Permalink     TEXT,
    Score         INTEGER,
    Stickied      BOOLEAN,
    SubredditID   VARCHAR (25),
    PRIMARY KEY (
        CommentID ASC
    )
    ON CONFLICT REPLACE,
    UNIQUE (
        InternalID ASC
    )
    ON CONFLICT IGNORE
);


-- Table: Downloads
DROP TABLE IF EXISTS Downloads;

CREATE TABLE Downloads (
    SubredditID           VARCHAR (25),
    SubmissionID          VARCHAR (25),
    LastDownloadAttempted DATETIME,
    LastDownloadCompleted DATETIME,
    DownloadStatus        VARCHAR (80)  DEFAULT Never,
    DownloadAttemptCount  INTEGER       DEFAULT (0),
    LinkControl           VARCHAR (250),
    ServerReply           TEXT,
    PRIMARY KEY (
        SubredditID ASC,
        SubmissionID
    ),
    UNIQUE (
        SubredditID,
        SubmissionID
    )
    ON CONFLICT IGNORE
);


-- Table: redditor
DROP TABLE IF EXISTS redditor;

CREATE TABLE redditor (
    RedditorID    VARCHAR (25),
    RedditorName  VARCHAR (50),
    CreationTime  DATETIME,
    VerifiedEmail BOOLEAN,
    IsEmployee    BOOLEAN,
    IsFriend      BOOLEAN
);


-- Table: submissions
DROP TABLE IF EXISTS submissions;

CREATE TABLE submissions (
    InternalID      BIGINT,
    FetchedTime     DATETIME,
    DownloadStatus  INTEGER,
    DownloadCount   INTEGER,
    RedditorID      VARCHAR (25),
    CreationTime    DATETIME,
    Distunguished   VARCHAR (25),
    Edited          BOOLEAN,
    SubmissionID    VARCHAR (25),
    PostLocked      BOOLEAN,
    NSFW            BOOLEAN,
    Permalink       TEXT,
    Score           INTEGER,
    SelfText        TEXT,
    Stickied        BOOLEAN,
    SubredditID     VARCHAR (25),
    SubmissionTitle TEXT,
    UpvoteRatio     NUMBER,
    URL             TEXT,
    PRIMARY KEY (
        SubmissionID
    )
    ON CONFLICT IGNORE
);


-- Table: subreddits
DROP TABLE IF EXISTS subreddits;

CREATE TABLE subreddits (
    SubredditName     VARCHAR (150),
    SubredditID       VARCHAR (25),
    CreationTime      DATETIME,
    NSFW              BOOLEAN,
    Description       TEXT,
    DescriptionHTML   TEXT,
    PublicDescription TEXT,
    Rules             TEXT,
    DownloadStatus    INTEGER,
    DownloadCount     INTEGER,
    LastDownloadTime  DATETIME,
    PRIMARY KEY (
        SubredditID
    )
    ON CONFLICT IGNORE
);


-- Index: SubmissionIDIndex
DROP INDEX IF EXISTS SubmissionIDIndex;

CREATE INDEX SubmissionIDIndex ON submissions (
    SubmissionID
);


-- Index: SubmissionSubredditIDIndex
DROP INDEX IF EXISTS SubmissionSubredditIDIndex;

CREATE INDEX SubmissionSubredditIDIndex ON submissions (
    SubredditID
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
