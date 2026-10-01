from models import Customer, Menu, MenuItem, Transaction


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

    try:
        item.update_price(-1)
        assert False, "expected ValueError"
    except ValueError:
        pass
