from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from database import products, setup

app = Flask(__name__)
CORS(app)

setup.create_tables()

# Obtine todo los registros de la db
@app.route('/products', methods=['GET'])
def getListProducts():
    productsList = products.select_all_products()
    if(len(productsList) > 0):
        return jsonify({"message": "List Products", "products": productsList})
    return jsonify({"message": "Products No Found"})

# Obtine un solo restro de la base cuando el clinete manda el id
@app.route('/products/<string:id>')
def getProductById(id):
    productFound = products.select_products_by_id(id)
    if(len(productFound) > 0):
        return jsonify({"message": "Producto Found", "product": productFound})
    return jsonify({"message": "Product Not Found"})

# Crea un nuevo registro pasandole los params name_pro y el price
@app.route('/products', methods=['POST'])
def add_product():
    name_pro = request.json['name_pro']
    price = request.json['price']
    create_date = datetime.now().strftime("%x") # 17/03/2022

    data = (name_pro, price, create_date)
    product_id = products.insert_products(data)

    if product_id:
        product = products.select_products_by_id(product_id)
        return jsonify({"message": "Product Created", "product": product})
    return jsonify({"message": "internal error"})

# Actualiza un registro de la base buscando por id y mandandole name_pro y price
@app.route('/products/<string:id>', methods=["PUT"])
def editProduct(id):
    name_pro = request.json['name_pro']
    price =request.json['price']
    data = (name_pro, price)

    if products.edit_product(id, data):
        product = products.select_products_by_id(id)
        return jsonify({"message": "Product Edit", "product": product})
    return jsonify({"message": "internal error"})

# Elimina el registro de la base pasandole el id
@app.route('/products/<string:id>', methods = ['DELETE'])
def deleteProduct(id):
    if products.delete_product(id):
        return jsonify({"message": "Product Deleted"})
    return jsonify({"message": "Internal Error"})


if __name__ == '__main__':
    app.run(debug=True)
