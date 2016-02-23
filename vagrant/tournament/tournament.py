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
    DB = connect();
    cursor = DB.cursor();
    cursor.execute("delete from matches");
    DB.commit();
    DB.close();


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect();
    cursor = DB.cursor();
    cursor.execute("delete from players");
    DB.commit();
    DB.close();


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect();
    cursor = DB.cursor();
    cursor.execute("select count(*) from players");
    for row in cursor.fetchall():
    	count = row[0];
    	break;
    DB.close();
    return count;

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect();
    cursor = DB.cursor();
    cursor.execute("insert into players (name) values (%s)", (name,));
    DB.commit();
    DB.close();


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
    DB = connect();
    cursor = DB.cursor();

    sql = '''
    	select m.player_id, m.name, w.wins, m.count 
    	from matches_by_player m, wins_by_player w
    	where m.player_id = w.player_id
    	order by wins desc;
    ''';
    cursor.execute(sql);
    standings = [(row[0], row[1], row[2], row[3]) for row in cursor.fetchall()];

    DB.close();
    return standings;


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect();
    cursor = DB.cursor();
    sql = '''insert into matches (winner, loser) values (%d, %d)
    	''' % (winner, loser);
    cursor.execute(sql);
    DB.commit();
    DB.close();

 
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
    standings = playerStandings();
    # [
    #    (id, name, wins, matches),
    #    (id, name, wins, matches),
    #    (id, name, wins, matches)
    # ]

    num_players = len(standings);

    # pair from the top down
    pairings = [];
    for i in range(0,num_players,2):
    	p1_name = standings[i][1];
    	p1_matches = standings[i][3];
    	p1_wins = standings[i][2];
    	p1_losses = p1_matches - p1_wins;
    	p2_name = standings[i+1][1];
    	p2_matches = standings[i+1][3];
    	p2_wins = standings[i+1][2];
    	p2_losses = p2_matches - p2_wins;
    	
    	print("match %s: %s (%s-%s) vs %s (%s-%s)" %
    		(i/2, p1_name, p1_wins, p1_losses, p2_name, p2_wins, p2_losses));
    		
    	pairings.append( (standings[i][0], standings[i][1], standings[i+1][0], standings[i+1][1]) );
    
    return pairings;
