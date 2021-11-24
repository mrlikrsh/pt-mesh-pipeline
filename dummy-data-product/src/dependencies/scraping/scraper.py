from numpy import NaN
import requests
from bs4 import BeautifulSoup
import pandas as pd

URL = "https://ppp.gov.ph/project-database/"


def scrape():
    df = pd.DataFrame(columns=["date", "time", "price"])
    result = requests.get(URL)
    if result.ok:
        list_header = []
        data = []
        soup = BeautifulSoup(result.content, "lxml")
        table = soup.find("table", attrs={"class": "table demo toggle-square"})
        for td in table.find_all("th"):
            list_header.append(td.text)
        list_header.append("Project URL")
        for tr in table.find_all("tr"):
            t_row = {}
            for td, th in zip(tr.find_all("td"), list_header):
                t_row[th] = td.text.replace("\n", "").strip()
            if tr.find_all("td").__len__() > 0:
                if tr.find_all("td")[0].find("a") is not None:
                    t_row["Project URL"] = tr.find_all("td")[0].find("a").get("href")
            if "Project URL" in t_row and t_row["Project URL"] != "":
                result = requests.get(t_row["Project URL"])
                if result.ok:
                    print(t_row["Project Name"])
                    soup = BeautifulSoup(result.content, "lxml")
                    div = soup.find_all(
                        "div",
                        class_="su-spoiler su-spoiler-style-fancy su-spoiler-icon-caret",
                    )
                    div1 = div[0].find_all(
                        "div", class_="su-spoiler-content su-clearfix"
                    )
                    for header in div1[0].find_all("h6"):
                        if header.text.strip() == "Region":
                            region = ""
                            name = header.find_next_siblings("ul", limit=1)[-1]
                            for litag in name.find_all("li"):
                                region += litag.text
                            t_row["Region"] = region
                        else:
                            name = header.find_next_siblings("p", limit=1)[-1]
                            if not name.contents[0]:
                                name = header.find_next_siblings("p", limit=2)[-1]
                                if not name.contents[0]:
                                    if (
                                        header.find_next_siblings("p")[0].find("a")
                                        is not None
                                    ):
                                        t_row[header.text.strip()] = (
                                            header.find_next_siblings("p")[0]
                                            .find("a")
                                            .text
                                        )
                                    else:
                                        t_row[header.text.strip()] = ""
                                else:
                                    t_row[header.text.strip()] = name.contents[
                                        0
                                    ].strip()
                            else:
                                t_row[header.text.strip()] = name.contents[0].strip()
                else:
                    print("error")
            data.append(t_row)
        df = pd.DataFrame(data)
        # df.to_csv("data.csv")
    else:
        print("error")
    return df
