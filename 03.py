#!/usr/bin/env python3

from datetime import date

import polars

customers = polars.scan_csv("noahs-customers.csv", parse_dates=True)

ARIES_START = date(1970, 3, 20).timetuple().tm_yday
ARIES_END = date(1970, 4, 20).timetuple().tm_yday

CITYSTATEZIP = "South Ozone Park, NY 11420"  # from Puzzle 2.

(phone,) = (
    customers.filter(polars.col("citystatezip") == CITYSTATEZIP)
    .filter(polars.col("birthdate").dt.ordinal_day().is_between(ARIES_START, ARIES_END))
    .filter((polars.col("birthdate").dt.year() - 1910) % 12 == 0)
    .select("phone")
    .collect()["phone"]
)

print(
    f"Can you find the phone number of the person that the contractor gave the rug to? {phone}"
)
