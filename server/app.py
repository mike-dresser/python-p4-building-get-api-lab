#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = Bakery.query.all()
    result = [bakery.to_dict(rules=('-baked_goods',)) for bakery in all_bakeries]
    return make_response(result, 200)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter_by(id=id).first()
    return bakery.to_dict(), 200

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    all_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return [baked_good.to_dict() for baked_good in all_goods], 200

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_exp = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return most_exp.to_dict(), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
