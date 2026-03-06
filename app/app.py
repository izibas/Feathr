from flask import Flask, request, jsonify
from pymongo import MongoClient
from elasticsearch import Elasticsearch
import os

app = Flask(__name__)

# Connection setup using Environment Variables for K8s
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb-service:27017/")
ES_HOST = os.getenv("ES_HOST", "http://elasticsearch-service:9200")

db = MongoClient(MONGO_URI).inventory_db
es = Elasticsearch([ES_HOST])

# --- CRUD Operations ---

@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    # Save full data to Mongo
    db.products.insert_one(data.copy())
    # Save description to ES for search
    es.index(index="products", id=data['ProductID'], body={"Description": data.get('Description', "")})
    return jsonify({"message": "Added"}), 201

@app.route('/products', methods=['GET'])
def list_products():
    # Return everything, hiding the Mongo internal _id
    products = list(db.products.find({}, {"_id": 0}))
    return jsonify(products)

@app.route('/products/<id>', methods=['GET'])
def get_product(id):
    product = db.products.find_one({"ProductID": id}, {"_id": 0})
    return jsonify(product) if product else (jsonify({"err": "Not found"}), 404)

@app.route('/products/<id>', methods=['PUT'])
def update_product(id):
    data = request.json
    db.products.update_one({"ProductID": id}, {"$set": data})
    if 'Description' in data:
        es.update(index="products", id=id, body={"doc": {"Description": data['Description']}})
    return jsonify({"message": "Updated"})

@app.route('/products/<id>', methods=['DELETE'])
def delete_product(id):
    db.products.delete_one({"ProductID": id})
    es.delete(index="products", id=id, ignore=[404])
    return jsonify({"message": "Deleted"})

# --- Search & Analytics ---

@app.route('/products/search', methods=['GET'])
def search():
    query = request.args.get('query')
    res = es.search(index="products", body={"query": {"match": {"Description": query}}})
    return jsonify([hit["_source"] for hit in res['hits']['hits']])

@app.route('/products/analytics', methods=['GET'])
def analytics():
    # Simple Mongo aggregation for count and average price
    pipeline = [{"$group": {"_id": "$ProductCategory", "count": {"$sum": 1}, "avgP": {"$avg": "$Price"}}}]
    results = list(db.products.aggregate(pipeline))
    
    total = sum(item['count'] for item in results)
    # Find the category with the highest count
    popular = max(results, key=lambda x: x['count'])['_id'] if results else "N/A"
    avg_price = sum(item['avgP'] for item in results) / len(results) if results else 0
    
    return jsonify({
        "total_products": total,
        "most_popular_category": popular,
        "average_price": round(avg_price, 2)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)