from flask import Flask, request, jsonify
import requests
import uuid
from functools import lru_cache

app = Flask(__name__)

# E-commerce company codes
companies = ["AMZ", "FLP", "SNP", "MYN", "AZO"]

# Registration data
registration_data = {'companyName': 'renubotique', 
'clientID': 'b42be82a-dff0-4085-a662-027c539829da',
 'clientSecret': 'NxzzbChehTbYJkuc', 
 'ownerName': 'Renu Bhargavi Pudi', 
 'ownerEmail': 'renubhargavipudi@gmai.com', 
 'rollNo': '20kb1a05c8'}

# Register with the test server
response = requests.post("http://20.244.56.144/test/register", json=registration_data)
credentials = response.json()

# Function to fetch products from an e-commerce company
@lru_cache(maxsize=128)
def fetch_products(company, category, min_price, max_price, top_n):
    url = "http://20.244.56.144/test/companies/:companyname/categories/categoryname/products?topnaminpri ce=p&maxPrice="
    params = {
        "top": top_n,
        "minPrice": min_price,
        "maxPrice": max_price
    }
    response = requests.get(url, params=params)
    return response.json()

# Helper function to generate a unique product ID
def generate_product_id(company, product_name):
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, company + product_name))

# GET /categories/<categoryname>/products
@app.route('/categories/<categoryname>/products', methods=['GET'])
def get_products(categoryname):
    n = int(request.args.get('n', 10))
    page = int(request.args.get('page', 1))
    min_price = request.args.get('minPrice', 0)
    max_price = request.args.get('maxPrice', float('inf'))
    sort_by = request.args.get('sortBy')
    order = request.args.get('order', 'asc')

    all_products = []
    for company in companies:
        products = fetch_products(company, categoryname, min_price, max_price, n * page)
        for product in products:
            product_id = generate_product_id(company, product['productName'])
            product.update({'company': company, 'productID': product_id})
            all_products.append(product)
    
    if sort_by:
        all_products.sort(key=lambda x: x[sort_by], reverse=(order == 'desc'))

    start = (page - 1) * n
    end = start + n
    paginated_products = all_products[start:end]
    
    return jsonify(paginated_products)

# GET /categories/<categoryname>/products/<productid>
@app.route('/categories/<categoryname>/products/<productid>', methods=['GET'])
def get_product_details(categoryname, productid):
    for company in companies:
        products = fetch_products(company, categoryname, 0, float('inf'), 100)
        for product in products:
            if generate_product_id(company, product['productName']) == productid:
                return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
