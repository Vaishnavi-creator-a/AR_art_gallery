from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Dummy data for paintings
paintings = [
    {
        "id": 1, 
        "name": "Sunset Bliss", 
        "category": "Nature", 
        "price": 200, 
        "image": "static/images/sunset.jpg",
        "description": "A breathtaking sunset painting capturing the golden hour over a serene landscape.",
        "collection_id": 1
    },
    {
        "id": 2, 
        "name": "City Lights", 
        "category": "Urban", 
        "price": 250, 
        "image": "static/images/city.jpg",
        "description": "An urban landscape painting showcasing the vibrant energy of city life at night.",
        "collection_id": 2
    },
    {
        "id": 3, 
        "name": "Ocean Breeze", 
        "category": "Nature", 
        "price": 300, 
        "image": "static/images/ocean.jpg",
        "description": "A calming seascape that brings the tranquility of the ocean into your space.",
        "collection_id": 1
    }
]

# Dummy data for collections
collections = [
    {
        "id": 1,
        "name": "Nature's Beauty",
        "description": "A collection of stunning landscape paintings capturing the essence of nature.",
        "image": "static/images/nature-collection.jpg"
    },
    {
        "id": 2,
        "name": "Urban Stories",
        "description": "Contemporary paintings depicting the dynamic energy of city life.",
        "image": "static/images/urban-collection.jpg"
    }
]

cart = []

@app.route('/')
def home():
    return render_template('index.html', paintings=paintings, collections=collections)

@app.route('/collections')
def collections_page():
    return render_template('collections.html', collections=collections)

@app.route('/collection/<int:collection_id>')
def collection(collection_id):
    collection_paintings = [p for p in paintings if p['collection_id'] == collection_id]
    collection = next((c for c in collections if c['id'] == collection_id), None)
    if not collection:
        return "Collection not found", 404
    return render_template('category.html', paintings=collection_paintings, collection=collection)

@app.route('/product/<int:painting_id>')
def product(painting_id):
    painting = next((p for p in paintings if p['id'] == painting_id), None)
    if not painting:
        return "Painting not found", 404
    return render_template('product.html', painting=painting)

@app.route('/category/<category>')
def category(category):
    filtered_paintings = [p for p in paintings if p['category'].lower() == category.lower()]
    return render_template('category.html', paintings=filtered_paintings)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    painting_id = request.json.get('id')
    painting = next((p for p in paintings if p['id'] == painting_id), None)
    if painting:
        cart.append(painting)
        return jsonify({"message": "Painting added to cart!", "cart": cart})
    return jsonify({"message": "Painting not found!"}), 404

@app.route('/cart')
def view_cart():
    return render_template('cart.html', cart=cart)

@app.route('/room_view/<int:painting_id>')
def room_view(painting_id):
    painting = next((p for p in paintings if p['id'] == painting_id), None)
    if not painting:
        return "Painting not found", 404
    return render_template('room_view.html', painting=painting)

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    painting_id = request.json.get('id')
    global cart
    cart = [item for item in cart if item['id'] != painting_id]
    return jsonify({"message": "Item removed from cart!", "cart": cart})

if __name__ == '__main__':
    app.run(debug=True)
