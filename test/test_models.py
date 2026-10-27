def test_find_by_id(self):
    """It should find a Product by its ID"""
    product = ProductFactory()
    product.create()

    found_product = Product.find(product.id)

    self.assertIsNotNone(found_product)
    self.assertEqual(found_product.id, product.id)
    self.assertEqual(found_product.name, product.name)

    product.delete()
