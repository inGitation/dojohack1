from system.core.model import Model
import re
import datetime

class Location(Model):
    def __init__(self):
        super(Location, self).__init__()

    def add_location(self, id, coords, event):
        query = "INSERT INTO locations (latitude, longitude, event, user_id, created_at, display_time) VALUES (%s, %s, %s, %s, NOW(), %s)"
        time_now = datetime.datetime.now().strftime("%B %d, %Y at %H:%M")
        data = [coords[0], coords[1], event, id, time_now]
        self.db.query_db(query, data)

    def get_all_locations(self):
        query = "SELECT * FROM locations"
        locations = self.db.query_db(query)
        return locations

    def get_location(self, id):
        query = "SELECT location FROM locations WHERE user_id != (%s)"
        data = [id]
        return self.db.query_db(query,data)
