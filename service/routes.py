"""REST endpoints for the product catalog."""

from flask import Blueprint, jsonify, request

from service.models import Category, Product


products = Blueprint("products", __name__)


def _category_from_payload(value):
    """Convert an enum name or display value into a Category."""
    if isinstance(value, Category):
        return value
    if not isinstance(value, str):
        return None
    try:
        return Category[value.upper()]
    except KeyError:
        for category in Category:
            if category.value.lower() == value.lower():
                return category
        return None


def _product_payload(product):
    return jsonify(product.serialize())


@products.route("/products", methods=["POST"])
def create_product():
    """Create a product from a JSON request body."""
    if not request.is_json:
        return jsonify(error="Content-Type must be application/json"), 415

    data = request.get_json() or {}
    if not data.get("name"):
        return jsonify(error="Product name is required"), 400

    category = _category_from_payload(data.get("category", "UNKNOWN"))
    if category is None:
        return jsonify(error="Invalid product category"), 400

    try:
        price = float(data.get("price", 0))
        if price < 0:
            raise ValueError
    except (TypeError, ValueError):
        return jsonify(error="Price must be a non-negative number"), 400

    available = data.get("available", False)
    if not isinstance(available, bool):
        return jsonify(error="available must be a boolean"), 400

    product = Product(
        name=data["name"],
        description=data.get("description", ""),
        price=price,
        available=available,
        category=category,
    )
    product.create()
    return _product_payload(product), 201


@products.route("/products", methods=["GET"])
def list_products():
    """List all products or filter by name, category, or availability."""
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        results = Product.find_by_name(name)
    elif category:
        category_value = getattr(Category, category.upper(), None)
        results = Product.find_by_category(category_value) if category_value else []
    elif available is not None:
        available_value = available.lower() in ["true", "yes", "1"]
        results = Product.find_by_availability(available_value)
    else:
        results = Product.all()

    return jsonify([product.serialize() for product in results]), 200


@products.route("/products/<int:product_id>", methods=["GET"])
def read_product(product_id):
    """Return one product by ID."""
    product = Product.find(product_id)
    if product is None:
        return jsonify(error="Product not found"), 404
    return _product_payload(product), 200


@products.route("/products/<int:product_id>", methods=["PUT", "PATCH"])
def update_product(product_id):
    """Update a product using JSON data."""
    if not request.is_json:
        return jsonify(error="Content-Type must be application/json"), 415

    product = Product.find(product_id)
    if product is None:
        return jsonify(error="Product not found"), 404

    data = request.get_json() or {}
    if "price" in data:
        try:
            price = float(data["price"])
            if price < 0:
                raise ValueError
        except (TypeError, ValueError):
            return jsonify(error="Price must be a non-negative number"), 400
    if "name" in data and not data["name"]:
        return jsonify(error="Product name cannot be empty"), 400
    if "available" in data and not isinstance(data["available"], bool):
        return jsonify(error="available must be a boolean"), 400
    if "category" in data and _category_from_payload(data["category"]) is None:
        return jsonify(error="Invalid product category"), 400

    product.deserialize(data)
    product.id = product_id
    product.update()
    return _product_payload(product), 200


@products.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Delete a product; return 204 whether or not it existed."""
    product = Product.find(product_id)
    if product is not None:
        product.delete()
    return "", 204
