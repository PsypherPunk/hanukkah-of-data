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
    .filter(polars.col("desc") == "Coffee, Drip")
    .filter(polars.col("ordered").str.starts_with("2017"))
    .filter(polars.col("name").str.to_lowercase().str.starts_with("j"))
    .filter(
        polars.col("name")
        .str.split(" ")
        .arr.last()
        .str.to_lowercase()
        .str.starts_with("d")
    )
    .select("phone")
    .collect()["phone"]
)

print(f"…but is there any chance you could find their phone number? {phone}")
