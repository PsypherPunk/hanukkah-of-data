#!/usr/bin/env python3

import re
from typing import Optional

import polars

COLOUR = re.compile(r"^.+\(([a-z]+)\).*$")
COLOURLESS_DESC = re.compile(r"^(.+) \([a-z]+\).*$")
CUSTOMERID = 8342  # from Puzzle 6.

products = polars.scan_csv("noahs-products.csv")
items = polars.scan_csv("noahs-orders_items.csv")
orders = polars.scan_csv("noahs-orders.csv")
customers = polars.scan_csv("noahs-customers.csv")


def get_colour(desc: str) -> Optional[str]:
    if match := COLOUR.match(desc):
        return match.group(1)


def get_colourless_desc(desc: str) -> Optional[str]:
    if match := COLOURLESS_DESC.match(desc):
        return match.group(1)


coloured = (
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
    .filter(polars.col("ordered") == polars.col("shipped"))
    .filter(polars.col("desc").str.contains(r"\([a-z]+\)"))
    .with_column(polars.col("ordered").str.split(" ").arr.first().alias("ordered_date"))
    .with_column(polars.col("desc").apply(get_colour).alias("colour"))
    .with_column(polars.col("desc").apply(get_colourless_desc).alias("colourless_desc"))
    .with_column(
        polars.col("ordered").str.strptime(polars.Datetime, fmt="%Y-%m-%d %H:%M:%S")
    )
    .with_column(
        polars.col("shipped").str.strptime(polars.Datetime, fmt="%Y-%m-%d %H:%M:%S")
    )
)

girlfriend_orders = coloured.filter(polars.col("customerid") == CUSTOMERID)

non_girlfriend_orders = coloured.filter(polars.col("customerid") != CUSTOMERID)

(phone,) = (
    girlfriend_orders.join(
        non_girlfriend_orders,
        on="ordered_date",
        how="inner",
    )
    .filter(polars.col("colourless_desc") == polars.col("colourless_desc_right"))
    .filter(polars.col("colour") != polars.col("colour_right"))
    .filter(
        (polars.col("ordered").dt.hour() - polars.col("ordered_right").dt.hour()) <= 1
    )
    .select("phone_right")
    .collect()["phone_right"]
)

print(f"Can you figure out her ex-boyfriend's phone number? {phone}")
