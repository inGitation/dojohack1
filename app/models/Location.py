from system.core.model import Model

class Location(Model):
    def __init__(self):
        super(Location, self).__init__()

    def set_locat(self, id, coords):
        print id
        print coords
        query = 'INSERT INTO locations(location,user_id) VALUES(%s,%s)'
        data = [coords,id]
        return self.db.query_db(query, data)

    def get_location(self,id):
        query ="SELECT location FROM locations WHERE user_id != (%s)"
        data = [id]
        return self.db.query_db(query,data)
