#!/usr/bin/env python3

import itertools
import pathlib
import urllib.request
import zipfile

path = pathlib.Path().resolve() / "noahs-csv.zip"

if not path.exists():
    request = urllib.request.Request("https://hanukkah.bluebird.sh/5783/noahs-csv.zip")
    request.add_header(
        "User-Agent",
        "hanukkah-of-data",
    )
    with urllib.request.urlopen(request) as r:
        body = r.read()
        with open(path, "wb") as o:
            o.write(body)

with zipfile.ZipFile("noahs-csv.zip") as z:
    for password in itertools.count():
        try:
            _ = [z.open(info, pwd=str(password).encode("utf-8")) for info in z.filelist]
        except:
            continue
        else:
            print(
                f"What's the password to open the .zip files on the USB drive? {password}"
            )
            break
