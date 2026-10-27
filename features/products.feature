Scenario: Read a Product
  When I enter "Classic Notebook" in the "Name" field
  And I click the "Search" button
  Then I should see "Classic Notebook"

Scenario: Update a Product
  When I enter "Classic Notebook" in the "Name" field
  And I click the "Search" button
  And I enter "Updated Classic Notebook" in the "Name" field
  And I click the "Update" button
  Then I should see "Updated Classic Notebook"

Scenario: Delete a Product
  When I enter "Classic Notebook" in the "Name" field
  And I click the "Search" button
  And I click the "Delete" button
  Then I should not see "Classic Notebook"

Scenario: List All Products
  When I click the "List All" button
  Then I should see "Classic Notebook"

Scenario: Search for Products by Category
  When I enter "Tools" in the "Category" field
  And I click the "Search" button
  Then I should see "Classic Notebook"

Scenario: Search for Products by Availability
  When I enter "true" in the "Available" field
  And I click the "Search" button
  Then I should see "Classic Notebook"

Scenario: Search for Products by Name
  When I enter "Classic Notebook" in the "Name" field
  And I click the "Search" button
  Then I should see "Classic Notebook"
