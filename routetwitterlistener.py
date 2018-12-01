# -*- coding: utf-8 -*-
"""
Created on Thu Nov 22 11:59:31 2018

@author: has_a
"""

##Route Twitter listener/scanner
import tweepy
import pdb
import routetwitterparse as rtwitterparse
import os
import time
import datetime

consumer_key = '6n8WP546sOXc5BSyUBQIAoeGI'
consumer_secret = '1d04V7XCPZ3omQsozvqogqO5N178mSP71sINSB8yFyRASKxMog'
access_token = '937096171180515329-1EBWoA4yBpzigeNgEP8ecJ0fKSuEXcm'
access_token_secret = '1lrniV3o3zzARj20QHZPouXYAUi6ZPlduBLud2BR010d0'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


searchterms = ["football", "highschool football", "college football", "NCAA", "hudl", 'FBS', 'FCS']


def call_listner():
    twitterStream = tweepy.Stream(auth, listener())
    twitterStream.filter(track=searchterms)


class listener(tweepy.streaming.StreamListener):
    
    
    pausetime = 90    
    rtp = rtwitterparse.RouteTwitterParse()
            
    
    def __init__(self):
        print("route twitter listener")
        
    def on_data(self, data):
        try:
            print("\ngot data at {}".format(datetime.datetime.now()))
            self.rtp.parse_tweet(data)
            time.sleep(self.pausetime)
        except:
            print("ERROR")
            time.sleep(self.pausetime)
            call_listner()
        
        
        
    def on_error(self, status):
        print(status)
        print("\n restarting listner... \n")
        try:
            call_listner()
        
        except:
            print('busted')
        
    
    
    
call_listner()
#twitterStream = tweepy.Stream(auth, listener())
#twitterStream.filter(track=searchterms)