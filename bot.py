import tweepy
import os
import dotenv
from datetime import date, timedelta

dotenv.load_dotenv()

auth_handler = tweepy.OAuthHandler(os.environ["API_KEY"], os.environ["API_SECRET_KEY"])
auth_handler.set_access_token(os.environ["ACCESS_TOKEN"], os.environ["ACCESS_TOKEN_SECRET"])

api = tweepy.API(auth_handler, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")

def tweeter(data):
    status = f'''
    Resource available : #${data['resource']}
    Available at : #${data['place']}
    Quantity available : #${data['quantity']}
    Price : #${data['price']}
    Contact : ${data['phone']}, 4{data['email']}

    #${data['place']} #${data['resource']} #sahaay
    visit sahaay.xyz for more resources
    '''
    api.update_status(status)


def retweeter():
    hashtag = "#COVIDsecondwave"
    yesterday = date.today() - timedelta(days = 1)
    tweets = tweepy.Cursor(api.search, q=hashtag, lang="en", since=yesterday, tweet_mode='extended').items(10)
    for tweet in tweets:
        tweet_id = tweet._json["id"])
        api.retweet(tweet_id)


if __name__ == "__main__":
    dummy_data = {
        "resource": "Test Resource",
        "place": "Test City",
        "quantity": "20",
        "price": "100",
        "phone": "1234567890",
        "email": "test@test.com"
    }
    # tweeter(dummy_data)
    retweeter()

