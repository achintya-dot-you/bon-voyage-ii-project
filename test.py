from bs4 import BeautifulSoup
import requests

req = requests.get(
    "https://www.budgetyourtrip.com/united-states-of-america").text
soup = BeautifulSoup(req, "lxml")
price = soup.find("span", class_="curvalue").text

print(price)
