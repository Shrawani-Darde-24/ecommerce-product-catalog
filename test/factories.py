"""Factory for generating Product test data."""

import factory
from factory.fuzzy import FuzzyChoice, FuzzyDecimal

from service.models import Category, Product


class ProductFactory(factory.Factory):
    """Creates fake products for testing."""

    class Meta:
        """Maps this factory to the Product model."""

        model = Product

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(choices=["Hat", "Shoes", "Big Mac", "Sheets"])
    description = factory.Faker("text")
    price = FuzzyDecimal(0.5, 2000.0, 2)
    available = FuzzyChoice(choices=[True, False])
    category = FuzzyChoice(
        choices=[
            Category.UNKNOWN,
            Category.CLOTHS,
            Category.FOOD,
            Category.HOUSEWARES,
            Category.AUTOMOTIVE,
            Category.TOOLS,
        ]
    )
