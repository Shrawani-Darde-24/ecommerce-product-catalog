"""REST route tests for the product catalog."""

import unittest

from service import create_app, db
from tests.factories import ProductFactory


class TestProductRoutes(unittest.TestCase):
    """Test the product REST endpoints."""

    def setUp(self):
        self.app = create_app(
            {
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": "sqlite://",
            }
        )
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_read_product(self):
        """It should read a product by ID."""
        product = ProductFactory()
        product.create()

        response = self.client.get("/products/{}".format(product.id))

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], product.id)
        self.assertEqual(data["name"], product.name)
        self.assertEqual(data["category"], product.category.value)

def test_update_product(self):
    """It should update a product by ID."""
    product = ProductFactory(name="Old Product Name")
    product.create()

    updated_data = {
        "name": "Updated Product Name",
        "description": "Updated product description",
        "price": 24.50,
        "available": False,
    }
    response = self.client.put(
        "/products/{}".format(product.id),
        json=updated_data,
    )

    self.assertEqual(response.status_code, 200)
    data = response.get_json()
    self.assertEqual(data["id"], product.id)
    self.assertEqual(data["name"], updated_data["name"])
    self.assertEqual(data["description"], updated_data["description"])
    self.assertEqual(data["price"], updated_data["price"])
    self.assertFalse(data["available"])


def test_delete_product(self):
    """It should delete a product by ID."""
    product = ProductFactory()
    product.create()

    response = self.client.delete("/products/{}".format(product.id))

    self.assertEqual(response.status_code, 204)
    read_response = self.client.get("/products/{}".format(product.id))
    self.assertEqual(read_response.status_code, 404)


def test_list_all_products(self):
    """It should return all products."""
    products = ProductFactory.create_batch(3)
    for product in products:
        product.create()
    expected_ids = {product.id for product in products}

    response = self.client.get("/products")

    self.assertEqual(response.status_code, 200)
    data = response.get_json()
    returned_ids = {item["id"] for item in data}
    self.assertTrue(expected_ids.issubset(returned_ids))


def test_list_products_by_name(self):
    """It should list products matching a name query."""
    matching_product = ProductFactory(name="Unique Desk Lamp")
    other_product = ProductFactory(name="Office Chair")
    for product in (matching_product, other_product):
        product.create()

    response = self.client.get(
        "/products",
        query_string={"name": "Unique Desk Lamp"},
    )

    self.assertEqual(response.status_code, 200)
    data = response.get_json()
    returned_ids = {item["id"] for item in data}
    self.assertIn(matching_product.id, returned_ids)
    self.assertNotIn(other_product.id, returned_ids)


def test_list_products_by_category(self):
    """It should list products matching a category query."""
    matching_product = ProductFactory(category=ProductCategory.TOOLS)
    other_product = ProductFactory(category=ProductCategory.FOOD)
    for product in (matching_product, other_product):
        product.create()

    response = self.client.get(
        "/products",
        query_string={"category": ProductCategory.TOOLS.value},
    )

    self.assertEqual(response.status_code, 200)
    data = response.get_json()
    returned_ids = {item["id"] for item in data}
    self.assertIn(matching_product.id, returned_ids)
    self.assertNotIn(other_product.id, returned_ids)

def test_list_products_by_availability(self):
    """It should list products matching availability."""
    available_product = ProductFactory(available=True)
    unavailable_product = ProductFactory(available=False)
    for product in (available_product, unavailable_product):
        product.create()

    response = self.client.get(
        "/products",
        query_string={"available": "true"},
    )

    self.assertEqual(response.status_code, 200)
    data = response.get_json()
    returned_ids = {item["id"] for item in data}
    self.assertIn(available_product.id, returned_ids)
    self.assertNotIn(unavailable_product.id, returned_ids)

