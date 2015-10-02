from system.core.model import Model
import re

class User(Model):
	def __init__(self):
		super(User, self).__init__()

	def add_user(self, info):
		EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
		NUMS_PATTERN = re.compile(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?')

		errors = []

		if not info['first_name']:
			errors.append('First name cannot be blank')
		elif len(info['first_name']) < 2:
			errors.append('First name must be at least 2 characters long')

		if not info['last_name']:
			errors.append('Last name cannot be blank')
		elif len(info['last_name']) < 2:
			errors.append('Last name must be at least 2 characters long')

		if not info['alias']:
			errors.append('Alias cannot be blank')
		elif len(info['alias']) < 2:
			errors.append('Alias must be at least 2 characters long')

		if not info['email']:
			errors.append('Email cannot be blank')
		elif not EMAIL_REGEX.match(info['email']):
			errors.append('Email format must be valid!')

		if not info['password']:
			errors.append('Password cannot be blank')
		elif len(info['password']) < 8:
			errors.append('Password must be at least 8 characters long')
		elif info['password'] != info['password_validation']:
			errors.append('Password and confirmation must match!')

		if len(info['birthdate']) != 8:
			errors.append("Birthdate must be entered and follow proper format.")
		elif not NUMS_PATTERN.match(info["birthdate"]):
			errors.append("Birthdate must be numerical.")
		elif int(info['birthdate'][4:]) > 2014:
			errors.append("Must be born before 2015 in order to user this website.")
		elif int(info['birthdate'][:2]) > 12 or int(info['birthdate'][:2]) < 1:
			errors.append("Month must be valid.")
		elif int(info['birthdate'][2:-4]) > 31 or int(info['birthdate'][2:-4]) < 1:
			errors.append("Birthdate day must be valid.")

		if errors:
			return {"status": False, "errors": errors}
		else:
			pw_hash = self.bcrypt.generate_password_hash(info['password'])
			add_query = "INSERT INTO users (alias, first_name, last_name, email, pw_hash, birthdate, created_at) VALUES (%s, %s, %s, %s, %s, %s, NOW())"
			data = [info['alias'], info['first_name'], info['last_name'], info['email'], pw_hash, info['birthdate']]
			self.db.query_db(add_query, data)

			select_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
			user = self.db.query_db(select_query)
			return {"status": True, "user": user[0]}

	def login_user(self, info):
		user_query = "SELECT * FROM users WHERE email = %s LIMIT 1"
		data = [info['email']]
		users = self.db.query_db(user_query, data)

		if len(users) > 0:
			if self.bcrypt.check_password_hash(users[0]['pw_hash'], info['password']):
				return {"status": True, "user": users[0]}

		errors = ["Not a valid e-mail/password combination."]
		return {"status": False, "errors": errors}

	def get_user_by_id(self, id):
		select_query = "SELECT users.id, users.alias ,users.email, users.first_name, users.last_name FROM users WHERE id = %s"
		data = [id]
		user = self.db.query_db(select_query, data)
		return user[0]

	def delete_user(self,id):
		data = [id]
		query2 = "DELETE FROM locations WHERE user_id = %s"
		self.db.query_db(query2, data)
		query= "DELETE FROM users WHERE id = %s"
		self.db.query_db(query, data)

	def update_user(self, id, info):
		query = "UPDATE users SET alias=%s, email=%s WHERE id = %s"
		data = [info['alias'], info['email'], id]
		self.db.query_db(query, data)
