import tweepy
import os
import dotenv
from datetime import date, timedelta
import random, requests, time, json
import env

dotenv.load_dotenv()

auth_handler = tweepy.OAuthHandler(env.API_KEY, env.API_SECRET_KEY)
auth_handler.set_access_token(env.ACCESS_TOKEN, env.ACCESS_TOKEN_SECRET)
headers = {
    "Authorization": f"Bearer {env.BEARER_TOKEN}"
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
    untweeted = []
    with open(os.path.join(os.path.expanduser('~/Sahaay-Bot'), 'states.json')) as json_file:
        states = json.load(json_file)["states"]
    status = ""
    for place in data:
        for resource in data[place]:
            for resource_id in data[place][resource]:
                details = data[place][resource][resource_id]
                state = "" 
                for state_data in states:
                    for district in state_data["districts"]:
                        if district.lower() == place.lower():
                            state = state_data["state"]
                            break
                    if state != "":
                        break
                if state != "":
                    status = f'''
Verification Status: {details['isVerified']}
Resource available : #{resource.capitalize()}
Available at : #{place.capitalize().replace(' ', '_')}, #{state.replace(' ', '_')}
Name : {details['name']}
Contact : {details['phone']}

#{place.capitalize()} #{state} #{resource.capitalize()} #sahaay
visit https://sahaay.xyz for more resources'''
                    pass
                else:
                    status = f'''
Verification Status: {details['isVerified']}
Resource available : #{resource.capitalize()}
Available at : #{place.capitalize()}
Name : {details['name']}
Contact : {details['phone']}

#{place.capitalize()} #{resource.capitalize()} #sahaay
visit https://sahaay.xyz for more resources'''
                    pass
                # print(status)
                try:
                    api.update_status(status)
                    print("New tweet : ", resource.capitalize(), " at ", place.capitalize())
                except:
                    print("Twitter kai ozhinju makkale !")
                    untweeted.append(resource_id)
                time.sleep(60)
    print("Bot termination: ", len(untweeted), " tweets failed !")
    with open(os.path.join(os.path.expanduser('~/Sahaay-Bot'), 'untweeted.txt')) as text_file:
        text_file.write(untweeted)


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
