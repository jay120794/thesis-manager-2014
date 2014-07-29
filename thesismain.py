import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
DEFAULT_GUESTBOOK_NAME1 = 'default_guestbook1'
DEFAULT_GUESTBOOK_NAME2 = 'default_guestbook2'

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
	"""Constructs a Datastore key for a Guestbook entity with guestbook_name."""
	return ndb.Key('Guestbook', guestbook_name)

class Greeting(ndb.Model):
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)
	
class Thesis(ndb.Model):
	thesis_title = ndb.StringProperty(indexed=False)
	thesis_desc = ndb.StringProperty(indexed=False)
	thesis_year = ndb.StringProperty(indexed=False)
	thesis_status = ndb.StringProperty(indexed=False)

class Adviser(ndb.Model):
	adviser_title = ndb.StringProperty(indexed=False)
	adviser_fname = ndb.StringProperty(indexed=False)
	adviser_lname = ndb.StringProperty(indexed=False)
	adviser_eadd = ndb.StringProperty(indexed=False)
	adviser_phonenum = ndb.StringProperty(indexed=False)
	adviser_dept = ndb.StringProperty(indexed=False)

class Student(ndb.Model):
	student_dept = ndb.StringProperty(indexed=False)
	student_fname = ndb.StringProperty(indexed=False)
	student_lname = ndb.StringProperty(indexed=False)
	student_studnum = ndb.StringProperty(indexed=False)
	student_eadd = ndb.StringProperty(indexed=False)
	student_remarks = ndb.StringProperty(indexed=False)

class ThesisViewHandler(webapp2.RequestHandler):
	def get(self, thesis_id):
		thesis_all=Thesis.query().fetch()
		thesis_id = int(thesis_id)
		
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values={
			'id': thesis_id,
			'thesis_all': thesis_all,
			'url': url,
			'url_linktext': url_linktext,
			'user_name': users.get_current_user()
		}
		template = JINJA_ENVIRONMENT.get_template('thesis_description.html')
		self.response.write(template.render(template_values))

class ThesisListHandler(webapp2.RequestHandler):
	def get(self):
		thesis_all=Thesis.query().fetch()
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
		template_values={
			'thesis_all': thesis_all,
			'url': url,
			'url_linktext': url_linktext,
			'user_name': users.get_current_user()
		}

		template = JINJA_ENVIRONMENT.get_template('thesis_list.html')
		self.response.write(template.render(template_values))

class ThesisEditHandler(webapp2.RequestHandler):
	def get(self, thesis_id):
		thesis_all=Thesis.query().fetch()
		thesis_id = int(thesis_id)

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
		template_values={
			'id': thesis_id,
			'thesis_all': thesis_all,
			'url': url,
			'url_linktext': url_linktext,
			'user_name': users.get_current_user()
		}
		template = JINJA_ENVIRONMENT.get_template('thesis_edit.html')
		self.response.write(template.render(template_values))

	def post(self, thesis_id):
		thesis_id = int(thesis_id)
		thesis = Thesis.get_by_id(thesis_id)
		thesis.thesis_title=self.request.get('thesis_title')
		thesis.thesis_desc=self.request.get('thesis_desc')
		thesis.thesis_year=self.request.get('thesis_year')
		thesis.thesis_status=self.request.get('thesis_status')
		thesis.put()
		self.redirect('/thesis/list')

class ThesisNewHandler(webapp2.RequestHandler):
	def get(self):

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'url': url,
			'url_linktext': url_linktext,
			'user_name': users.get_current_user()
		}

		template = JINJA_ENVIRONMENT.get_template('thesis_new.html')
		self.response.write(template.render(template_values))

	def post(self):
		thesis = Thesis()
		thesis.thesis_title=self.request.get('thesis_title')
		thesis.thesis_desc=self.request.get('thesis_desc')
		thesis.thesis_year=self.request.get('thesis_year')
		thesis.thesis_status=self.request.get('thesis_status')
		thesis.put()
		self.redirect('/thesis/list')

class AdviserNewHandler(webapp2.RequestHandler):
	def get(self):

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'url': url,
			'url_linktext': url_linktext,
			'user_name': users.get_current_user()
		}

		template = JINJA_ENVIRONMENT.get_template('adviser_new.html')
		self.response.write(template.render(template_values))

	def post(self):
		adviser = Adviser()
		adviser.adviser_title=self.request.get('adviser_title')
		adviser.adviser_fname=self.request.get('adviser_fname')
		adviser.adviser_lname=self.request.get('adviser_lname')
		adviser.adviser_eadd=self.request.get('adviser_eadd')
		adviser.adviser_phonenum=self.request.get('adviser_phonenum')
		adviser.adviser_dept=self.request.get('adviser_dept')
		adviser.put()
		self.redirect('/adviser/list')

