def test_find_by_id(self):
    """It should find a Product by its ID"""
    product = ProductFactory()
    product.create()

    found_product = Product.find(product.id)

    self.assertIsNotNone(found_product)
    self.assertEqual(found_product.id, product.id)
    self.assertEqual(found_product.name, product.name)

    product.delete()


def test_update_product(self):

    """It should update a Product"""

    product = ProductFactory()

    product.create()

    original_name = product.name

    product.name = "Updated Product Name"

    product.update()

    updated_product = Product.find(product.id)

    self.assertIsNotNone(updated_product)

    self.assertNotEqual(updated_product.name, original_name)

    self.assertEqual(updated_product.name, "Updated Product Name")

    product.delete()


def test_delete_product():
    """It should delete a Product."""
    product = ProductFactory()
    product.create()
    product_id = product.id

    product.delete()

    assert Product.find(product_id) is None
