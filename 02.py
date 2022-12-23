#!/usr/bin/env python3

import csv

with open("noahs-products.csv") as i:
    products = list(csv.DictReader(i))

with open("noahs-orders_items.csv") as i:
    items = {}
    for item in csv.DictReader(i):
        items.setdefault(item["sku"], []).append(item)

with open("noahs-orders.csv") as i:
    orders = {order["orderid"]: order for order in csv.DictReader(i)}

with open("noahs-customers.csv") as i:
    customers = {customer["customerid"]: customer for customer in csv.DictReader(i)}

bagels_cleaner = [product for product in products if product["desc"] == "Coffee, Drip"]
items = [item for bagel in bagels_cleaner for item in items[bagel["sku"]]]
orders = [orders[item["orderid"]] for item in items]
customers = [
    customers[order["customerid"]]
    for order in orders
    if order["ordered"].startswith("2017")
]

customer = next(
    customer
    for customer in customers
    if customer["name"].startswith("J") and customer["name"].split()[-1].startswith("D")
)

print(
    f"…but is there any chance you could find their phone number? {customer['phone']}"
)
