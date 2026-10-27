"""Tests for the Product model."""

import unittest

from service import create_app, db
from service.models import Product
from tests.factories import ProductFactory


class TestProductModel(unittest.TestCase):
    """Exercise the Product model's CRUD and query methods."""

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

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _create_products(self, count):
        products = ProductFactory.create_batch(count)
        for product in products:
            product.id = None
            product.create()
        return products

    def test_read_a_product(self):
        """It should Read a Product."""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)

        found_product = Product.find(product.id)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.description, product.description)
        self.assertEqual(found_product.price, product.price)

    def test_update_a_product(self):
        """It should Update a Product."""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)

        product.description = "testing"
        original_id = product.id
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.description, "testing")

        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, original_id)
        self.assertEqual(products[0].description, "testing")

    def test_delete_a_product(self):
        """It should Delete a Product."""
        product = ProductFactory()
        product.id = None
        product.create()
        self.assertEqual(len(Product.all()), 1)

        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        """It should List all Products in the database."""
        self.assertEqual(Product.all(), [])

        self._create_products(5)
        self.assertEqual(len(Product.all()), 5)

    def test_find_by_name(self):
        """It should Find a Product by Name."""
        products = self._create_products(5)
        name = products[0].name
        expected_count = sum(product.name == name for product in products)

        found = Product.find_by_name(name)
        self.assertEqual(found.count(), expected_count)
        for product in found:
            self.assertEqual(product.name, name)

    def test_find_by_category(self):
        """It should Find Products by Category."""
        products = self._create_products(10)
        category = products[0].category
        expected_count = sum(product.category == category for product in products)

        found = Product.find_by_category(category)
        self.assertEqual(found.count(), expected_count)
        for product in found:
            self.assertEqual(product.category, category)

    def test_find_by_availability(self):
        """It should Find Products by Availability."""
        products = self._create_products(10)
        available = products[0].available
        expected_count = sum(product.available == available for product in products)

        found = Product.find_by_availability(available)
        self.assertEqual(found.count(), expected_count)
        for product in found:
            self.assertEqual(product.available, available)
