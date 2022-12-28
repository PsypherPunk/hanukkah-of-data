#!/usr/bin/env python3

import polars

customers = polars.scan_csv("noahs-customers.csv")
orders = polars.scan_csv("noahs-orders.csv", parse_dates=True)
items = polars.scan_csv("noahs-orders_items.csv")

(phone,) = (
    orders.join(
        items,
        on="orderid",
        how="inner",
    )
    .join(
        customers,
        on="customerid",
        how="inner",
    )
    .filter(polars.col("ordered").dt.year() <= 2019)  # "…that was years ago!"
    .filter(polars.col("sku").str.starts_with("BKY"))  # "…and some pastries…"
    .filter(
        # "…came over at 5am…"
        polars.col("ordered")
        .dt.hour()
        .is_in([3, 4, 5])
    )
    .filter(
        # "…claim the first pastries that came out of the oven."
        polars.col("shipped")
        .dt.hour()
        .is_in([3, 4, 5])
    )
    .groupby(["customerid", "phone"])
    .agg([polars.count()])
    .filter(polars.col("count") > 1)
    .select("phone")
    .collect()["phone"]
)

print(f"Can you find the bicycle fixer's phone number? {phone}")
