WITH
aC (d) as
(SELECT m.FetchedTime
  FROM submissions m
  INNER JOIN subreddits r ON (m.SubredditID = r.SubredditID)
  WHERE r.SubredditName = 'AskReddit'
  ORDER BY FetchedTime DESC
Limit 1)

,

bC (d) as
(SELECT m.FetchedTime
  FROM submissions m
  INNER JOIN subreddits r ON (m.SubredditID = r.SubredditID)
  WHERE r.SubredditName = 'AskReddit'
  ORDER BY FetchedTime ASC
Limit 1)

SELECT aC.d,bC.d, JulianDay(aC.d) - JulianDay(bC.d) AS DaysTaken FROM aC, bC
