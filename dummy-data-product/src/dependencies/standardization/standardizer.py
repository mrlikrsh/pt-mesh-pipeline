from os import replace
from numpy import NaN
import requests
from datetime import datetime, timedelta
import time
import webbrowser
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re

php = 0.020  # currency_conversion
df = pd.read_csv(r"C:\Projects\taiyo\pt-mesh-pipeline\data.csv", na_values=["-", "TBD"])
df.dropna(how="all", inplace=True)
print(df)
data = []
for i in range(len(df)):
    if df["Project Cost"][i] == "-":
        df["Project Cost"][i] = "NULL"
    elif df["Project Cost"][i] == "":
        df["Project Cost"][i] = "NULL"
    else:
        if str(df["Project Cost"][i]).lower().startswith("php"):
            lines = (
                str(df["Project Cost"][i])
                .replace(",", "")
                .replace("Php", "Php ")
                .split()
            )
            amount = re.sub(r"[^0-9^\-\.]+", "", lines[1])
            if type(amount) == str:
                if amount.endswith("."):
                    amount = amount[:-1]
                    amount = float(amount)
            if len(lines) > 2:
                if lines[2].lower().startswith("million"):
                    print(float(amount) * 1000000 * php)
                elif lines[2].lower().startswith("billion"):
                    print(float(amount) * 1000000000 * php)
                else:
                    print(float(amount) * php)
            else:
                print(float(amount) * php)
df.to_csv(r"C:\Projects\taiyo\pt-mesh-pipeline\data.csv")
