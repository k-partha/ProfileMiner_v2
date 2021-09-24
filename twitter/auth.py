import tweepy
import parameters as p

def auth(index):

    auth = tweepy.OAuthHandler(p.keys[index]['consumer_key'], p.keys[index]['consumer_secret'])
    auth.set_access_token(p.keys[index]['access_token_key'], p.keys[index]['access_token_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    return p.keys[index], api

if __name__ == "__main__":
    pass