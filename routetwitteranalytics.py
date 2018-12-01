# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 22:30:46 2018

@author: has_a
"""

import tweepy
import pdb
import collections
import json
import routetwitteranalytics as rtwitteranalytics
import savetwitterprofile as save_profile
import routetwitterapi as rtapi 
import os
import datetime
import time
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import numpy


class RouteTwitterAnalytics():
    
    sentiment = 0
    pos_keywords = ['FCS', 'FBS', 'NCAA', 'ACAA', 'highschool', 'middleschool', 'Football', 'Class', '2022', '2020', '2021', '2019']
    pos_adj = ['good']
    negative_keywords = ['Soccer', 'hockey', 'baseball', 'volleyball', 'co.uk', 'wife', 'husband', 'father', 'dad', 'Horseracing', 'Nigeria', 'erotic', 'fiction', 
                         'argue', 'Manchester', 'Liverpool', 'ebay', 'hate', 'MAGA', 'nationalist', 'redhats', 'constitutionalist', 'chanelsea_', 'slingstagram92']
    blacklist = ['MakenaMD', 'CFL_PAK', 'juscarts', 'LukePollard', 'bigtaltal', 'Ryanlugo1']
    
    def __init__(self):
        print("init RouteTwitterAnalytics")
        
        
    def send_follow_request(self, userId = None):
        rta = rtapi.RouteTwitterAPI()
        rta.send_follow_request(userId)
        
        
    def get_tweettext_analytics(self, data):
                
        stop_words = set(stopwords.words("english"))
        words = word_tokenize(data)
        filtered_sentence = []
        for w in words:
            if w not in stop_words:
                filtered_sentence.append(w)
        
        #print(sent_tokenize(data))
        #print(word_tokenize(data))
        print(filtered_sentence)
        print("\n")
        
        ## if pos self.sentiment += 0.1
        
    
    def tokenize_words(self, sentence = None):
        if sentence is not None:
            stop_words = set(stopwords.words("english"))
            words = word_tokenize(sentence)
            filtered_sentence = []
            for w in words:
                if w not in stop_words:
                    filtered_sentence.append(w)
            return filtered_sentence
        else:
            return None
        
        
    def make_array_lower(self, values = None):
        try:
            return (x.lower() for x in values)
        except:
            print("error in make array lower")
            return []
      
        
    ## analyze the description of user
    def description_analytics(self, description=None):
        sentiment = 0
        
        if description is not None:
            words = word_tokenize(description)
            for val in words:
                for x in range(len(self.pos_keywords)):
                    if val.lower() == self.pos_keywords[x].lower():
                        print("in descript:",val)
                        sentiment += 0.03
            
            for val in words:
                for y in range(len(self.negative_keywords)):
                    if val.lower() == self.negative_keywords[y].lower():
                        sentiment -= 0.03 
                        
            print("toeknized description {}".format(words))
            
        return sentiment
    
    
    def get_entities_analytics(self, jdata=None):
        try:
            print("checking entities for urls")
            if 'hudl.com' in jdata:
                print("RouteTwitterAnalytics()-->get_entities_analytics()-->ln 104")
                #pdb.set_trace()
                self.sentiment += 0.75
                
            else:
                self.sentiment -= 0.01
            print("sentiment:",self.sentiment)
            return self.sentiment
        except:
            print("error in get_entities_analytics")
            return False
        
        
    def get_user_analytics(self, data = None, place = None):
        
        send_request = False
        
        ##positive sentiment location list
        states = ["Alaska","Alabama","Arkansas","American Samoa","Arizona",
                  "California","Colorado","Connecticut",
                  "District of Columbia","Delaware",
                  "Florida",
                  "Georgia","Guam",
                  "Hawaii",
                  "Iowa","Idaho","Illinois","Indiana",
                  "Kansas","Kentucky",
                  "Louisiana",
                  "Massachusetts","Maryland","Maine","Michigan","Minnesota","Missouri","Mississippi","Montana",
                  "North Carolina","North Dakota","Nebraska","New Hampshire","New Jersey","New Mexico","Nevada","New York",
                  "Ohio","Oklahoma","Oregon",
                  "Pennsylvania","Puerto Rico","Rhode Island",
                  "South Carolina","South Dakota",
                  "Tennessee","Texas",
                  "Utah",
                  "Virginia","Virgin Islands","Vermont",
                  "Washington","Wisconsin","West Virginia","Wyoming" ,"USA",
                  "AK","AL","AR","AS","AZ",
                  "CA","CO","CT",
                  "DC","DE",
                  "FL","GA","GU",
                  "HI","IA","ID","IL","IN",
                  "KS","KY","LA",
                  "MA","MD","ME","MI","MN","MO","MS","MT",
                  "NC","ND","NE","NH","NJ","NM","NV","NY",
                  "OH","OK","OR",
                  "PA","PR","RI",
                  "SC","SD","TN","TX","UT",
                  "VA","VI","VT",
                  "WA","WI","WV","WY"
                  ]

        
        
        ##negative sentiment location list
        other_country = ['Africa', "Argentina", "Australia", 
                         'Brazil'
                         'England', 
                         'Indonesia',
                         'London', 
                         'Manchester', 'Liverpool',
                         'Nigeria',
                         'Sydney', "Scotland",
                         'United Kingdom', "UK"]
        
        
        
        location = self.tokenize_words(data["location"])
        location = self.make_array_lower(location)
        states = self.make_array_lower(states)
        other_country = self.make_array_lower(other_country)
        blklst = self.make_array_lower(self.blacklist)
        

        if (data['screen_name'] in blklst):
            print('user in black list - skipping user')
            self.sentiment = 0
            return

        ## are we following user:
        if data['lang'] == 'en':
            self.sentiment += 0.02
        elif data['lang'] == 'es':
            self.sentiment += 0.01
        else:
            self.sentiment -= 0.05
            
        print('calculating add user sentiment:{')
        if data['following'] is True:
            self.sentiment += 0.1
            print('following',self.sentiment)
            
            
        if data["followers_count"] > 1000:
            self.sentiment += 0.075
            print('in followers count:',self.sentiment)
        elif data["followers_count"] > 300:
            self.sentiment += 0.03
            print('in followers count:',self.sentiment)
            
        if location is not None:
            print("location is not None assesing sentiment value")
            print(location)
            print(states)
            if list(set(location) & set(states)):
                self.sentiment += 0.09
                print('location:',self.sentiment, data["location"] )
            
            if list(set(location) & set(other_country)):
                self.sentiment -= 0.12
                print('location:',self.sentiment, data["location"] )


          
        if data["verified"] is True:
            self.sentiment += 0.05
            print('acct verified',self.sentiment)  
            
            
            
        if data['description'] is not None:   
            self.sentiment = self.sentiment + self.description_analytics(data['description'])
        
          
        ##check ur
        if data["url"] is not None:
            if len(data["url"]) > 0:
                if 'hudl.com' in data["url"]:
                    self.sentiment += 0.2
                    ### hudl.com user - store in db without checking user sentiments
                    print("send a request")  ## no longer required to cehck sentiment to send friend request
                    self.send_follow_request(data["id_str"])
                    self.sentiment = 0 
                    print("saving the profile - writting to the DB")
                    sp = save_profile.RouteTwitterDB()
                    sp.write_profile_toDB(data, place)

                    return
                if 'co.uk' in data["url"]:
                    self.sentiment -= 0.075
                    
                    
        print("sentiment: ",self.sentiment)   
        if self.sentiment > 0.13 and data['follow_request_sent'] is None: 
            send_request = True
            print("send a request")
            self.send_follow_request(data["id_str"])
            
        ## reset the sentiment value    
        self.sentiment = 0 
            
            
            
        
        