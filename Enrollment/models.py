from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import models as auth_models
from embed_video.fields import EmbedVideoField
from positions.fields import PositionField

import os

def get_upload_path_image(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s%s.%s" % ('img', instance.pk, ext)

	return os.path.join(
		'images', instance.module.course.code , str(instance.module.id), filename
	)

def get_upload_path_file(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s%s.%s" % ('file', instance.pk, ext)

	return os.path.join(
		'files', instance.module.course.code , str(instance.module.id), filename
	)

class Category(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class Course(models.Model):
	code = models.CharField(max_length=8, unique=True, default=None)
	name = models.CharField(max_length=200)
	description = models.TextField()
	allow_enroll = models.BooleanField()
	
	instructor = models.ForeignKey(auth_models.User, default=auth_models.User)
	enrollmentNo = models.IntegerField(default=0, editable=False)

	# MERGERS_AND_ACQUISITIONS = 'MERQ'
	# MARKETS = 'MRKT'
	# RISK_MANAGEMENT = 'RKMN'
	# SECURITIES = 'SCRT'
	# FINANCIAL_MODELLING = 'FIMO'
	# OPERATIONS = 'OPER'
	# INFORMATION_TECHNOLOGY = 'IFTC'

	# CATEGORY_CHOICES = (
	# 	(MERGERS_AND_ACQUISITIONS, 'Mergers and Acquisitions'),
	# 	(MARKETS, 'Markets'),
	# 	(RISK_MANAGEMENT, 'Risk Management'),
	# 	(SECURITIES, 'Securities'),
	# 	(FINANCIAL_MODELLING, 'Financial Modelling'),
	# 	(OPERATIONS, 'Operations'),	
	# 	(INFORMATION_TECHNOLOGY, 'Information Technology'),		
	# )

	# category = models.CharField(
	# 	max_length=4,
	# 	choices=CATEGORY_CHOICES,
	# 	default=MERGERS_AND_ACQUISITIONS,
	# 	null=True,
	# )

	category = models.ForeignKey(Category)

	def __str__(self):
		return self.name

	def getModules(self):
		return Module.objects.filter(course=self).order_by('position')

	def getInstructor(self):
		return  get_object_or_404(Instructor, user=self.instructor)

	def available(self):
		if self.allow_enroll:
			return "Available"
		else:
			return "Not Available"


class Instructor(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, blank=True, null=True)

	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	position = models.CharField(max_length=50)

	def __str__(self):
		return (self.first_name + " " + self.last_name)

	def getUser(self):
		return self.user


class Participant(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, default=None, blank=True, null=True)

	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	position = models.CharField(max_length=50)

	def __str__(self):
		return (self.first_name + " " + self.last_name)

	def getUser(self):
		return self.user

class Enrollment(models.Model):
	course = models.ForeignKey('Course',on_delete=models.CASCADE, default=None, blank=True, null=True)
	participant = models.ForeignKey(User)
	date_enrollment = models.DateField()
	date_finish = models.DateField(default=None, blank=True, null=True)
	PROGRESS = 'PR'
	FINISHED = 'FI'
	STATE_CHOICES = (
		(PROGRESS, 'Progress'),
		(FINISHED, 'Finished'),
	)
	state = models.CharField(
		max_length=2,
		choices=STATE_CHOICES,
		default=PROGRESS,
	)
	progress = models.IntegerField(default=0)

class Module(models.Model):
	course = models.ForeignKey('Course',on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	visible = models.BooleanField(default=True)
	instructor = models.ForeignKey(auth_models.User, default='',)
	position = PositionField(collection='course',default=0)


	def __str__(self):
		return (self.course.code + " " + self.name)

	def getComponents(self):
		return Component.objects.filter(module=self).order_by('position')

class Component(models.Model):
	module = models.ForeignKey('Module',on_delete=models.CASCADE)
	name = models.CharField(max_length=50, null=True)
	instructor = models.ForeignKey(auth_models.User, default='')
	position = PositionField(collection='module',default=0)

	TEXT = 'TXT'
	IMAGE = 'IMG'
	VIDEO = 'VID'
	FILE = 'FIL'
	COMPONENT_TYPE_CHOICES = (
		(TEXT, 'Text'),
		(IMAGE, 'Image'),
		(VIDEO, 'Video'),
		(FILE, 'File'),
	)
	component_type = models.CharField(
		max_length=3,
		choices=COMPONENT_TYPE_CHOICES,
		default=TEXT,
		null=True,
	)
	text = models.TextField(blank=True, null=True)
	image = models.ImageField(upload_to=get_upload_path_image, blank=True, null=True)
	file = models.FileField(upload_to=get_upload_path_file, blank=True, null=True)
	video = EmbedVideoField(blank=True, null=True)

	def __str__(self):
		return self.name

	def printContent(self):
		if self.component_type == "TXT":
			return self.text
		if self.component_type == "IMG":
			content = "<img src='" + self.image.url + "'/>"
			return content
		if self.component_type == "FIL":
			content = "<a href='" + self.file.url + "'>" + self.name + "</a>"
			return content


	def printLink(self):
		if self.component_type == "FIL":
			content = "<a href='" + self.file.url + "'>" + self.name + "</a>"
			return content

		else:
			content = "<a href='./c/" + str(self.id) + "'>" + self.name + "</a>"
			return content

	def getComponentType(self):
		if self.component_type == "TXT":
			return "Text"
		if self.component_type == "IMG":
			return "Image"
		if self.component_type == "FIL":
			return "File"
		if self.component_type == "VID":
			return "Video"

