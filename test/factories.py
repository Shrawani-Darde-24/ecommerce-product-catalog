import factory
from service.models import Product, ProductCategory


class ProductFactory(factory.Factory):
    """Creates fake Product objects for tests."""

    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Faker("word")
    description = factory.Faker("sentence")
    price = factory.Faker(
        "pydecimal",
        left_digits=3,
        right_digits=2,
        positive=True,
    )
    available = factory.Faker("boolean")
    category = factory.Faker(
        "random_element",
        elements=list(ProductCategory),
    )
