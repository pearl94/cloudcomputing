#A database and  the views are defined hwere as this is how i could get the database to appear on the navigation bar

from app import app
from flask import render_template, request
import unirest
from forms import MessageForm
from flask_navigation import Navigation
from app import simple
from flask_pymongo import PyMongo
from flask import jsonify
import os

#The database is defined here
#parts of the code found online
app.config['MONGO_DBNAME'] = os.environ['OPENSHIFT_APP_NAME']
app.config['MONGO_URI'] = os.environ['OPENSHIFT_MONGODB_DB_URL'] + os.environ['OPENSHIFT_APP_NAME']

mongo = PyMongo(app)


@app.route('/database/methods', methods=['GET'])
def get_db_methods_and_attributes():
	return jsonify({'All methods and attributes on a flask mongodb object' : dir(mongo.db)})


@app.route('/database/London/methods', methods=['GET'])
def get_collection_methods_and_attributes():
	return jsonify({'All methods and attributes on a flask mongodn collection object' : dir(mongo.db.London_Visitors)})

#@app.route('/database/collections', methods=['GET'])
#def get_all_collections():
#	return jsonify({'result' : mongo.db.collection_names()})

@app.route('/database/London/sample', methods=['GET'])
def get_sample_document():
	collection = mongo.db.London_Visitors
	output = []
	i = 0;
	for document in collection.find():
		i=i+1
		if i > 50:
		   break

		output.append({attr:value for attr, value in document.iteritems() if attr!=u'_id'})
	return render_template("db.html",mood=output)

# Here the views are defined
@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")

@app.route('/visualization')
def colur():
	return simple.polynomial()

@app.route('/database/methods')
def database_methods():
	return render_template("db.html")



@app.route('/emotion/')
def emotion():
	return render_template("my_form.html",mood='happy',form=MessageForm())

@app.route('/emotion/', methods=['POST'])
def emotion_post():
	msg = request.form['message']
	response = unirest.post("https://community-sentiment.p.mashape.com/text/",
	  headers={
	    "X-Mashape-Key": "6VWQcE5umumsh9oLsHfFlOseFGbDp1caaUKjsnj6PJRqxZKslv",
	    "Content-Type": "application/x-www-form-urlencoded",
    	"Accept": "application/json"
    	},
  		params={
    	"txt": msg
  		}
	)
	return render_template("my_form.html",mood=response.body['result']['sentiment'],form=MessageForm())
#Here the navigatin bar items are defined
nav = Navigation(app)

nav.Bar('top', [
nav.Item('Home', 'index'),
nav.Item('Emotion App', 'emotion'),
nav.Item('Visualization', 'polynomial'),
nav.Item('Methods database', 'get_db_methods_and_attributes'),
nav.Item('Collections and Attributes Database', 'get_collection_methods_and_attributes')
])
