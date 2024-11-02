from flask import Flask, jsonify, request

products =[
    {'id' : 1, 'name': 'product 1'},
     {'id' : 2, 'name': 'product 2'},
]

app = Flask(__name__)

@app.route('/products')
def get_products():
    return jsonify(products)


@app.route('/product/<int:id>')
def get_product(id):
    productl_list= [product for product in products if product['id']==id] # list comprehsion technique
    if len(productl_list)==0:
        return f'Product with id {id} not found', 404
    return jsonify(productl_list[0])


# curl --header "Content-Type: application/json" --request POST --data '{"name":"product 3"}' -v http://localhost:5000/product
@app.route('/product',methods=['POST'])
def post_product():
    #retricve product from the request body
    request_product = request.json

    #generate an Id for the psot 
    new_id = max([product['id'] for product in products] + 1)

    # create a new product
    new_product = {
        'id':new_id,
        'name': request_product['name']
    }

    # Append the new product to our product lsit
    products.append(new_product)

    # return the new product back to the client
    return jsonify(new_product), 201

#curl --header "Content-Type: appplication/json" --request PUT --data '{"name":"product 2" -v http://localhost:5000/product}
@app.route('/product/<int:id>', methods=['PUT'])
def put_prouct(id):

    # Get the request palyload
    updated_product = request.json

    # Find the product with the specific ID
    for product in products:
        if product['id'] == id:
            #Update the product name
            product['name'] = updated_product['name']
            return jsonify(product), 200
    return f'Product with id {id} not found', 404


@app.route('/product/<int:id>', methods=['DELETE'])
def delete_product(id):
    productl_list = [product for product in products if product['id']==id]
    if len(productl_list)==1:
        product.remove()(productl_list[0])
        return f'Product with id {id} deleted',200
    return f'Product with id {id} not found',404

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0')