class AdviserEditHandler(webapp2.RequestHandler):
	def get(self, adviser_id):
		adviser_all=Adviser.query().fetch()
		adviser_id = int(adviser_id)

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values={
			'id': adviser_id,
			'adviser_all': adviser_all,
			'url': url,
			'url_linktext': url_linktext,
			'user_name': users.get_current_user()
		}
		template = JINJA_ENVIRONMENT.get_template('adviser_edit.html')
		self.response.write(template.render(template_values))

	def post(self, adviser_id):
		adviser_id = int(adviser_id)
		adviser = Adviser.get_by_id(adviser_id)
		adviser.adviser_title=self.request.get('adviser_title')
		adviser.adviser_fname=self.request.get('adviser_fname')
		adviser.adviser_lname=self.request.get('adviser_lname')
		adviser.adviser_eadd=self.request.get('adviser_eadd')
		adviser.adviser_phonenum=self.request.get('adviser_phonenum')
		adviser.adviser_dept=self.request.get('adviser_dept')
		adviser.put()
		self.redirect('/adviser/list')

class AdviserListHandler(webapp2.RequestHandler):
	def get(self):
		adviser_all=Adviser.query().fetch()

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values={
			'adviser_all': adviser_all,
			'url': url,
			'url_linktext': url_linktext,
			'user_name': users.get_current_user()
		}

		template = JINJA_ENVIRONMENT.get_template('adviser_list.html')
		self.response.write(template.render(template_values))

class AdviserViewHandler(webapp2.RequestHandler):
	def get(self, adviser_id):
		adviser_all=Adviser.query().fetch()
		adviser_id = int(adviser_id)
		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values={
			'id': adviser_id,
			'adviser_all': adviser_all,
			'url': url,
			'url_linktext': url_linktext,
			'user_name': users.get_current_user()
		}
		template = JINJA_ENVIRONMENT.get_template('adviser_view.html')
		self.response.write(template.render(template_values))

class StudentNewHandler(webapp2.RequestHandler):
	def get(self):

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'url': url,
			'url_linktext': url_linktext,
			'user_name': users.get_current_user()
		}

		template = JINJA_ENVIRONMENT.get_template('student_new.html')
		self.response.write(template.render(template_values))

	def post(self):
		student = Student()
		student.student_dept=self.request.get('student_dept')
		student.student_fname=self.request.get('student_fname')
		student.student_lname=self.request.get('student_lname')
		student.student_studnum=self.request.get('student_studnum')
		student.student_eadd=self.request.get('student_eadd')
		student.student_remarks=self.request.get('student_remarks')
		student.put()
		self.redirect('/student/list')

class StudentListHandler(webapp2.RequestHandler):
	def get(self):
		student_all=Student.query().fetch()

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values={
			'student_all': student_all,
			'url': url,
			'url_linktext': url_linktext,
			'user_name': users.get_current_user()
		}

		template = JINJA_ENVIRONMENT.get_template('student_list.html')
		self.response.write(template.render(template_values))

class StudentViewHandler(webapp2.RequestHandler):
	def get(self, student_id):
		student_all=Student.query().fetch()
		student_id = int(student_id)

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'id': student_id,
			'student_all': student_all,
			'url': url,
			'url_linktext': url_linktext,
			'user_name': users.get_current_user()
		}
		template = JINJA_ENVIRONMENT.get_template('student_view.html')
		self.response.write(template.render(template_values))

class StudentEditHandler(webapp2.RequestHandler):
	def get(self, student_id):
		student_all=Student.query().fetch()
		student_id = int(student_id)

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values={
			'id': student_id,
			'student_all': student_all,
			'url': url,
			'url_linktext': url_linktext,
			'user_name': users.get_current_user()
		}
		template = JINJA_ENVIRONMENT.get_template('student_edit.html')
		self.response.write(template.render(template_values))

	def post(self, student_id):
		student_id = int(student_id)
		student = Student.get_by_id(student_id)
		student.student_dept=self.request.get('student_dept')
		student.student_fname=self.request.get('student_fname')
		student.student_lname=self.request.get('student_lname')
		student.student_studnum=self.request.get('student_studnum')
		student.student_eadd=self.request.get('student_eadd')
		student.student_remarks=self.request.get('student_remarks')
		student.put()
		self.redirect('/student/list')

