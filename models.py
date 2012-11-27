# -*- coding: utf-8 -*-
from flask.ext.mongoengine.wtf import model_form
from wtforms.fields import * # for our custom signup form
from flask.ext.mongoengine.wtf.orm import validators
from flask.ext.mongoengine import *
from datetime import datetime

class Comment(mongoengine.EmbeddedDocument):
	name = mongoengine.StringField()
	comment = mongoengine.StringField()
	timestamp = mongoengine.DateTimeField(default=datetime.now())

class Image(mongoengine.Document):

	title = mongoengine.StringField(max_length=120, required=True)
	description = mongoengine.StringField()
	postedby = mongoengine.StringField(max_length=120, required=True, verbose_name="Your name")
	
	tags = mongoengine.ListField( mongoengine.StringField())

	filename = mongoengine.StringField()

	# Comments is a list of Document type 'Comments' defined above
	comments = mongoengine.ListField( mongoengine.EmbeddedDocumentField(Comment) )

	# Timestamp will record the date and time idea was created.
	timestamp = mongoengine.DateTimeField(default=datetime.now())


photo_form = model_form(Image)

# Create a WTForm form for the photo upload.
# This form will inhirit the Photo model above
# It will have all the fields of the Photo model
# We are adding in a separate fielclass Idea(Document):

	creator = StringField(max_length=120, required=True, verbose_name="Your Name", help_text="Please enter your first name")
	title = StringField(max_length=120, required=True, verbose_name="Item Title")
	#title = StringField(max_length=120, required=True)
	slug = StringField()
	idea = StringField(required=True, verbose_name="Description")
	#image = StringField(required=True, verbose_name="item image")
	#idea = StringField(required=True, verbose_name="Description?")

	# Category is a list of Strings
	categories = ListField(StringField(max_length=30))

	# Images
	#images = ListField(StringField)

	# Comments is a list of Document type 'Comments' defined above
	comments = ListField( EmbeddedDocumentField(Comment) )

	# Timestamp will record the date and time idea was created.
	timestamp = DateTimeField(default=datetime.now())

IdeaForm = model_form(Idea)
	

d for the file upload called 'fileupload'
class photo_upload_form(photo_form):
	fileupload = FileField('Upload an image file', validators=[])







	

