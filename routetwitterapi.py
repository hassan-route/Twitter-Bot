import tweepy
import pdb
import collections
from flask import jsonify
import os
import datetime
import time




consumer_key = '6n8WP546sOXc5BSyUBQIAoeGI'
consumer_secret = '1d04V7XCPZ3omQsozvqogqO5N178mSP71sINSB8yFyRASKxMog'
access_token = '937096171180515329-1EBWoA4yBpzigeNgEP8ecJ0fKSuEXcm'
access_token_secret = '1lrniV3o3zzARj20QHZPouXYAUi6ZPlduBLud2BR010d0'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


numberOfTweets = 10


class RouteTwitterAPI():
    

        
    user = api.me()
    def __init__(self):
        
        print(self.user.name)
        print(self.user.location)
        
        
        
    def get_home_timeline(self):
        timeline = []
        for status in (tweepy.Cursor(api.home_timeline).items(10)):  
            tcol = collections.OrderedDict()
            try:
                #pdb.set_trace()
                tcol['timeline'] = status._json
                """
                tcol['text']= status._json['text']
                tcol['retweeted']= status._json['retweeted']
                tcol['retweet_count']= status._json['retweet_count']
                tcol['screen_name']= status._json['screen_name']
                tcol['name']= status._json['name']"""
                
            except tweepy.TweepError as e:
                print(e.reason)
            except StopIteration:
                break
            finally:
                pass

            timeline.append(tcol)   
        return jsonify(timeline)
    
    
    
        
    def get_timeline(self):
        x = 0
        timeline = []
        for x, status in enumerate(tweepy.Cursor(api.user_timeline).items(3)):  
            tcol = collections.OrderedDict()
            print(x)
            if x<3:  ## only check the first 3 tweets
                try:
                    tcol['text']= status._json['text']
                    tcol['retweeted']= status._json['retweeted']
                    tcol['retweet_count']= status._json['retweet_count']
                except tweepy.TweepError as e:
                    print(e.reason)
                except StopIteration:
                    break
                finally:
                    pass
            else:
                print(tcol)
                break
            timeline.append(tcol)
        pdb.set_trace()    
        return jsonify(timeline)
    
    
    ##not working
    def get_statuses_timeline(self):
        x = 0
        timeline = []
        
        for status in tweepy.Cursor(api.statuses_lookup, id='402771404').items():  
            tcol = collections.OrderedDict()
            print(x)
            pdb.set_trace()
            if x<3:  ## only check the first 3 tweets
                try:
                    tcol['text']= status._json['text']
                    tcol['retweeted']= status._json['retweeted']
                    tcol['retweet_count']= status._json['retweet_count']
                except tweepy.TweepError as e:
                    print(e.reason)
                except StopIteration:
                    break
                finally:
                    pass
            else:
                print(tcol)
                break
            timeline.append(tcol)
            x +=x
        pdb.set_trace()    
        return jsonify(timeline)
    
    
    
    def get_user(self, id = None):
        tcol = collections.OrderedDict()
        tcol[id] = api.get_user(id)._json

        return jsonify(tcol)
    
    
    
    def get_rate_limits(self):
        tcol = collections.OrderedDict()
        tcol['rate_limit'] = api.rate_limit_status()
        
        return jsonify(tcol)
        
        
    
    def get_summary(self):
        tcol = collections.OrderedDict()
        #tcol['rate_limit'] = api.rate_limit_status()
        tcol['user'] = self.user.name
        tcol['followers_count'] = self.user.followers_count
        tcol['following'] = self.user.followers_ids()
        tcol['friends_count'] = self.user.friends_count
        tcol['friends'] = api.friends_ids()
        tcol['tweets_favourited'] = self.user.favourites_count
        tcol['public_list'] = self.user.listed_count
        tcol['tweets'] = self.user.statuses_count
        return jsonify(tcol)
        
        
        
    def get_follower_list(self):
        x=0
        tcol = collections.OrderedDict()
        for follower in (tweepy.Cursor(api.followers).items()):  
            print("follower item number: {} \n",x) 
            x += x
            try:
                tcol[follower._json["screen_name"]]= follower._json
            except tweepy.TweepError as e:
                print(e.reason)
            except StopIteration:
                break
            finally:
                print(tcol)

            time.sleep(10)
 
        ## diplay the account info of the requester  
        tcol['user'] = self.user.name
        tcol[self.user.name +'_followers'] = self.user.followers_count
        tcol[self.user.name + '_following'] = self.user.friends_count
        tcol[self.user.name + '_tweets_favourited'] = self.user.favourites_count
        tcol[self.user.name + '_public_list'] = self.user.listed_count
        tcol[self.user.name + '_tweets'] = self.user.statuses_count
        jtcol =jsonify(tcol)          
        return jtcol
    
        
    
    def get_follower_list_ids(self):
        x = 0
        tcol = collections.OrderedDict()
        ids = []
        for follower in tweepy.Cursor(api.followers_ids).pages():  
            #pdb.set_trace()
            try:
                #tcol[follower._json["screen_name"]]= follower._json
                print(follower)
                ids.extend(follower)
                ##print(ids.count(self))
            except tweepy.TweepError as e:
                print(e.reason)
            except StopIteration:
                break
            finally:
                print(ids)
                print (len(follower))

            time.sleep(60)
           
        ## diplay the account info of the requester  
        tcol['user'] = self.user.name
        tcol[self.user.name +'_followers'] = self.user.followers_count
        tcol[self.user.name + '_following'] = self.user.friends_count
        tcol[self.user.name + '_tweets_favourited'] = self.user.favourites_count
        tcol[self.user.name + '_public_list'] = self.user.listed_count
        tcol[self.user.name + '_tweets'] = self.user.statuses_count
        tcol['ids'] = ids
        jtcol =jsonify(tcol)          
        return jtcol
    
    
    def get_friend_list(self):
        x = 0
        tcol = collections.OrderedDict()
        for x, follower in enumerate(tweepy.Cursor(api.friends).items()):  
            print(x)
            if x<3:  ## only check the first 3 tweets
                try:
                    tcol[follower._json["screen_name"]]= follower._json
                except tweepy.TweepError as e:
                    print(e.reason)
                except StopIteration:
                    break
                finally:
                    pass
                    #print(tcol)
            else:
                print(tcol)
                break
            
        tcol['user'] = self.user.name
        tcol['following'] = self.user.followers_count
        tcol['followers'] = self.user.friends_count
        tcol['tweets_favourited'] = self.user.favourites_count
        tcol['public_list'] = self.user.listed_count
        tcol['tweets'] = self.user.statuses_count
                
        jtcol =jsonify(tcol)          
        return jtcol
        
        
        
    def followBack_followers(self):            
        for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
            try:
                #Follow
                tweet.user.follow()
                print('Followed the user')
                
            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break
      
        
    ##send a friend request
    def send_follow_request(self, twitter_id):            
        try:
            #Follow
            api.create_friendship(twitter_id)
            print('Followed the user')
            
        except tweepy.TweepError as e:
            print(e.reason)


            
            
    def replyto_tweets(self):
        for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
            try:
                #Reply
                print('\nTweet by: @' + tweet.user.screen_name)
                print('ID: @' + str(tweet.user.id))
                tweetId = tweet.user.id
                username = tweet.user.screen_name
                api.update_status("@" + username + " " + phrase, in_reply_to_status_id = tweetId)
                print ("Replied with " + phrase)
                
            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break
            
            
    def retweet(self):
        for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
            try:
                #Retweet
                tweet.retweet()
                print('Retweeted the tweet')   

            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break
        
        
    def favorite_tweet(self):
        for tweet in tweepy.Cursor(api.search, search).items(numberOfTweets):
            try:
                #Favorite
                tweet.favorite()
                print('Favorited the tweet')   

            except tweepy.TweepError as e:
                print(e.reason)

            except StopIteration:
                break
            
            
            
    ## check if we are following all the coaches in our database
    def arewe_following_coach(self):
        return None
        for tweet in tweepy.Cursor(api.search, coach_name).items(5):
            pass
        
            
            

        




