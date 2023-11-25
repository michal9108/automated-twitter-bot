import tweepy
import mysql.connector
import random
import dotenv 
import os

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
bearer_token = os.environ.get("BEARER_TOKEN")


dotenv.load_dotenv()

mysql_host = os.environ.get("MYSQL_HOST")
mysql_user = os.environ.get("MYSQL_USER")
mysql_password = os.environ.get("MYSQL_PASSWORD")
mysql_database = os.environ.get("MYSQL_DATABASE")


# Connect to MySQL using environment variables
db = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database
)

# Authenticate to Twitter
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# Fetch a random quote from the MySQL database
cursor = db.cursor(dictionary=True)
cursor.execute("SELECT * FROM quotes ORDER BY RAND() LIMIT 1")
quote_data = cursor.fetchone()

if quote_data:
    next_tweet = quote_data['quote']

    # Check if the tweet has already been sent
    cursor.execute("SELECT * FROM sent_tweets WHERE tweet=%s", (next_tweet,))
    existing_tweet = cursor.fetchone()

    if not existing_tweet:
        # Post tweet through Twitter API
        client.create_tweet(text=next_tweet)

        # Insert the sent tweet into the 'sent_tweets' table
        cursor.execute("INSERT INTO sent_tweets (tweet) VALUES (%s)", (next_tweet,))
        db.commit()

        print("Tweet posted successfully.")
    else:
        print("The same tweet has already been sent.")
else:
    print("No quotes found in the database.")

# Close MySQL connection
cursor.close()
db.close()



