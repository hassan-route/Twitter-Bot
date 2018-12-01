# -*- coding: utf-8 -*-
"""
Created on Sat Nov 24 17:36:24 2018

@author: has_a
"""

import datetime
##route helper class
import os
import logging
import pdb
import mysql.connector as mariadb
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import re


#get OS values on windows localhost

if os.environ.get("HOST") is None:
    import environ as ES
    os.environ["HOST"] = ES.environ.getOSValues()["HOST"]
    os.environ["DB_NAME"] = ES.environ.getOSValues()["DB_NAME"]
    os.environ["DB_USERNAME"] = ES.environ.getOSValues()["DB_USERNAME"]
    os.environ["DB_PASSWORD"] = ES.environ.getOSValues()["DB_PASSWORD"]

class RouteTwitterDB():
    
    
    cnx = mariadb.connect(user=os.environ["DB_USERNAME"], password=os.environ["DB_PASSWORD"], database=os.environ["DB_NAME"], host=os.environ["HOST"])
    cnx.get_warnings = True
    cnx.autocommit = True
    

    
    ## write values to athlete_bio table field - overall_rating
    def write_profile_toDB(self, results=None, place=None):
        print("inside write_profile_toDB, input:{}\n\n".format(results))
        #tablevals = ['id','twitter_id','verified','screen_name','name','description','following','friends_count','followers_count','follow_request_sent','location','url','geo_enabled','created_at_twitter','created_at']
        self.cnx.autocommit = True
        cursor = self.cnx.cursor()
        location = None
        if results['location'] is None:
            location = results['location']
        if place is not None:
           location = place['full_name']   ## full name of location stored in place
           location = re.sub(r'[^\w]', ' ',location)
           
           
        stop_words = set(stopwords.words("english"))
        words = word_tokenize(results['description'])
        filtered_sentence = []
        for w in words:
            if w not in stop_words:
                filtered_sentence.append(w)
                
        description = re.sub(r'[^\w]', ' ',results['description'])
        name = re.sub(r'[^\w]', ' ',results['name'])


        query = ("""INSERT INTO twitter_base 
                 (twitter_id, verified, screen_name,name, description, isfriend, following, friends_count, followers_count,
                 follow_request_sent, location, url, geo_enabled, created_at_twitter, created_at)
                 VALUES ({},'{}','{}','{}','{}','{}','{}',{},{},'{}','{}','{}','{}','{}','{}') 
                 ON DUPLICATE KEY UPDATE 
                 verified='{}', screen_name='{}',name='{}', description='{}', isfriend='{}', following='{}', 
                 friends_count='{}', followers_count='{}',
                 follow_request_sent='{}', location='{}', url='{}', geo_enabled='{}', created_at_twitter='{}'
                 """.format(results['id'],
                 results['verified'],results['screen_name'],name,description,results['following'],
                 results['following'],results['friends_count'],results['followers_count'],results['follow_request_sent'],
                 location, results['url'],results['geo_enabled'],datetime.datetime.now(),datetime.datetime.now(),
                 results['verified'],results['screen_name'],name,description,results['following'],
                 results['following'],results['friends_count'],results['followers_count'],results['follow_request_sent'],
                 location, results['url'],results['geo_enabled'],results['created_at']
                ))  
        

        
        print(query)
        cursor.execute(query)
        self.cnx.commit()
        return True
    


####testing block
# =============================================================================
# results = {'id': 2265431520, 'id_str': '2265431520', 'name': 'B. UlmerJr', 'screen_name': '_highestpoint', 'location': 'Decatur, GA', 'url': 'http://www.hudl.com/v/2AJfrv', 
#            'description': 'Official Recruiting Page Of Bryant Ulmer Jr Class of 2019 WR/S Southwest Dekalb Football | 6’1 175 #TRUE19', 
#            'translator_type': 'none', 'protected': False, 'verified': False, 'followers_count': 219, 'friends_count': 279, 
#            'listed_count': 0, 'favourites_count': 163, 'statuses_count': 126, 'created_at': 'Sat Dec 28 05:54:04 +0000 2013', 
#            'utc_offset': None, 'time_zone': None, 'geo_enabled': True, 'lang': 'en', 'contributors_enabled': False, 
#            'is_translator': False, 'profile_background_color': 'C0DEED', 
#            'profile_background_image_url': 'http://abs.twimg.com/images/themes/theme1/bg.png', 
#            'profile_background_image_url_https': 'https://abs.twimg.com/images/themes/theme1/bg.png', 
#            'profile_background_tile': False, 'profile_link_color': '1DA1F2', 'profile_sidebar_border_color': 'C0DEED', 
#            'profile_sidebar_fill_color': 'DDEEF6', 'profile_text_color': '333333', 'profile_use_background_image': True, 
#            'profile_image_url': 'http://pbs.twimg.com/profile_images/1036478759107551233/0WA2LT23_normal.jpg', 
#            'profile_image_url_https': 'https://pbs.twimg.com/profile_images/1036478759107551233/0WA2LT23_normal.jpg', 
#            'profile_banner_url': 'https://pbs.twimg.com/profile_banners/2265431520/1536071384', 'default_profile': True, 
#            'default_profile_image': False, 'following': None, 'follow_request_sent': None, 'notifications': None}
#         
# rt = RouteTwitterDB()
# rt.write_profile_toDB(results)
# =============================================================================
