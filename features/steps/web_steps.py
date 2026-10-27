"""Reusable Selenium step definitions for product UI scenarios."""

from behave import given, when, then
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


def _wait_seconds(context):
    return getattr(context, "wait_seconds", 10)


def _field_element(context, field):
    """Find a form field by its label-derived ID, with common ID variants."""
    field_id = field.lower().replace(" ", "_")
    candidates = [field_id, "{}-fld".format(field_id), "{}-field".format(field_id)]
    for candidate in candidates:
        try:
            return context.driver.find_element(By.ID, candidate)
        except NoSuchElementException:
            continue
    raise NoSuchElementException("Could not find field {!r}".format(field))


@given('I visit the "{page}"')
@when('I visit the "{page}"')
def step_visit_page(context, page):
    """Open the requested page in the browser."""
    url = getattr(context, "home_page", None) or getattr(context, "base_url")
    context.driver.get(url)


@when('I press the "{button}" button')
def step_press_button(context, button):
    """Click a page button identified by the course UI's button ID."""
    button_id = button.lower() + "-btn"
    context.driver.find_element(By.ID, button_id).click()


@when('I set the "{field}" to "{value}"')
@when('I change "{field}" to "{value}"')
def step_set_field(context, field, value):
    """Replace the contents of a text field."""
    element = _field_element(context, field)
    element.clear()
    element.send_keys(value)


@when('I select "{value}" in the "{field}" dropdown')
def step_select_dropdown(context, value, field):
    """Select an option from a dropdown by its visible text."""
    Select(_field_element(context, field)).select_by_visible_text(value)


@when('I copy the "{field}" field')
def step_copy_field(context, field):
    """Save a form field's current value for a later paste step."""
    context.copied_field_value = _field_element(context, field).get_attribute("value")


@when('I paste the "{field}" field')
def step_paste_field(context, field):
    """Paste the value saved by the copy-field step."""
    element = _field_element(context, field)
    element.clear()
    element.send_keys(context.copied_field_value)


@then('I should see "{name}" in the results')
def step_should_see_in_results(context, name):
    """Wait until the requested text appears in the search results."""
    found = WebDriverWait(context.driver, _wait_seconds(context)).until(
        EC.text_to_be_present_in_element((By.ID, "search_results"), name)
    )
    assert found


@then('I should not see "{name}" in the results')
def step_should_not_see_in_results(context, name):
    """Assert that the requested text is absent from search results."""
    results = context.driver.find_element(By.ID, "search_results")
    assert name not in results.text


@then('I should see the message "{message}"')
def step_should_see_message(context, message):
    """Wait until the requested text appears in the flash message."""
    found = WebDriverWait(context.driver, _wait_seconds(context)).until(
        EC.text_to_be_present_in_element((By.ID, "flash_message"), message)
    )
    assert found


@then('I should see "{value}" in the "{field}" field')
def step_should_see_value_in_field(context, value, field):
    """Verify the value displayed in a form input."""
    element = WebDriverWait(
        context.driver, _wait_seconds(context)
    ).until(EC.visibility_of(_field_element(context, field)))
    assert element.get_attribute("value") == value


@then('I should see "{value}" in the "{field}" dropdown')
def step_should_see_value_in_dropdown(context, value, field):
    """Verify the selected value displayed in a dropdown."""
    element = WebDriverWait(
        context.driver, _wait_seconds(context)
    ).until(EC.visibility_of(_field_element(context, field)))
    selected = Select(element).first_selected_option.text
    assert selected.lower() == value.lower()

