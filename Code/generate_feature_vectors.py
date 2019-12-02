import json
import botometer
import pickle
import numpy as np

user_len_screen_name={}
user_longevity={} 
user_friends={} 
user_followers={} 
user_tweets={} 
user_fav={} 
user_total_retweets_received={} 
user_total_fav_received={} 

user_features={}

screen_names=[]
def main():
    rapidapi_key = "XXXXXXXXXXXXXXXXXX" # now it's called rapidapi key
    twitter_app_auth = {
        'consumer_key': 'XXXXXXXXXXXXXXXXXX',
        'consumer_secret': 'XXXXXXXXXXXXXXXXXX',
        'access_token': 'XXXXXXXXXXXXXXXXXX',
        'access_token_secret': 'XXXXXXXXXXXXXXXXXX',
      }
    
    bom = botometer.Botometer(wait_on_ratelimit=True,
                              rapidapi_key=rapidapi_key,
                              **twitter_app_auth)

    with open('data-4.json') as json_file:
        line=json_file.readline()
        cnt=0
        maximum=0
        while line: 
            data=json.loads(line)

            if getScreenName(data) not in screen_names:
                screen_names.append(getScreenName(data))

            if getScreenName(data) not in user_total_retweets_received:
                user_total_retweets_received[getScreenName(data)]=getRetweets(data)
                user_total_fav_received[getScreenName(data)]=getFavoritesforTweet(data)
            else:
                user_total_retweets_received[getScreenName(data)]=user_total_retweets_received[getScreenName(data)]+getRetweets(data)
                user_total_fav_received[getScreenName(data)]=user_total_fav_received[getScreenName(data)]+getFavoritesforTweet(data)
                                                
            user_followers[getScreenName(data)]=getFollowersCount(data)
            user_friends[getScreenName(data)]=getFriendsCount(data)
            user_longevity[getScreenName(data)]=getLongevityofAccount(data)
            user_tweets[getScreenName(data)]=getNumofTweets(data)
            user_fav[getScreenName(data)]=getNumofFavs(data)
            user_len_screen_name[getScreenName(data)]=len(getScreenName(data))
	
            line=json_file.readline()
            cnt=cnt+1

        f = open("data/user_len_screen_name.pickle", "wb")
        pickle.dump(user_len_screen_name,f)

        f = open("data/screen_name.pickle", "wb")
        pickle.dump(screen_names,f)

        f = open("data/user_longevity.pickle", "wb")
        pickle.dump(user_longevity,f)

        f = open("data/user_friends.pickle", "wb")
        pickle.dump(user_friends,f)

        f = open("data/user_followers.pickle", "wb")
        pickle.dump(user_followers,f)

        f = open("data/user_tweets.pickle", "wb")
        pickle.dump(user_tweets,f)

        f = open("data/user_fav.pickle", "wb")
        pickle.dump(user_fav,f)

        f = open("data/user_total_retweets_received.pickle", "wb")
        pickle.dump(user_total_retweets_received,f)

        f = open("data/user_total_fav_received.pickle", "wb")
        pickle.dump(user_total_fav_received,f)
        print(cnt)

        f_vec=generate_feature_vectors_for_all_users()
        print(f_vec.shape)

        f=open('data/f_vec.pickle','wb')
        pickle.dump(f_vec,f)

def generate_feature_vectors_for_all_users():
    """
    returns feature vector for a user id: Has the following format

    | len_screen_name | longevity | friends | followers | frnd-follower ratio | # tweets | # of tweets per day | total retweets received | total favorited | total favorites received
    """
    fv=[]
    for user in user_followers.keys():
        ls=[]
        ls.append(user_len_screen_name.get(user))
        ls.append(user_longevity.get(user))
        ls.append(user_friends.get(user))
        ls.append(user_followers.get(user))
        ls.append(user_friends.get(user)/(user_followers.get(user)+1))
        ls.append(user_tweets.get(user))
        ls.append(user_tweets.get(user)/(user_longevity.get(user)*365))
        ls.append(user_total_retweets_received.get(user))
        ls.append(user_fav.get(user))
        ls.append(user_total_fav_received.get(user))
        fv.append(ls)
        user_features[user]=ls

    f=open('data/user_features.pickle','wb')
    pickle.dump(user_features,f)

    return np.array(fv)    

def botOrNot(screen_name,bom):    
    result=bom.check_account(screen_name)
    total=0
    for v in result['display_scores']:
        total=total+result['display_scores'][v]

    avg=total/8

    if avg >=3.5:
        return 1
    else:
        return 0    

def getTweetTime(data):
    tweet_time=data['created_at'].split(" ")
    return int(tweet_time[len(tweet_time)-1])

def getRetweeterCreationTime(data):
    c_time=data['user']['created_at'].split(" ")
    return int(c_time[len(c_time)-1])

def getCreationTime(data):
    try:
        c_time=data['retweeted_status']['user']['created_at'].split(" ")
        return int(c_time[len(c_time)-1])
    except:
        c_time=data['user']['created_at'].split(" ")
        return int(c_time[len(c_time)-1])

def getFavoritesforTweet(data):
    try:
        return int(data['retweeted_status']['favorite_count'])
    except:
        return int(data['favorite_count'])    

def getFullText(data):
    return data['retweeted_status']['full_text']

def getRetweets(data):
    try:
        return int(data['retweeted_status']['retweet_count'])
    
    except Exception as e:
        return 0

def getFollowersCount(data):
    try:
        return int(data['retweeted_status']['user']['followers_count'])
    except:
        return data['user']['followers_count']

def getFriendsCount(data):
    try:
        return int(data['retweeted_status']['user']['friends_count'])
    except:
        return int(data['user']['friends_count'])

def getScreenName(data):
    try:
        return data['retweeted_status']['user']['screen_name']

    except Exception as e:
        return getRetweeterName(data)

def getRetweeterName(data):
    return data['user']['screen_name']

def getNumofTweets(data):
    try:
        return int(data['retweeted_status']['user']['statuses_count'])
    except:
        return int(data['user']['statuses_count'])

def getNumofFavs(data):
    try:
        return int(data['retweeted_status']['user']['favourites_count'])
    except:
        return int(data['user']['favourites_count'])        

def getLongevityofAccount(data):
    return int(2019-getCreationTime(data))+1    

if __name__ == '__main__':
    main()
