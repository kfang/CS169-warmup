"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from warmup.models import User
from django.utils import simplejson as json
from django.db import DatabaseError


# class SimpleTest(TestCase):
# 	def test_basic_addition(self):
# 		"""
# 		Tests that 1 + 1 always equals 2.
# 		"""
# 		self.assertEqual(1 + 1, 2)

class ClearTest(TestCase):
	def test_Clearing_Database(self):
		user = User(name='admin', password='admin', num_logins=1)
		user.save()

		count = User.objects.count()
		self.assertEqual(count, 1)

		response = self.client.post('/TESTAPI/resetFixture', '', content_type="application/json")
		self.assertEqual(response.status_code, 200)

		count = User.objects.count()
		self.assertEqual(count, 0)

class AddTest(TestCase):
	def test_add_user(self):
		request_data = {}
		request_data['user'] = 'admin'
		request_data['password'] = 'admin'
		response = self.client.post('/users/add', json.dumps(request_data), content_type="application/json")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(User.objects.count(), 1)

class AddBadPassTest(TestCase):
	def test_add_bad_pass(self):
		password = ''
		for n in range(129):
			password += 'a'
		request_data = {}
		request_data['user'] = 'admin'
		request_data['password'] = password
		response = self.client.post('/users/add', json.dumps(request_data), content_type="application/json")
		self.assertEqual(response.status_code, 200)

		response_data = {}
		response_data['errCode'] = -4
		self.assertEqual(response.content, json.dumps(response_data));

class AddBadUserTest(TestCase):
	def test_add_bad_user(self):
		username = ''
		for n in range(129):
			username += 'a'
		request_data = {}
		request_data['user'] = username
		request_data['password'] = 'admin'
		response = self.client.post('/users/add', json.dumps(request_data), content_type="application/json")
		self.assertEqual(response.status_code, 200)

		response_data = {}
		response_data['errCode'] = -3
		self.assertEqual(response.content, json.dumps(response_data));

class AddBlankUserTest(TestCase):
	def test_blank_user(self):
		request_data = {}
		request_data['user'] = ''
		request_data['password'] = 'admin'
		response = self.client.post('/users/add', json.dumps(request_data), content_type="application/json")
		self.assertEqual(response.status_code, 200)

		response_data = {}
		response_data['errCode'] = -3
		self.assertEqual(response.content, json.dumps(response_data));

class AddExistingUserTest(TestCase):
	def test_add_exist_user(self):
		request_data = {}
		request_data['user'] = 'admin'
		request_data['password'] = 'admin'
		response = self.client.post('/users/add', json.dumps(request_data), content_type="application/json")
		self.assertEqual(response.status_code, 200)

		request_data = {}
		request_data['user'] = 'admin'
		request_data['password'] = 'admin'
		response = self.client.post('/users/add', json.dumps(request_data), content_type="application/json")
		self.assertEqual(response.status_code, 200)

		response_data = {}
		response_data['errCode'] = -2
		self.assertEqual(response.content, json.dumps(response_data));

class BadPassLoginTest(TestCase):
	def test_bad_pass_login(self):
		request_data = {}
		request_data['user'] = 'admin'
		request_data['password'] = 'admin'
		response = self.client.post('/users/add', json.dumps(request_data), content_type="application/json")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(User.objects.count(), 1)
		response = self.client.post('/users/login', json.dumps(request_data), content_type="application/json")
		self.assertEqual(response.status_code, 200)

		request_data['password'] = 'fkjfdla;'
		response = self.client.post('/users/login', json.dumps(request_data), content_type="application/json")

		response_data = {}
		response_data['errCode'] = -1
		self.assertEqual(response.content, json.dumps(response_data));

class BadUserLoginTest(TestCase):
	def test_bad_user_login(self):
		request_data = {}
		request_data['user'] = 'admin'
		request_data['password'] = 'admin'
		response = self.client.post('/users/add', json.dumps(request_data), content_type="application/json")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(User.objects.count(), 1)

		request_data['user'] = 'fkjfdla;'
		response = self.client.post('/users/login', json.dumps(request_data), content_type="application/json")

		response_data = {}
		response_data['errCode'] = -1
		self.assertEqual(response.content, json.dumps(response_data));

class LoginTest(TestCase):
	def test_login_user(self):
		request_data = {}
		request_data['user'] = 'admin'
		request_data['password'] = 'admin'
		response = self.client.post('/users/add', json.dumps(request_data), content_type="application/json")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(User.objects.count(), 1)
		response = self.client.post('/users/login', json.dumps(request_data), content_type="application/json")
		self.assertEqual(response.status_code, 200)

		response_data = {}
		response_data['errCode'] = 1
		response_data['count'] = 2
		self.assertEqual(response.content, json.dumps(response_data));

class CountTest(TestCase):
	def test_login_count(self):
		request_data = {}
		request_data['user'] = 'admin'
		request_data['password'] = 'admin'
		response = self.client.post('/users/add', json.dumps(request_data), content_type="application/json")
		self.assertEqual(response.status_code, 200)
		self.assertEqual(User.objects.count(), 1)
		response = self.client.post('/users/login', json.dumps(request_data), content_type="application/json")
		self.assertEqual(response.status_code, 200)

		response_data = {}
		response_data['errCode'] = 1
		response_data['count'] = 2
		self.assertEqual(response.content, json.dumps(response_data));

		response = self.client.post('/users/login', json.dumps(request_data), content_type="application/json")
		response_data['count'] = 3
		self.assertEqual(response.content, json.dumps(response_data));

		response = self.client.post('/users/login', json.dumps(request_data), content_type="application/json")
		response_data['count'] = 4
		self.assertEqual(response.content, json.dumps(response_data));