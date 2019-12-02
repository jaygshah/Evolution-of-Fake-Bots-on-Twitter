import json
import botometer
import pickle

def main():
    rapidapi_key = "XXXXXXXXXXXXXXXXXX" 
    twitter_app_auth = {
        'consumer_key': 'XXXXXXXXXXXXXXXXXX',
        'consumer_secret': 'XXXXXXXXXXXXXXXXXX',
        'access_token': 'XXXXXXXXXXXXXXXXXX',
        'access_token_secret': 'XXXXXXXXXXXXXXXXXX',
      }
    
    bom = botometer.Botometer(wait_on_ratelimit=True,
                              rapidapi_key=rapidapi_key,
                              **twitter_app_auth)

    user_labels={}
    
    f=open('data/screen_name.pickle','rb')
    screen_names=pickle.load(f)

    #### Uncomment this and run this file once
    #### Then comment the following three lines to
    #### fetch the data 
    # f2=open('data/user_labels.pickle','wb')
    # pickle.dump(user_labels,f2)
    # exit(0)
    
    f3=open('data/user_labels.pickle','rb')
    user_labels=pickle.load(f3)
    cnt=len(user_labels.keys())

    try:
        for name in screen_names:
            if name not in user_labels.keys():        
                user_labels[name]=botOrNot(screen_name=name,bom=bom)
                cnt=cnt+1
                print(user_labels[name])
                print(f'{cnt}/{len(screen_names)} done...')    

    except Exception:
        f4=open('data/user_labels.pickle','wb')
        pickle.dump(user_labels,f4)
        # exit(0)

    f = open("data/user_labels.pickle", "wb")
    pickle.dump(user_labels,f)

def botOrNot(screen_name,bom):
    try:    
        result=bom.check_account(screen_name)
        total=0
        for v in result['display_scores']:
            total=total+result['display_scores'][v]

        avg=total/8
        if avg >=2.5:
            return 1
        else:
            return 0

    except Exception as e:
        print(e)
        return 1
                
def getScreenName(data):
    try:
        return data['retweeted_status']['user']['screen_name']

    except Exception as e:
        return getRetweeterName(data)            

def getRetweeterName(data):
    return data['user']['screen_name']

if __name__ == '__main__':
    main()