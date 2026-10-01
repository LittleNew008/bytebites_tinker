import pytest

from models import Customer, Menu, MenuItem, Transaction


def test_get_items_by_category_filters_out_other_categories():
    menu = Menu()
    burger = MenuItem("Spicy Burger", 7.5, "Food")
    soda = MenuItem("Large Soda", 2.5, "Drinks")
    menu.add_item(burger)
    menu.add_item(soda)

    drinks = menu.get_items_by_category("Drinks")

    assert [item.name for item in drinks] == ["Large Soda"]


def test_get_items_by_category_unknown_category_returns_empty_list():
    menu = Menu()
    menu.add_item(MenuItem("Spicy Burger", 7.5, "Food"))

    assert menu.get_items_by_category("Desserts") == []


def test_get_items_by_category_sorts_by_popularity_descending():
    menu = Menu()
    low = MenuItem("Soda", 2.0, "Drinks", popularity_rating=1)
    high = MenuItem("Juice", 3.0, "Drinks", popularity_rating=9)
    mid = MenuItem("Water", 1.0, "Drinks", popularity_rating=4)
    for item in (low, high, mid):
        menu.add_item(item)

    ordered = menu.get_items_by_category("Drinks")

    assert [item.name for item in ordered] == ["Juice", "Water", "Soda"]


def test_menu_grouping_sorted_by_popularity():
    menu = Menu()
    burger = MenuItem("Spicy Burger", 7.5, "Food", popularity_rating=2)
    fries = MenuItem("Fries", 3.0, "Food", popularity_rating=5)
    soda = MenuItem("Large Soda", 2.5, "Drinks", popularity_rating=1)
    for item in (burger, fries, soda):
        menu.add_item(item)

    grouped = menu.get_items_grouped_by_category()

    assert [item.name for item in grouped["Food"]] == ["Fries", "Spicy Burger"]
    assert [item.name for item in grouped["Drinks"]] == ["Large Soda"]


def test_transaction_total_and_popularity_increment():
    soda = MenuItem("Large Soda", 2.5, "Drinks")
    burger = MenuItem("Spicy Burger", 7.5, "Food")
    customer = Customer("Alice")

    transaction = Transaction(customer.customer_id)
    transaction.add_item(soda)
    transaction.add_item(burger)

    assert transaction.calculate_total() == 10.0
    assert soda.popularity_rating == 1
    assert burger.popularity_rating == 1


def test_calculate_total_for_burger_and_soda_equals_fifteen():
    burger = MenuItem("Burger", 10.0, "Food")
    soda = MenuItem("Soda", 5.0, "Drinks")
    customer = Customer("Alice")
    transaction = Transaction(customer.customer_id)

    transaction.add_item(burger)
    transaction.add_item(soda)

    assert transaction.calculate_total() == 15.0


def test_calculate_total_on_empty_transaction_returns_zero_not_crash():
    customer = Customer("Alice")
    transaction = Transaction(customer.customer_id)

    total = transaction.calculate_total()

    assert total == 0


def test_calculate_total_counts_repeated_item_each_time_added():
    soda = MenuItem("Large Soda", 2.5, "Drinks")
    customer = Customer("Alice")
    transaction = Transaction(customer.customer_id)

    transaction.add_item(soda)
    transaction.add_item(soda)

    assert transaction.calculate_total() == 5.0
    assert soda.popularity_rating == 2


def test_customer_becomes_verified_after_first_purchase():
    customer = Customer("Bob")
    assert customer.is_verified() is False

    transaction = Transaction(customer.customer_id)
    customer.add_purchase(transaction)

    assert customer.is_verified() is True
    assert len(customer.purchase_history) == 1


def test_menu_item_price_update_rejects_negative():
    item = MenuItem("Fries", 3.0, "Food")
    item.update_price(3.5)
    assert item.price == 3.5

    with pytest.raises(ValueError):
        item.update_price(-1)


def test_menu_item_rejects_negative_price_at_creation():
    with pytest.raises(ValueError):
        MenuItem("Fries", -1, "Food")


def test_submit_order_then_complete_payment_transitions_status():
    customer = Customer("Alice")
    transaction = Transaction(customer.customer_id)
    assert transaction.transaction_status() == "init"

    transaction.submit_order()
    assert transaction.transaction_status() == "pending"

    transaction.complete_payment()
    assert transaction.transaction_status() == "completed"


def test_add_item_after_submit_order_raises():
    customer = Customer("Alice")
    transaction = Transaction(customer.customer_id)
    transaction.submit_order()

    with pytest.raises(ValueError):
        transaction.add_item(MenuItem("Soda", 2.5, "Drinks"))


def test_complete_payment_before_submit_order_raises():
    customer = Customer("Alice")
    transaction = Transaction(customer.customer_id)

    with pytest.raises(ValueError):
        transaction.complete_payment()
