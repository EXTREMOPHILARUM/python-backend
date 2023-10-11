from flask import Flask
from flask_restful import Api
from flask_restful import Resource
from flask_restful import reqparse
from werkzeug.exceptions import BadRequest
import requests

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        request_data = requests.get("https://jsonplaceholder.typicode.com/todos/")
        return request_data.json()

parser = reqparse.RequestParser()
parser.add_argument('name', type=str)

class GreetUser(Resource):
    def get(self):
        args = parser.parse_args()
        return {'message': f'Hello, {args["name"]}!'}
    

class CustomBadRequest(BadRequest):
    description = 'This is a custom bad request error!'

api.add_resource(GreetUser, '/greet')
api.add_resource(HelloWorld, "/")
app.register_error_handler(CustomBadRequest, lambda err: (str(err), err.code))

app.run(debug=True)
