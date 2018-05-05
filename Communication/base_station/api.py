import sys
from flask import Flask
from flask_restful import Resource, Api



from base_station import BaseStation



app = Flask(__name__)
api = Api(app)

class getInfo(Resource):
    def get(self):
       with open('data.txt', 'r') as f:
           info = f.readline()
           data = [ord(x) for x in list(info)]
           print "info ", data
           data = data[:-1]  
           return data

api.add_resource(getInfo, '/getInfo')

if __name__ == '__main__':
    app.run(debug=True)

