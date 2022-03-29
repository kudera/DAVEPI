from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from flask_basicauth import BasicAuth
import pandas as pd
import json

app = Flask(__name__)
api = Api(app)

#authorization details
with open("../config.json") as config:
    config = json.load(config)

app.config['DAVE_API']['BASIC_AUTH_USERNAME']
app.config['DAVE_API']['BASIC_AUTH_PASSWORD']
app.config['DAVE_API']['BASIC_AUTH_FORCE']

basic_auth = BasicAuth(app)
@app.route('/secret')
@basic_auth.required
def secret_view():
    return render_template('secret.html')

#Sites CSV class
class Sites(Resource):
    def get(self):
        data = pd.read_csv('sites.csv')
        data = data.to_dict()
        return {'data': data}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('root_domain', required=True)
        parser.add_argument('domain_authority', required=True)
        parser.add_argument('spam_score', required=True)
        args = parser.parse_args()

        data = pd.read_csv('sites.csv')

        if args['root_domain'] in list(data['root_domain']):
            return {
                'message': f"'{args['root_domain']}' already exists."
            }, 409
        else:
            # create new dataframe containing new values
            new_data = pd.DataFrame({
                'root_domain': [args['root_domain']],
                'domain_authority': [args['domain_authority']],
                'spam_score': [args['spam_score']],
            })
            # add the newly provided values
            data = data.append(new_data, ignore_index=True)
            data.to_csv('sites.csv', index=False)
            return {'data': data.to_dict()}, 200

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('root_domain', required=True)
        args = parser.parse_args()
        
        data = pd.read_csv('sites.csv')
        
        if args['root_domain'] in list(data['root_domain']):
            data = data[data['root_domain'] != args['root_domain']]
            
            data.to_csv('sites.csv', index=False)

            return {'data': data.to_dict()}, 200
        else:
            return {
                'message': f"'{args['root_domain']}' site  not found."
            }, 404


api.add_resource(Sites, '/sites')

if __name__ == '__main__':
    app.run()