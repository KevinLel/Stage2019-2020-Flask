#coding:latin-1

from flask import Flask
from flask_restful import Resource, Api, fields, marshal_with
from models import *

app = Flask(__name__)
api = Api(app)

Immeubles_field = {
    'idProprietaire': fields.String,
    'adresse': fields.String,
    'ville': fields.String,
    'codePostal': fields.String,
    'nombreEtage': fields.String,
}
class ImmeubleAPI(Resource):
    @marshal_with(Immeubles_field)
    def get(self):
        return [d for d in Immeuble.select()]

api.add_resource(ImmeubleAPI, '/api/immeubles/')



if __name__ == '__main__':
    app.run(debug=True)

    