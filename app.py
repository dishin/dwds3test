# -*- coding: utf-8 -*-
import os, datetime, re
from flask import Flask, request, render_template, redirect, abort
from werkzeug import secure_filename

from flask import jsonify



# import all of mongoengine
from flask.ext.mongoengine import mongoengine

# import data models
import models

# Amazon AWS library
import boto

# Python Image Library
import StringIO
#from PIL import Image



# create Flask app
app = Flask(__name__)   # create our flask app


app = Flask(__name__)   # create our flask app
app.secret_key = os.environ.get('SECRET_KEY') # put SECRET_KEY variable inside .env file with a random string of alphanumeric characters
app.config['CSRF_ENABLED'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 megabyte file upload

# --------- Database Connection ---------
# MongoDB connection to MongoLab's database
mongoengine.connect('mydata', host=os.environ.get('MONGOLAB_URI'))
app.logger.debug("Connecting to MongoLabs")

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

# hardcoded categories for the checkboxes on the form
#categories = ['GEAR','TECH','FASHION','BODY','ART','RIDE','PLACE']


# --------- Routes ----------



@app.route("/fsq", methods=['GET','POST'])
def main():
	if request.method == "GET":
		return render_template('main.html')

	elif request.method == "POST":

		user_latlng = request.form.get('user_latlng')

		# Foursquare API endpoint for Venues
		fsq_url = "https://api.foursquare.com/v2/venues/search"

		# prepare the foursquare query parameters for the Venues Search request
		# simple example includes lat,long search
		# we pass in our client id and secret along with 'v', a version date of API.
		fsq_query = {
			'll' : user_latlng,
			'query': 'car',
			'client_id' : os.environ.get('FOURSQUARE_CLIENT_ID'), # info from foursquare developer setting, placed inside .env
			'client_secret' : os.environ.get('FOURSQUARE_CLIENT_SECRET'),
			'v' : '20121113' # YYYYMMDD
		}









		# using Requests library, make a GET request to the fsq_url
		# pass in the fsq_query dictionary as 'params', this will build the full URL with encoding variables.
		results = requests.get(fsq_url, params=fsq_query)

		# log out the url that was request
		app.logger.info("Requested url : %s" % results.url)

		# if we receive a 200 HTTP status code, great! 
		if results.status_code == 200:

			# get the response, venue array 
			fsq_response = results.json # .json returns a python dictonary to us.
			nearby_venues = fsq_response['response']['venues']

			app.logger.info('nearby venues')
			app.logger.info(nearby_venues)

			# Return raw json for demonstration purposes. 
			# You would likely use this data in your templates or database in a real app
			

			#return jsonify(results.json['response'])
	
		#else:

			# Foursquare API request failed somehow
			#return "uhoh, something went wrong %s" % results.json




			# Return raw json for demonstration purposes. 
			# You would likely use this data in your templates or database in a real app
			
			shopping = results.json['response']
			venues = shopping.get('venues')

			
			templateData = {

			'venues' : venues

			}
			#return jsonify(shopping)
			return render_template('shopping.html', **templateData)

	
		else:

			# Foursquare API request failed somehow
			return "uhoh, something went wrong %s" % results.json



































# this is our main page
@app.route("/", methods=['GET','POST'])
def index():

	# get Idea form from models.py
	photo_upload_form = models.photo_upload_form(request.form)
	
	# if form was submitted and it is valid...
	if request.method == "POST" and photo_upload_form.validate():
		uploaded_file = request.files['fileupload']
		# app.logger.info(file)
		# app.logger.info(file.mimetype)
		# app.logger.info(dir(file))
		
		# Uploading is fun
		# 1 - Generate a file name with the datetime prefixing filename
		# 2 - Connect to s3
		# 3 - Get the s3 bucket, put the file
		# 4 - After saving to s3, save data to database

		if uploaded_file and allowed_file(uploaded_file.filename):
			# create filename, prefixed with datetime
			now = datetime.datetime.now()
			filename = now.strftime('%Y%m%d%H%M%s') + "-" + secure_filename(uploaded_file.filename)
			thumb_filename = now.strftime('%Y%m%d%H%M%s') + "-" + secure_filename(uploaded_file.filename)

			# connect to s3
			s3conn = boto.connect_s3(os.environ.get('AWS_ACCESS_KEY_ID'),os.environ.get('AWS_SECRET_ACCESS_KEY'))

			# open s3 bucket, create new Key/file
			# set the mimetype, content and access control
			b = s3conn.get_bucket(os.environ.get('AWS_BUCKET')) # bucket name defined in .env
			k = b.new_key(b)
			k.key = filename
			k.set_metadata("Content-Type", uploaded_file.mimetype)
			k.set_contents_from_string(uploaded_file.stream.read())
			k.make_public()

			# save information to MONGO database
			if k and k.size > 0:
				
				submitted_image = models.Image()
				submitted_image.title = request.form.get('title')
				submitted_image.description = request.form.get('description')

				submitted_image.category = request.form.get('category')

                


				submitted_image.postedby = request.form.get('postedby')
				submitted_image.filename = filename # same filename of s3 bucket file
				submitted_image.save()


			return redirect('/')

		else:
			return "uhoh there was an error " + uploaded_file.filename



	else:
		# get existing images
		images = models.Image.objects.order_by('-timestamp')
		
		# render the template
		templateData = {
			'images' : images,
			'form' : photo_upload_form
		}

		return render_template("main.html", **templateData)

@app.route('/delete/<imageid>')
def delete_image(imageid):
	
	image = models.Image.objects.get(id=imageid)
	if image:

		# delete from s3
	
		# connect to s3
		s3conn = boto.connect_s3(os.environ.get('AWS_ACCESS_KEY_ID'),os.environ.get('AWS_SECRET_ACCESS_KEY'))

		# open s3 bucket, create new Key/file
		# set the mimetype, content and access control
		bucket = s3conn.get_bucket(os.environ.get('AWS_BUCKET')) # bucket name defined in .env
		k = bucket.new_key(bucket)
		k.key = image.filename
		bucket.delete_key(k)

		# delete from Mongo	
		image.delete()

		return redirect('/')

	else:
		return "Unable to find requested image in database."






#addtional 
@app.route("/", methods=['GET','POST'])
def thumb():
	if request.method == "POST":
		if request.form.get('do') == 'like':
			like_response.update(inc__likes=1)
		#if request.form.get('do') == 'dislike':
			#like_response.update(dec__likes=1)
		return redirect('/')


















@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

def allowed_file(filename):
    return '.' in filename and \
           filename.lower().rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)



	