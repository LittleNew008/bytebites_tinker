import uuid
from datetime import datetime
from typing import Dict, List


class MenuItem:
    def __init__(self, name: str, price: float, category: str, popularity_rating: float = 0.0):
        self.item_id: str = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.category = category
        self.popularity_rating = popularity_rating

    def update_price(self, new_price: float) -> None:
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        self.price = new_price

    def increment_popularity(self) -> None:
        self.popularity_rating += 1


class Menu:
    def __init__(self):
        self.items: List[MenuItem] = []

    def add_item(self, item: MenuItem) -> None:
        self.items.append(item)

    def get_items_by_category(self, category: str) -> List[MenuItem]:
        matches = [item for item in self.items if item.category == category]
        return sorted(matches, key=lambda item: item.popularity_rating, reverse=True)

    def get_items_grouped_by_category(self) -> Dict[str, List[MenuItem]]:
        categories = dict.fromkeys(item.category for item in self.items)
        return {category: self.get_items_by_category(category) for category in categories}


class Transaction:
    def __init__(self, customer_id: str):
        self.transaction_id: str = str(uuid.uuid4())
        self.customer_id = customer_id
        self.timestamp: datetime = datetime.now()
        self.items: List[MenuItem] = []
        self.status = "init"

    def add_item(self, item: MenuItem) -> None:
        if self.status != "init":
            raise ValueError("Cannot add items after the order has been submitted")
        self.items.append(item)
        item.increment_popularity()

    def calculate_total(self) -> float:
        return sum(item.price for item in self.items)

    def submit_order(self) -> None:
        if self.status != "init":
            raise ValueError("Order has already been submitted")
        self.status = "pending"

    def complete_payment(self) -> None:
        if self.status != "pending":
            raise ValueError("Order must be submitted before payment can be completed")
        self.status = "completed"

    def transaction_status(self) -> str:
        # init during customer adding items
        # pending during customer submit order
        # completed after payment is processed
        return self.status


class Customer:
    def __init__(self, name: str):
        self.customer_id: str = str(uuid.uuid4())
        self.name = name
        self.purchase_history: List[Transaction] = []

    def add_purchase(self, transaction: Transaction) -> None:
        self.purchase_history.append(transaction)

    def is_verified(self) -> bool:
        return len(self.purchase_history) > 0
