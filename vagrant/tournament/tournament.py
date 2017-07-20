#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("delete from matches;")
    connection.commit()
    connection.close


def deletePlayers():
    """Remove all the player records from the database."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("delete from players;")
    connection.commit()
    connection.close


def countPlayers():
    """Returns the number of players currently registered."""
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("select count(*) as num from players;")
    results = cursor.fetchall()
    connection.close
    if not results:
        results = 0
    return int(results[0][0])



def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.
  
    Args:
      name: the player's full name (need not be unique).
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("insert into players (name) values(%s);",(name,))
    connection.commit()
    connection.close


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("select * from standings;")
    results = cursor.fetchall()
    connection.close
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("insert into matches (winner, loser) values(%s,%s);",(winner, loser))
    connection.commit()
    connection.close


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    
    connection = connect()
    cursor = connection.cursor()
    # The below query employs nested subqueries to retrieve and format the data
    # as required by this function.
    #
    # Essentially it creates through sub-queries 2 copies of the "standings" view,
    # each containing a "row" column numbering each row (in order of wins). One
    # of these tables is then cut down to only the odd-numbered rows, and the other
    # cut down to the even-numbered rows. These are then joined, so that each
    # even-numbered player is displayed next to the player next-down in the "standings" view.
    cursor.execute("""
                    SELECT a.id,
                           a.name,
                           b.id,
                           b.name
                    FROM
                      (SELECT id,
                              name,
                              row
                       FROM
                         (SELECT id,
                                 name,
                                 ROW_NUMBER() over (ORDER BY wins DESC) AS row
                          FROM standings) AS rowified
                       WHERE row % 2 != 0) AS a,

                      (SELECT id,
                              name,
                              row
                       FROM
                         (SELECT id,
                                 name,
                                 ROW_NUMBER() over (ORDER BY wins DESC) AS row
                          FROM standings) AS rowified
                       WHERE row % 2 = 0) AS b
                    WHERE a.row = b.row -1;""")
    result=cursor.fetchall()
    connection.close
    return result

