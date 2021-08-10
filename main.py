from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app)

class Users(Resource):
    # GET
    def get(self):
        data = pd.read_csv('users.csv') # read CSV
        data = data.to_dict() # convert dataframe to dictionary
        return{'data': data}, 200 # return data and 200 OK code

    # POST
    def post(self):
        parser = reqparse.RequestParser() # initialize
        
        parser.add_argument('userId', required = True)
        parser.add_argument('name', required = True)
        parser.add_argument('city', required = True)

        args = parser.parse_args() # parse arguments to dictionary

        # read CSV
        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            return{
                'message':f"'{args['userId']}' already exists."
            }, 401
        else:
            new_data = pd.DataFrame({
                'userId': args['userId'],
                'name': args['name'],
                'city': args['city'],
                'locations': [[]]
            })
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            data.to_csv('users.csv', index=False)            # save back to CSV
            return {'data':data.to_dict()}, 200

    # PUT
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required = True)
        parser.add_argument('location', required = True)
        args = parser.parse_args()

        data = pd.read_csv('users.csv')
        
        if args['userId'] in list(data['userId']):
            # evaluate strings of lists to lists
            data['locations'] = data['locations'].apply(
                lambda x: ast.literal_eval(x)
            )

            # select our user
            user_data = data[data['userId'] == args['userId']]
            # update user's location
            user_data['locations'] = user_data['locations'].values[0].append(args['location'])

            # save
            data.to_csv('users.csv', index=False)
            return{'data':data.to_dict()}, 200
        
        else:
            return{
                'message': f"'{args['userId']}' user not found."
            }, 404

    # DELETE
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required = True)
        args = parser.parse_args()

        data = pd.read_csv('users.csv')

        if args['userId'] in list(data['userId']):
            data = data[data['userId'] != args['userId']]
            data.to_csv('users.csv', index=False)
            return{'data':data.to_dict()}, 200
        else:
            return{
                'message': f"'{args['userId']}' user not found."
            }, 404


class Locations(Resource):
    def get(self):
        data = pd.read_csv('locations.csv') # read CSV
        return{'data': data.to_dict()}, 200 # return data and 200 OK code
    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('locationId', required = True, type = int)
        parser.add_argument('name', required = True)
        parser.add_argument('rating', required = True)
        args = parser.parse_args()

        data = pd.read_csv('loactions.csv')
        if args['locationId'] in list(data['locationId']):
            return{
                'message':f"'{args['locationId']}' already exists."
            }, 401
        else:
            new_data = pd.DataFrame({
                'locaitonId':args['locationId'],
                'name': args['name'],
                'rating': args['rating']
            })

            data = data.append(new_data, ignore_index=True)
            data.to_csv('locaitons.csv', index=False)
            return{'data':data.to_dict()}, 200

    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('locationId', required = True, type = int)
        parser.add_argument('name', required = True)
        parser.add_argument('rating', required = True)
        args = parser.parse_args()

        data = pd.read_csv('locations.csv')

        if args['locationId'] in list(data['locationId']):
            user_data = data[data['locationId']== args['locationId']]

            if 'name' in args:
                user_data['name'] = args['name']
            
            if 'rating' in args:
                user_data['rating'] = args['rating']

            data[data['locationId']== args['locationId']] = user_data

            data.to_csv('locations.csv', index=False)
            return {'data':data.to_dict()}, 200
        else:
            return{
                'message':f"'{args['locationId']}' location does not exist."
            }, 404

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('locationId', required =True, type = int)
        args = parser.parse_args()

        data = pd.read_csv('locations.csv')

        if args['locationId'] in list(data['locationsId']):
            data = data[data['locationId'] != args['locationId']]
            data.to_csv('locations.csv', index=False)
            return{'data':data.to_dict()}, 200
        else:
            return{
                'message':f"'{args['locationId']}' locaiton does not exist."
            }

api.add_resource(Users, '/users') # '/users' is entry point
api.add_resource(Locations, '/locations') # '/users' is entry point


if __name__ == '__main__':
    app.run() # run Flask app
