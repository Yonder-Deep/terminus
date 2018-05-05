import sys
from flask import Flask
from flask_restful import Resource, Api

sys.path.insert(0, '../Communication/base_station/')


from base_station import returnInfo



app = Flask(__name__)
api = Api(app)

class getInfo(Resource):
    def get(self):
       return returnInfo()

api.add_resource(getInfo, '/getInfo')

if __name__ == '__main__':
    app.run(debug=True)

