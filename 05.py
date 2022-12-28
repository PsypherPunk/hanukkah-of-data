#!/usr/bin/env python3

import polars

products = polars.scan_csv("noahs-products.csv")
items = polars.scan_csv("noahs-orders_items.csv")
orders = polars.scan_csv("noahs-orders.csv")
customers = polars.scan_csv("noahs-customers.csv")

(phone,) = (
    items.join(
        products,
        on="sku",
        how="inner",
    )
    .join(
        orders,
        on="orderid",
        how="inner",
    )
    .join(
        customers,
        on="customerid",
        how="inner",
    )
    .filter(polars.col("citystatezip").str.contains("Queens Village"))
    .filter(polars.col("desc").str.contains("Cat"))
    .groupby(["customerid", "phone"])
    .agg([polars.count()])
    .filter(polars.col("count") > 1)
    .sort("count", reverse=True)
    .first()
    .select("phone")
    .collect()["phone"]
)

print(f"What's the phone number of the woman from Freecycle? {phone}")
