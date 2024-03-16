from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    description = db.Column(db.String(500))
    price = db.Column(db.Float)
    category = db.Column(db.String(50), index=True)
    
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category
            }

@app.route('/product', methods=['POST'])
def create_product():
    if not request.json or not 'name' in request.json:
        abort(400)
    product = Product(name=request.json['name'], description=request.json.get('description', ""), price=request.json.get('price', 0.0), category=request.json.get('category', ""))
    db.session.add(product)
    db.session.commit()
    return jsonify({'product': product.serialize}), 201


@app.route('/product/<int:id>', methods=['GET'])
def read_product(id):
    product = Product.query.get(id)
    if product is None:
        abort(404)
    return jsonify({'product': product.serialize})


@app.route('/product/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if product is None:
        abort(404)
    if not request.json:
        abort(400)
    product.name = request.json.get('name', product.name)
    product.description = request.json.get('description', product.description)
    product.price = request.json.get('price', product.price)
    product.category = request.json.get('category', product.category)
    db.session.commit()
    return jsonify({'product': product.serialize})


@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if product is None:
        abort(404)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'result': True})


@app.route('/product/search', methods=['GET'])
def search_product():
    name = request.args.get('name')
    description = request.args.get('description')
    products = Product.query.filter(Product.name.contains(name) | Product.description.contains(description)).all()
    return jsonify({'products': [product.serialize for product in products]})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)