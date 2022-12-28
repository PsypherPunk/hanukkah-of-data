#!/usr/bin/env python3

import polars

PHONE = {
    "0": None,
    "1": None,
    "2": ["a", "b", "c"],
    "3": ["d", "e", "f"],
    "4": ["g", "h", "i"],
    "5": ["j", "k", "l"],
    "6": ["m", "n", "o"],
    "7": ["p", "q", "r", "s"],
    "8": ["t", "u", "v"],
    "9": ["w", "x", "y", "z"],
}

phone = {l: k for k, v in PHONE.items() for l in v or []}

customers = polars.scan_csv("noahs-customers.csv")

(phone,) = (
    customers.with_column(
        polars.col("name")
        .str.split(" ")
        .arr.last()
        .str.to_lowercase()
        .alias("last_name")
    )
    .with_column(polars.col("phone").str.replace_all("-", "").alias("phone_"))
    .with_column(
        polars.col("last_name")
        .apply(lambda last_name: "".join(phone.get(c, "") for c in last_name))
        .alias("last_name_phone")
    )
    .filter(polars.col("phone_") == polars.col("last_name_phone"))
    .select("phone")
    .collect()["phone"]
)

print(f"Can you find this private investigator's phone number? {phone}")
