import requests
import time

# The URL where your Flask app is running
# If running locally for testing, use http://localhost:5000
# If running inside Minikube, you'll need the Minikube IP
BASE_URL = "http://localhost:5000/products"

sample_products = [
    {
        "ProductID": "101",
        "ProductName": "Quantum Laptop",
        "ProductCategory": "Electronics",
        "Price": 1200.50,
        "AvailableQuantity": 10,
        "Description": "A high-end laptop with quantum processing power and 32GB RAM."
    },
    {
        "ProductID": "102",
        "ProductName": "Ergonomic Chair",
        "ProductCategory": "Furniture",
        "Price": 299.99,
        "AvailableQuantity": 25,
        "Description": "Breathable mesh office chair with lumbar support and adjustable armrests."
    },
    {
        "ProductID": "103",
        "ProductName": "Wireless Headphones",
        "ProductCategory": "Electronics",
        "Price": 150.00,
        "AvailableQuantity": 50,
        "Description": "Noise-canceling over-ear headphones with 40-hour battery life."
    },
    {
        "ProductID": "104",
        "ProductName": "Smart Coffee Maker",
        "ProductCategory": "Appliances",
        "Price": 89.00,
        "AvailableQuantity": 15,
        "Description": "Programmable coffee maker with app control and thermal carafe."
    },
    {
        "ProductID": "105",
        "ProductName": "Mechanical Keyboard",
        "ProductCategory": "Electronics",
        "Price": 110.00,
        "AvailableQuantity": 30,
        "Description": "RGB backlit mechanical keyboard with tactile blue switches."
    }
]

def seed_database():
    print("Starting to seed database...")
    for product in sample_products:
        try:
            response = requests.post(BASE_URL, json=product)
            if response.status_code == 201:
                print(f"Successfully added: {product['ProductName']}")
            else:
                print(f"Failed to add {product['ProductName']}: {response.text}")
        except Exception as e:
            print(f"Error connecting to API: {e}")
            break

if __name__ == "__main__":
    seed_database()