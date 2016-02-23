\c vagrant
drop database if exists tournament;
create database tournament;
\c tournament

-- optionally, I could just drop the tables, assuming the db exists
-- drop table if exists matches;
-- drop table if exists players;

create table players(
  player_id serial primary key,
  name text
  );
  
create table matches(
  match_id serial primary key,
  winner int references players (player_id),
  loser int references players (player_id)
  );

create view wins_by_player as
    select players.player_id, count(matches.match_id) as wins
      from players left join matches
        on players.player_id = matches.winner
      group by players.player_id
      order by wins desc;

create view matches_by_player as
    select players.player_id, players.name, count(matches.match_id) 
      from players left join matches
        on players.player_id = matches.winner or players.player_id = matches.loser
      group by players.player_id;
  

-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


