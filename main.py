import requests
from flask import Flask, render_template, request, redirect
from bs4 import BeautifulSoup
app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def home():



        return render_template('index.html')



@app.route("/details", methods = ["POST","GET"])
def details():
    if request.method == "POST":
        location = request.form["place"]
        response = requests.get(
           f"https://api.weatherapi.com/v1/current.json?key=c06274bfc57f4655906104744220406&q={location.capitalize()}&aqi=no").json()
        print(response)
        temperature = response["current"]["temp_c"]
        localtime = response["location"]["localtime"]
        humidity = response["current"]["humidity"]
        condition = response["current"]["condition"]["text"]
        condition_url = response["current"]["condition"]["icon"]

        return render_template("details.html", inputUser=request.form)
    else:
        return render_template('details.html')

if __name__=="__main__":
    app.run(debug=True)

#location = input("Enter a city : ")

response = requests.get(
    f"https://flight.easemytrip.com/FlightList/Index?srch=BOM-Mumbai-India|DEL-NewDelhi-%20India|24/06/2022&px=1-0-0&cbn=0&ar=undefined&isow=true&isdm=true&lang=&&IsDoubleSeat=false").text

soup = BeautifulSoup(response, "lxml")


#print(response)

#india = response.json()
#for item in india["location"]:
    #print(item, india["location"][item])
