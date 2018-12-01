### ROUTE APIS
## Created By: ROUTE Inc 2018
## Author: Hassan Ali
## Created: 4/01/2018
## Edit: 4/16/2018
## Edits: 5/6/2018
## Edits: 8/10/2018
## Edits: 10/17/2018
## Edits: 11/17/2018

##module imports
from flask import Flask, request, jsonify, abort
from flask_cors import CORS, cross_origin

import pdb


app = Flask(__name__)
CORS(app, expose_headers='authorization')


##file imports
#import common.route_assist as ra
import routetwitterapi
rtweet = routetwitterapi.RouteTwitterAPI()



#default API description page
@app.route('/', methods=["GET"])
def routetweet():
    return "route tweet api"

#default API description page
@app.route('/GetHomeTimeline', methods=["GET"])
def getHomeTimeLine():
    return rtweet.get_home_timeline()


#default API description page
@app.route('/GetStatusesTimeline', methods=["GET"])
def getStatusesTimeline():
    return rtweet.get_statuses_timeline()

#default API description page
@app.route('/GetUser', methods=["GET"])
def getUser():
    return rtweet.get_user('402771404')


#default API description page
@app.route('/GetRateLimit', methods=["GET"])
def getRateLimits():
    return rtweet.get_rate_limits()

#default API description page
@app.route('/GetSummary', methods=["GET"])
def getSummary():
    return rtweet.get_summary()

#default API description page
@app.route('/GetFollowers', methods=["GET"])
def listFollowers():
    return rtweet.get_follower_list()

#default API description page
@app.route('/GetFollowersIds', methods=["GET"])
def listFollowers_ids():
    return rtweet.get_follower_list_ids()


#default API description page
@app.route('/GetFriends', methods=["GET"])
def listFriends():
    return rtweet.get_friend_list()
        

##testing a simple return api call
@app.route('/test', methods = ['GET'])
def getTest():
    ## test api
    return "testing a basic api return call"



##System controls
@app.teardown_appcontext
def close_connections(error):
    print('api teardown {}'.format(error))
    ##rtapi.closeConnection()
    
    
#todo: return a json string with empty message
@app.errorhandler(404)
def page_not_found(e):
    return "page not found becasue we haven't made that page yet, {} \n {}".format(404,e)


@app.errorhandler(403)
def permission_error(e):
    return "error, {} \n {}".format(403,e)

#unauthorized
@app.errorhandler(401)
def unauthorized_access(e):
    return "error, {} \n {}".format(401,e)




#app running on http://127.0.0.1:5000/
if __name__ == '__main__':
    print('running...')
    app.run(host='0.0.0.0', debug=True)
    
if __name__ != '__main__':
    print('Gunicorn running...')
    
 
    




        



    

    
    


