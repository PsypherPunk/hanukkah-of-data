#!/usr/bin/env python3

import polars

items = polars.scan_csv("noahs-orders_items.csv")
orders = polars.scan_csv("noahs-orders.csv")
customers = polars.scan_csv("noahs-customers.csv")

(phone,) = (
    orders.join(
        items,
        on="orderid",
        how="inner",
    )
    .groupby(["customerid", "sku"])
    .agg([polars.count()])
    .select("*")
    .groupby(["customerid"])
    .agg([polars.count()])
    .sort("count", reverse=True)
    .first()
    .join(
        customers,
        on="customerid",
        how="inner",
    )
    .first()
    .select("phone")
    .collect()["phone"]
)

print(f"Can you find the collector's phone number in time? {phone}")
