from flask_restful import Resource, Api
from app import app
from models import db,Lot

api = Api(app)

class LotResource(Resource):
    def get(self):
        lots = Lot.query.all()
        return {'lots':[(lot.lot_id, lot.prime_loc) for lot in lots]}
      
api.add_resource(LotResource, '/api/lot')
