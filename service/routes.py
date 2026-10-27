@products.route("/products/<int:product_id>", methods=["GET"])
def read_product(product_id):
    """Return one product by ID."""
    product = Product.find(product_id)
    if product is None:
        return jsonify(error="Product not found"), 404
    return _product_payload(product), 200


@products.route("/products/<int:product_id>", methods=["PUT", "PATCH"])
def update_product(product_id):
    """Update supplied fields of an existing product."""
    product = Product.find(product_id)
    if product is None:
        return jsonify(error="Product not found"), 404

    data = request.get_json(silent=True) or {}
    if "name" in data:
        if not data["name"]:
            return jsonify(error="Product name cannot be empty"), 400
        product.name = data["name"]
    if "description" in data:
        product.description = data["description"]
    if "price" in data:
        try:
            price = float(data["price"])
            if price < 0:
                raise ValueError
        except (TypeError, ValueError):
            return jsonify(error="Price must be a non-negative number"), 400
        product.price = price
    if "available" in data:
        if not isinstance(data["available"], bool):
            return jsonify(error="available must be a boolean"), 400
        product.available = data["available"]
    if "category" in data:
        category = _category_from_payload(data["category"])
        if category is None:
            return jsonify(error="Invalid product category"), 400
        product.category = category

    product.update()
    return _product_payload(product), 200


@products.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    """Delete a product by ID."""
    product = Product.find(product_id)
    if product is None:
        return jsonify(error="Product not found"), 404
    product.delete()
    return "", 204


@products.route("/products", methods=["GET"])
def list_products():
    """List all products, optionally filtered by name, category, or availability."""
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        results = Product.find_by_name(name)
    elif category:
        results = Product.find_by_category(category)
    elif available is not None:
        normalized = available.strip().lower()
        if normalized not in ("true", "false"):
            return jsonify(error="available must be true or false"), 400
        results = Product.find_by_availability(normalized == "true")
    else:
        results = Product.all()

    return jsonify([product.serialize() for product in results]), 200
