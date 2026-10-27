"""Tests for the product REST API."""

import unittest

from service import create_app, db
from tests.factories import ProductFactory

BASE_URL = "/products"


class TestProductRoutes(unittest.TestCase):
    """Exercise the product API endpoints."""

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

    def _create_products(self, count):
        products = []
        for _ in range(count):
            product = ProductFactory()
            product.id = None
            response = self.client.post(BASE_URL, json=product.serialize())
            self.assertEqual(response.status_code, 201)
            products.append(response.get_json())
        return products

    def _get_product_count(self):
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        return len(response.get_json())

    def test_read_product(self):
        """It should read a product and return its attributes."""
        product = ProductFactory()
        product.id = None
        create_response = self.client.post(BASE_URL, json=product.serialize())
        self.assertEqual(create_response.status_code, 201)
        created = create_response.get_json()

        response = self.client.get("{}/{}".format(BASE_URL, created["id"]))

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["id"], created["id"])
        self.assertEqual(data["name"], product.name)
        self.assertEqual(data["description"], product.description)
        self.assertEqual(data["price"], float(product.price))

    def test_update_product(self):
        """It should update an existing product."""
        test_product = ProductFactory()
        test_product.id = None
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, 201)

        new_product = response.get_json()
        new_product["description"] = "unknown"
        response = self.client.put(
            "{}/{}".format(BASE_URL, new_product["id"]),
            json=new_product,
        )
        self.assertEqual(response.status_code, 200)
        updated_product = response.get_json()
        self.assertEqual(updated_product["description"], "unknown")

    def test_delete_product(self):
        """It should delete a product and decrement the product count."""
        products = self._create_products(5)
        initial_count = self._get_product_count()
        product_id = products[0]["id"]

        response = self.client.delete("{}/{}".format(BASE_URL, product_id))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(response.data), 0)

        response = self.client.get("{}/{}".format(BASE_URL, product_id))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(self._get_product_count(), initial_count - 1)

    def test_get_product_list(self):
        """It should Get a list of Products."""
        self._create_products(5)

        response = self.client.get(BASE_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 5)

    def test_query_by_name(self):
        """It should Query Products by name."""
        products = self._create_products(5)
        name = products[0]["name"]
        expected_count = sum(product["name"] == name for product in products)

        response = self.client.get(BASE_URL, query_string={"name": name})

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), expected_count)
        for product in data:
            self.assertEqual(product["name"], name)

    def test_query_by_category(self):
        """It should Query Products by category."""
        products = self._create_products(10)
        category = products[0]["category"]
        expected_count = sum(product["category"] == category for product in products)

        response = self.client.get(BASE_URL, query_string={"category": category})

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), expected_count)
        for product in data:
            self.assertEqual(product["category"], category)

    def test_query_by_availability(self):
        """It should Query Products by availability."""
        products = self._create_products(10)
        available = products[0]["available"]
        expected_count = sum(product["available"] == available for product in products)

        response = self.client.get(
            BASE_URL,
            query_string={"available": str(available).lower()},
        )

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), expected_count)
        for product in data:
            self.assertEqual(product["available"], available)

