import tweepy
import os
import dotenv
from datetime import date, timedelta
import random, requests, time

dotenv.load_dotenv()

auth_handler = tweepy.OAuthHandler(os.environ['API_KEY'], os.environ['API_SECRET_KEY'])
auth_handler.set_access_token(os.environ['ACCESS_TOKEN'], os.environ['ACCESS_TOKEN_SECRET'])
headers = {
    "Authorization": f"Bearer {os.environ['BEARER_TOKEN']}"
    }
api = tweepy.API(auth_handler, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
try:
    api.verify_credentials()
    print('Authentication OK')
except:
    print('Error during authentication')

def sahaay_tweeter(data):
    status = f'''
    Resource available : #{data['resource']}
    Available at : #{data['place']}
    Quantity available : #{data['quantity']}
    Price : #{data['price']}
    Contact : {data['phone']}

    #{data['place']} #{data['resource']} #sahaay
    visit https://sahaay.xyz for more resources
    '''
    api.update_status(status)

def data_tweeter(data):
    for place in data:
        for resource in data[place]:
            for resource_id in data[place][resource]:
                details = data[place][resource][resource_id]
                status = f'''
Resource available : #{resource.capitalize()}
Available at : #{place.capitalize()}
Contact : {details['phone']}
Verification Status: {details['isVerified']}

#{place.capitalize()} #{resource.capitalize()} #sahaay
visit https://sahaay.xyz for more resources
                '''
                # print(status)
                try:
                    api.update_status(status)
                except:
                    print("Twitter kai ozhinju makkale !")
                time.sleep(20)


def retweeter():
    resources = ["oxygen", "icu", "(bed OR beds)", "(ambulance OR ambulances)", "(food OR foods OR tiffin OR tiffins)", "favipiravir", "tocilizumab", "plasma", "(ventilator OR ventilators)", "fabiflu", "remdesivir", "(test OR tests OR testing)", "(ambulance OR ambulances)"]
    cities = ['Delhi', 'Noida', 'Gurgaon', 'Bangalore', 'Hyderabad', 'Chennai', 'Mumbai']
    city = cities[random.randint(0, len(cities) - 1)]
    resource = resources[random.randint(0, len(resources) - 1)]
    hashtag = f"""verified {city} {resource} -any - requirement - requirements - requires - require - required - request - requests - requesting - needed - needs - need - seeking - seek - not verified - notverified - looking - unverified - urgent - urgently - urgently required - sending - send - help - dm - get - year - old - male - female - saturation -is:reply -is:retweet -is:quote&max_results=20&tweet.fields=created_at,public_metrics&expansions=author_id"""
    yesterday = date.today() - timedelta(days = 1)
    print(hashtag, yesterday)

    try:
        tweets = requests.get(f"https://api.twitter.com/2/tweets/search/recent?query={hashtag}", headers=headers).json()
        for tweet in tweets['data']:
            for key in tweet.keys():
                api.retweet(tweet['id'])
                time.sleep(20)
    except tweepy.TweepError as e:
        print(e)



def main():
    dummy_data = {
        "resource": "Test Resource",
        "place": "Test City",
        "quantity": "20",
        "price": "100",
        "phone": "1234567890",
        "email": "test@test.co",
    }
    # tweeter(dummy_data)
    retweeter()
