-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players(ID serial PRIMARY KEY,
                     name text);

CREATE TABLE matches(ID serial PRIMARY KEY,
                     winner serial REFERENCES players(ID),
                     loser serial REFERENCES players(ID));


-- Summary of the below view:
--
-- This view creates and formats the needed outcome of the playerStandings
-- function.
--
-- In addition to retrieving a player's name and id, it also:
--
-- Counts up the number of wins for that player.
--		-  (This could potentially have been part of the main select clause,
--			but was done within a subquery, because otherwise the
--		    existence of an aggregate function in the main select
--		    clause causes PostgreSQL to need the other desired
--		    columns to be mentioned in a GROUP BY statement as well.
--          This would not have had the effect I wanted.)
--
-- Counts the player's total games played by counting the number of times
-- the player's id is found in the winner or loser columns.
--
-- These 2 subselects are joined with the players table in a 3-way join.
-- The wins and total games columns are selected, and then the resulting
-- table is sorted by number of wins.
--

CREATE VIEW standings AS
SELECT players.ID,
       players.name,
       winners.wins,
       played.totalgames
FROM players
JOIN
  (SELECT players.ID AS ID,
          count(matches.winner) AS wins
   FROM players
   LEFT JOIN matches ON players.ID=matches.winner
   GROUP BY players.ID) AS winners ON players.ID=winners.ID
JOIN
  (SELECT players.ID AS ID,
          count(matches.winner) AS totalgames
   FROM players
   LEFT JOIN matches ON players.ID=matches.winner
   OR players.ID=matches.loser
   GROUP BY players.ID) AS played ON played.ID=players.ID
ORDER BY winners.wins DESC;

