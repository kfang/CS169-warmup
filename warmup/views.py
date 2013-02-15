from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render

from warmup.models import User

#import JSON library
from django.utils import simplejson as json

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger('hellodjango.custom')

def index(request):
    context = {}
    return render(request, 'warmup/index.html', context)

def add_form(request):
	return render(request, 'warmup/form.html', {})

def login_form(request):
	return render(request, 'warmup/login.html', {})

def reset_form(request):
	return render(request, 'warmup/reset.html', {})

def add(request):
	data = json.loads(request.raw_post_data)
	username = data['user']
	password = data['password']

	response_data = {}
	if User.objects.filter(name=username).count() > 0 :

		#User exists, return ERR_USER_EXISTS
		response_data['errCode'] = -2
		return HttpResponse(json.dumps(response_data), mimetype="application/json")

	elif username == '' or len(username) > 128 :

		#empty username or mroe than 128 ascii characters, return ERR_BAD_USERNAME
		response_data['errCode'] = -3
		return HttpResponse(json.dumps(response_data), mimetype="application/json")

	elif (len(password) > 128) :

		#password more than 128 characters, return ERR_BAD_PASSWORD
		response_data['errCode'] = -4
		return HttpResponse(json.dumps(response_data), mimetype="application/json")

	else :

		#all is good, save the new User
		new_user = User(name=username, password=password,num_logins=1)
		new_user.save()

		#return a SUCCESS and number of logins, should be 1
		response_data['errCode'] = 1
		response_data['count'] = new_user.num_logins
		return HttpResponse(json.dumps(response_data), mimetype="application/json")	

def login(request):
	#get username and password from form data
	data = json.loads(request.raw_post_data)
	username = data['user']
	password = data['password']

	response_data = {}
	#check if credentials match
	try:
		user = User.objects.get(name=username, password=password)
	except (KeyError, User.DoesNotExist):
		response_data['errCode'] = -1
		return HttpResponse(json.dumps(response_data), mimetype="application/json")
	except (KeyError, User.MultipleObjectsReturned):
		response_data['errCode'] = -1
		return HttpResponse(json.dumps(response_data), mimetype="application/json")	
	else:
		user.num_logins += 1
		user.save()
		response_data['errCode'] = 1
		response_data['count'] = user.num_logins
		return HttpResponse(json.dumps(response_data), mimetype="application/json")	

def reset(request):
	response_data = {}
	if request.method == "POST":
		User.objects.all().delete()
		response_data['errCode'] = 1
		return HttpResponse(json.dumps(response_data), mimetype="application/json")	
	else :	
		response_data['errCode'] = 'MUST BE A POST REQUEST'
		return HttpResponse(json.dumps(response_data), mimetype="application/json")	