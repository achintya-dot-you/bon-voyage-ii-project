from itertools import count
import requests
from flask import Flask, current_app, render_template, request, redirect
from bs4 import BeautifulSoup
app = Flask(__name__)
currency_codes = {
    "United States of America" : "USD",
    "India" : "INR",
    "United Kingdom" : "GBP",
    "United Arab Emirates": "AED",
    "Japan" : "JPY",
    "Australia" : "AUD",
    "Canada" : "CAD",
    "China" : "CNH",
    "Hong Kong" : "HKD",
    "New Zealand" : "NZD"
}


@app.route("/", methods = ['POST', 'GET'])
def home():



        return render_template('index.html')



@app.route("/details", methods = ["POST","GET"])
def details():
    if request.method == "POST":
        location = request.form["place"]
        response = requests.get(
           f"https://api.weatherapi.com/v1/current.json?key=c06274bfc57f4655906104744220406&q={location.capitalize()}&aqi=no").json()

        temperature = response["current"]["temp_c"]
        localtime = response["location"]["localtime"]
        humidity = response["current"]["humidity"]
        condition = response["current"]["condition"]["text"]
        condition_url = response["current"]["condition"]["icon"]
        country = response["location"]["country"]
        country = country.replace(" ", "-").lower()
        locationc = location.replace(" ","-").lower()
        try:
            cost = requests.get(
            f"https://www.budgetyourtrip.com/{country}/{locationc}").text
            soup = BeautifulSoup(cost, "lxml")
            price = soup.find("span", class_="curvalue").text
        except:
            cost = requests.get(
                f"https://www.budgetyourtrip.com/{country}").text
            soup = BeautifulSoup(cost, "lxml")
            price = soup.find("span", class_="curvalue").text



        
        currency = requests.get(
            "https://v6.exchangerate-api.com/v6/8c549f036a43d4ed5d05a979/latest/USD").json()
        try:
            exchangeRate = currency["conversion_rates"][currency_codes[response["location"]["country"]]]
        except:
            exchangeRate = 1
        
        accomodation = soup.find(
            "li", class_="cost-tile cost-tile-category cost-tile-category-accommodation cost-tile-category-1").text
        newList = accomodation.split("Hotel or hostel for one person")
        accomodation = newList[-1]
        accomodation = accomodation.replace("\t","")
        accomodation = accomodation.replace("\n","")
        accomodation = accomodation.replace(" ","")
        accomodation = accomodation.replace(",","")
        accomodation = accomodation[1:]
        price = price.replace(",","")
        accomodationInUSD = int(accomodation)//exchangeRate
        priceInUSD = int(price)//exchangeRate
        totalExpenditure = accomodationInUSD + priceInUSD + 100
        print(priceInUSD)
        data = {
            "temperature" : temperature,
            "humidity" : humidity,
            "localtime" : str(localtime)[10:],
            "condition" : condition,
            "condition_url" : condition_url,
            "country" : country,
            "location" : location.capitalize(),
            "accomodationInUSD" : accomodationInUSD,
            "priceInUSD" : priceInUSD+100,
            "totalExpenditure" : totalExpenditure,
            "currency": currency_codes[response["location"]["country"]],
            "exchangeRate" : exchangeRate

        }




        return render_template("details.html", data = data)
    else:
        return render_template('details.html')

if __name__=="__main__":
    app.run(debug=True)

#location = input("Enter a city : ")

response = requests.get(
    f"https://flight.easemytrip.com/FlightList/Index?srch=BOM-Mumbai-India|DEL-NewDelhi-%20India|24/06/2022&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lang=&&IsDoubleSeat=false").text

soup = BeautifulSoup(response, "lxml")


