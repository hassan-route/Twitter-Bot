# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 00:48:17 2018

@author: has_a
"""

import tweepy
import pdb
import collections
from flask import jsonify
import json
import routetwitteranalytics as rtwitteranalytics
import os
import datetime
import time
import mysql.connector as mariadb
from colorama import Fore, Back, Style


class RouteTwitterParse():
        
    key_accounts = ['@QBHitList', '@NxtLevelAtx', '@PlayBookAthlete']
    key_hashtags = ['#WHYIGRIND']
    key_words = ['i got accepted', 'season', 'highlights' ]
    numberOfTweets = 10
    searchterms = ["football", "highschool football", "college football"]

    
    rta = rtwitteranalytics.RouteTwitterAnalytics()
    
    
    
    if os.environ.get("HOST") is None:
        import environ as ES
        os.environ["HOST"] = ES.environ.getOSValues()["HOST"]
        os.environ["DB_NAME"] = ES.environ.getOSValues()["DB_NAME"]
        os.environ["DB_USERNAME"] = ES.environ.getOSValues()["DB_USERNAME"]
        os.environ["DB_PASSWORD"] = ES.environ.getOSValues()["DB_PASSWORD"]
    
    def __init__(self):
        print("init Route Twitter Parser")
        
        
    def is_tweet_likable(self):
        ##analyze tweet to check if it fits criteria to like
        ##TODO:
        return False
    
    def is_tweet_retweetable(self):
        ##analyze tweet to check if it fits criteria to retweet
        ##TODO:
        return False
    
    
    
    def parse_tweet(self, data=None):
        if data is not None:
            jdata = json.loads(data)
            print(jdata)
            self.get_account_info(jdata)
    
    
    
    def parse_entities(self, jdata=None):
        print('\nentities:{')
        print(jdata['entities']) 
        for data in jdata['entities']:
            #print('{}:{}'.format(data, jdata['entities'][data]))
            if len(jdata['entities'][data]) > 0:
                for x in range(len(jdata['entities'][data])):
                    #print(jdata['entities'][data][x])
                    for vals in jdata['entities'][data][x]:
                        print('{}:{}:{}'.format(data,vals, jdata['entities'][data][x][vals]))  
                        if data == 'urls':
                            self.rta.get_entities_analytics(jdata['entities']['urls'][x][vals])
        print('}end of entities\n')
            
            
    def parse_user(self, jdata):
        print('\nuser:')
        for user in jdata['user']:
            print('{} = {}'.format(str(user),jdata['user'][str(user)]))
        ##check if user data has highschool footbal related info 
        ## check is hudl is a link in bio
        print('end user\n')
        
        
        ##pass the user to be analyzed
        self.rta.get_user_analytics(jdata['user'])
        
        
    
    
    def get_account_info(self, jdata=None):

            print('\ntweet id = {}'.format(jdata['id']))
            ## need to handle retweets with recursive
            print('retweeted =  {}'.format(jdata['retweeted']) )
            if jdata['retweeted']:
                print('paser the retweeted data recursively \n')
                print('tweet = {} \n'.format(jdata['tweet']))
                for data in jdata['tweet']:
                    print('{} = {}'.format(data,jdata[data]))


            
            ##read user data
            self.parse_user(jdata)
               
            
            
            ##this works now analyze and save accordinly 
            self.parse_entities(jdata)


        
        
            ##this works now analyze and save accordinly
            print('\nplace = {} \n'.format(jdata['place'])) 
            if  jdata['place'] is not None:
                for data in jdata['place']:
                    print("{}:{}".format(data,jdata['place'][data]))


            ## requires deeper parsing
            print("truncated = ",jdata['truncated'])
            if jdata['truncated']:
                print("extended tweet")
                print('extended tweet = {}'.format(jdata['extended_tweet']))
                for etdata in jdata['extended_tweet']:
                    print("{}:{}".format(etdata,jdata['extended_tweet'][etdata]))
                print("end extended tweet")
                

            
            #quote is true
            if 'is_quote_status' in jdata and jdata['is_quote_status']:
                print("start quote_status{")
                print('is_quote_status = {}'.format(jdata['is_quote_status']))
                for quotes in jdata['quoted_status']:
                    if quotes is "user":
                        self.parse_user(jdata['quoted_status'])
                    elif quotes is "entities":
                        self.parse_entities(jdata['quoted_status'])
                    else:
                        print("{}:{}".format(quotes,jdata['quoted_status'][quotes]))
  
                print("}end quote_status\n")
                     
            if 'quote_count' in jdata:
                print('quote_count = {}'.format(jdata['quote_count']))
                
            
            if 'quoted_status_permalink' in jdata:
                for permalink in jdata['quoted_status_permalink']:
                    print(permalink)
    
            if 'tweet' in jdata:
                print("tweet tags true:{")
                for tweet in jdata['tweet']:
                    print(":",tweet)
                    for data in jdata['tweet'][tweet]:
                        print(data)

            ## handle actual tweet text
            if 'text' in jdata:
                print('\ntweet text = {}\n'.format(jdata['text']))
                self.rta.get_tweettext_analytics(jdata['text'])
                
            #pdb.set_trace()
            
        
    
 
        
        
        
        
        
        
    
    