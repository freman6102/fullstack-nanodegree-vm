#
# Database access functions for the web forum.
# 

import time
import psycopg2 
import bleach

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.    

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    #posts = [{'content': str(row[1]), 'time': str(row[0])} for row in DB]
    #posts.sort(key=lambda row: row['time'], reverse=True)
    
    ## Database connection
    DB = psycopg2.connect("dbname=forum")

    cursor = DB.cursor();
    cursor.execute("select content, time from posts order by time desc");
    posts = [{'content' : row[0], 'time' : row[1]} for row in cursor.fetchall()];
    
    # close DB connection
    DB.close();

    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
#    t = time.strftime('%c', time.localtime())
#    DB.append((t, content))

    ## Database connection
    DB = psycopg2.connect("dbname=forum")
    
    cursor = DB.cursor();
    
    # use bleach to prevent Script-injection attacks
    content = bleach.clean(content);
    # use tuple parameters to prevent SQL-injection attacks
    cursor.execute("insert into posts values (%s)", (content,)); 
    DB.commit();    

    # close DB connection
    DB.close();
