from system.core.model import Model
import re

class Location(Model):
    def __init__(self):
        super(Location, self).__init__()

    def add_location(self, id, coords):
        query = "INSERT INTO locations (latitude, longitude, user_id, created_at) VALUES (%s, %s, %s, NOW())"
        data = [coords[0], coords[1], id]
        self.db.query_db(query, data)

    def get_all_locations(self):
        query = "SELECT * FROM locations"
        locations = self.db.query_db(query)
        return locations

    def get_location(self, id):
        query = "SELECT location FROM locations WHERE user_id != (%s)"
        data = [id]
        return self.db.query_db(query,data)
