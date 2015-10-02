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
		login_status

		if login_status['status'] == True:
			session['id'] = login_status['user']['id']
			session['alias'] = login_status['user']['alias']

			return redirect('/users/landing_page')
		else:
			for message in login_status['errors']:
				flash(message, 'regis_errors')
		return redirect('/')

	def edit(self,id):
		user = self.models['User'].get_user_by_id(id)
		return self.load_view("/users/edit.html",user = user)

	def delete(self,id):
		self.models['User'].delete_user(id)
		session.pop('id')
		session.pop('alias')
		return redirect('/')

	def landing_page(self):
		user = self.models['User'].get_user_by_id(session['id'])
		return self.load_view('/users/landing_page.html', user=user)

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
		event = request.form['event']
		lat_and_long = coords.split(",")
		self.models['Location'].add_location(id, lat_and_long, event)
		return redirect('/find_location')

	def update(self, id):
		info = {
			'alias': request.form['alias'],
			'email': request.form['email']
		}
		self.models['User'].update_user(id, info)
		return redirect('/users/landing_page')

	# def people_near_me(self):
	# 	id = session['id']
	# 	locations = self.models['Location'].get_location(id)
	# 	print locations
	# 	return jsonify(locations=locations)
