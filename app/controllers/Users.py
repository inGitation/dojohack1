from system.core.controller import *

class Users(Controller):
	def __init__(self, action):
		super(Users, self).__init__(action)
		self.load_model('User')
		self.load_model('Location')

	def index(self):
		if 'id' in session:
			return redirect('/users/landing_page')
		return self.load_view('users/index.html')

	def signup_page(self):
		return self.load_view('users/login.html')

	def create(self):
		user_info = {
			'alias': request.form['alias'],
			'first_name': request.form['first_name'],
			'last_name': request.form['last_name'],
			'email': request.form['email'],
			'password': request.form['password'],
			'password_validation': request.form['password_validation'],
			'birthdate': request.form['birthdate']
		}

		create_status = self.models['User'].add_user(user_info)

		if create_status['status'] == True:
			session['id'] = create_status['user']['id']
			session['alias'] = create_status['user']['alias']
			return redirect('/users/landing_page')
		else:
			for message in create_status['errors']:
				flash(message, 'regis_errors')
		return redirect('/signup_page')

	def login(self):
		user_info = {
			'email': request.form['username'],
			'password': request.form['password']
		}

		login_status = self.models['User'].login_user(user_info)

		if login_status['status'] == True:
			session['id'] = login_status['user']['id']
			session['alias'] = login_status['user']['alias']
			return redirect('/users/landing_page')
		else:
			for message in login_status['errors']:
				flash(message, 'regis_errors')
		return redirect('/')

	def landing_page(self):
		return self.load_view('/users/landing_page.html')

	def logout(self):
		session.pop('id')
		session.pop('alias')
		return redirect('/')

	def find_location(self):
		print "AND WE GOT TO THE FIND LOCATION METHOD!"
		locations = self.models['Location'].get_all_locations()
		length_locations = len(locations)
		return self.load_view('/location/get_location.html', locations=locations, length_locations=length_locations)

	def set_location(self):
		user = self.models['User'].get_user_by_id(session['id'])
		print user
		return self.load_view('/location/set_location.html', user=user)

	def set(self, id, coords):
		lat_and_long = coords.split(",")
		self.models['Location'].add_location(id, lat_and_long)
		return redirect('/find_location')
