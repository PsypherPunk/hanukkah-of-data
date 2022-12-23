#!/usr/bin/env python3

import csv

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

with open("noahs-customers.csv") as i:
    customers = csv.DictReader(i)

    pi = next(
        c
        for c in customers
        if "".join(phone.get(l, "0") for l in c["name"].split()[-1].lower())
        == c["phone"].replace("-", "")
    )

print(f"Can you find this private investigator's phone number? {pi['phone']}")
