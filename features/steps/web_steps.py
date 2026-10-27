from behave import when
from selenium.webdriver.common.by import By


@when('I click the "{button}" button')
def step_click_button(context, button):
    """Click a button or input control by its visible label."""
    xpath = (
        "//button[normalize-space(.)='{0}']"
        " | //input[@type='submit' and @value='{0}']"
        " | //input[@type='button' and @value='{0}']"
    ).format(button)
    context.driver.find_element(By.XPATH, xpath).click()

from behave import then
from selenium.webdriver.common.by import By


@then('I should see "{text}"')
def step_should_see_text(context, text):
    """Assert that the requested text appears on the current page."""
    page_text = context.driver.find_element(By.TAG_NAME, "body").text
    assert text in page_text, "Expected {!r} to be visible on the page".format(text)


@then('I should not see "{text}"')
def step_should_not_see_text(context, text):
    """Assert that the requested text does not appear on the page."""
    page_text = context.driver.find_element(By.TAG_NAME, "body").text
    assert text not in page_text, "Did not expect {!r} to be visible on the page".format(text)


@then('I should see the message "{message}"')
def step_should_see_message(context, message):
    """Assert that a specific status or confirmation message appears."""
    page_text = context.driver.find_element(By.TAG_NAME, "body").text
    assert message in page_text, "Expected message {!r} to be visible on the page".format(message)
