Feature: Checkout

  Background:
    Given the user is signed in
    And the cart contains 2 items

  @qase.id=13 @qase.suite=Checkout.Success
  Scenario: Successful checkout
    When the user clicks "Place order"
    Then the order is created

  @qase.id=14 @qase.suite=Checkout.PaymentDeclined
  Scenario: Declined payment
    Given the saved card is expired
    When the user clicks "Place order"
    Then the payment fails with "card_expired"