class HomePageHandler(webapp2.RequestHandler):
	def get(self):
		guestbook_name = self.request.get('guestbook_name',
			DEFAULT_GUESTBOOK_NAME)
		greetings_query = Greeting.query(
			ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
		greetings = greetings_query.fetch(5)

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'greetings': greetings,
			'guestbook_name': urllib.quote_plus(guestbook_name),
			'url': url,
			'url_linktext': url_linktext,
			'user_name': users.get_current_user()
			}

		template = JINJA_ENVIRONMENT.get_template('homepage.html')
		self.response.write(template.render(template_values))

	def post(self):
		guestbook_name = self.request.get('guestbook_name',
			DEFAULT_GUESTBOOK_NAME)
		greeting = Greeting(parent=guestbook_key(guestbook_name))

		if users.get_current_user():
			greeting.author = users.get_current_user()

		greeting.content = self.request.get('content')
		greeting.put()

		query_params = {'guestbook_name': guestbook_name}
		self.redirect('/')

class MemberOnePage(webapp2.RequestHandler):
	def get(self):
		guestbook_name = self.request.get('guestbook_name1',
			DEFAULT_GUESTBOOK_NAME1)
		greetings_query = Greeting.query(
			ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
		greetings = greetings_query.fetch(5)

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'greetings': greetings,
			'guestbook_name': urllib.quote_plus(guestbook_name),
			'url': url,
			'url_linktext': url_linktext,
			'user_name': users.get_current_user()
			}

		template = JINJA_ENVIRONMENT.get_template('personal-web-member-1.html')
		self.response.write(template.render(template_values))

	def post(self):
		guestbook_name = self.request.get('guestbook_name1',
			DEFAULT_GUESTBOOK_NAME1)
		greeting = Greeting(parent=guestbook_key(guestbook_name))

		if users.get_current_user():
			greeting.author = users.get_current_user()

			greeting.content = self.request.get('content')
			greeting.put()

			query_params = {'guestbook_name': guestbook_name}
			self.redirect('/module-1/1')

class MemberTwoPage(webapp2.RequestHandler):
	def get(self):
		guestbook_name = self.request.get('guestbook_name2',
			DEFAULT_GUESTBOOK_NAME2)
		greetings_query = Greeting.query(
			ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
		greetings = greetings_query.fetch(5)

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			url_linktext = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'

		template_values = {
			'greetings': greetings,
			'guestbook_name': urllib.quote_plus(guestbook_name),
			'url': url,
			'url_linktext': url_linktext,
			'user_name': users.get_current_user()
		}

		template = JINJA_ENVIRONMENT.get_template('personal-web-member-2.html')
		self.response.write(template.render(template_values))
	def post(self):
		guestbook_name = self.request.get('guestbook_name',
			DEFAULT_GUESTBOOK_NAME)
		greeting = Greeting(parent=guestbook_key(guestbook_name))

		if users.get_current_user():
			greeting.author = users.get_current_user()

		greeting.content = self.request.get('content')
		greeting.put()

		query_params = {'guestbook_name': guestbook_name}
		self.redirect('/module-1/2?')

application = webapp2.WSGIApplication([
    ('/thesis/new', ThesisNewHandler),
    ('/thesis/list', ThesisListHandler),
    ('/thesis/view/(\d+)', ThesisViewHandler),
    ('/thesis/edit/(\d+)', ThesisEditHandler), 
    ('/adviser/new', AdviserNewHandler),
    ('/adviser/list', AdviserListHandler),
    ('/adviser/view/(\d+)', AdviserViewHandler),
    ('/adviser/edit/(\d+)', AdviserEditHandler),
    ('/student/new', StudentNewHandler),
    ('/student/list', StudentListHandler),
    ('/student/view/(\d+)', StudentViewHandler),
    ('/student/edit/(\d+)', StudentEditHandler),
    ('/module-1/1', MemberOnePage),
    ('/post-member1', MemberOnePage),
    ('/module-1/2', MemberTwoPage),
    ('/post-member2', MemberTwoPage),
    ('/', HomePageHandler),
    ('/sign', HomePageHandler)
], debug=True)