from bs4 import BeautifulSoup
import requests as r
import json
import csv

query = input("Enter the product you want to search: ")
pages = int(input("Enter the number of pages you want to scrap: "))
for page in range(1, pages + 1):
    url = f"https://www.flipkart.com/search?q=${query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    if page > 1:
        url = f"https://www.flipkart.com/search?q={query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={page}"

    def scrap(url):
        res = r.get(url)
        soup = BeautifulSoup(res.text, "html.parser")
        print(soup.prettify())
        get_data(soup)

    def get_data(soup):
        data = soup.find_all("div", class_="tUxRFH")
        items = []
        for i in data:
            temp = {}
            try:
                temp["name"] = i.find("div", class_="KzDlHZ").text

                temp["price"] = i.find("div", class_="Nx9bqj").text.replace(
                    "\u20b9", "Rs."
                ).replace("₹", "Rs.") or i.find("div", class_="_4b5DiR").text.replace(
                    "\u20b9", "Rs."
                ).replace(
                    "₹", "Rs."
                )

                temp["ratings"] = i.find("div", class_="XQDdHH").text

                temp["url"] = (
                    "https://www.flipkart.com" + i.find("a", class_="CGtC98")["href"]
                )

                temp["no_of_ratings"] = (
                    i.find("span", class_="Wphh3N")
                    .find("span")
                    .find("span")
                    .text.replace("\u00a0", "")
                )
                temp["Description"] = "\n".join(
                    [i.text for i in i.find("ul", class_="G4BRas").findAll("li")]
                )
                temp["Discount"] = i.find("div", class_="UkUFwK").find("span").text
                items.append(temp)
            except:
                break
        print(items)
        if page > 1:
            with open("data.json") as f:
                old_data = json.load(f)
            old_data.extend(items)
            items = old_data
        write_data(items)

    def write_data(items):
        with open("data.json", "w") as f:
            json.dump(items, f, indent=4)

    scrap(url)


def convert_to_csv():
    with open("data.json") as f:
        data = json.load(f)
    csv_file = "data.csv"
    with open(csv_file, "a", newline="") as csvfile:
        fieldnames = data[0].keys() if isinstance(data, list) and len(data) > 0 else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        if isinstance(data, list):
            writer.writerows(data)
        else:
            writer.writerow(data)


convert_to_csv()
