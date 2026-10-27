from behave import given
import requests


@given("the following products")
def load_products(context):
    """Create the products listed in the feature's data table."""
    if not hasattr(context, "table") or context.table is None:
        raise AssertionError("The step requires a Gherkin data table")

    for row in context.table:
        product = {
            "name": row["name"],
            "description": row["description"],
            "price": float(row["price"]),
            "available": row["available"].strip().lower() == "true",
            "category": row["category"],
        }
        response = requests.post(
            "{}/products".format(context.base_url.rstrip("/")),
            json=product,
            timeout=10,
        )
        assert response.status_code == 201, (
            "Could not load product {!r}: {} {}".format(
                product["name"], response.status_code, response.text
            )
        )
