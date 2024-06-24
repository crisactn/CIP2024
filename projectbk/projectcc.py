import sys
import requests
import json
from fpdf import FPDF
import re
from datetime import date


def main():
    year = 2024
    d = input("Enter date: ")
    input_date = input_d(d,year)
    dolar,euro = convert_curr(input_date,year)
    curr_from, curr_to, q_from = conv_par()
    convertion,exchange = print_conv(dolar,euro, curr_from, curr_to, q_from)
    ppdf(convertion,exchange,input_date)

def input_d(d,year):
    #Validate input date, format and range for year given. Return date validated.
    while True:
        try:
            year1, month, day = d.split("-")
            dt = date(int(year1), int(month), int(day))
            if date(year,1,1) <= dt <= date.today():
                break
            else:
                print(f"Enter a valid date for year {year}: YYYY-MM-DD")
                d = input("Enter date: ")
            if re.search(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$", d):
                year1, month, day = d.split("-")
                dt = date(int(year1), int(month), int(day))
            else:
                print(f"Enter a valid date for year {year}: YYYY-MM-DD")
                d = input("Enter date: ")
        except:
            pass
    return str(date(int(year1), int(month), int(day)))

def convert_curr(input_date,year):
    #validate if json file that contain the data to be iterated exists, if not retreive data from web.
    today = str(date.today())
    try:
        with open("dolar.json", "r") as d:
            dolarv = json.load(d)
        with open("euro.json", "r") as e:
            eurov = json.load(e)
        us = dolarv["Dolares"]
        eu = eurov["Euros"]
    except:
        sys.exit("could not load json file")

    for usd in us:
        if today in usd["Fecha"]:
            value1 = True
        else:
            value1 = False
    for eur in eu:
        if today in eur["Fecha"]:
            value2 = True
        else:
            value2 = False
    if not value1 and not value2:
        try:
            json_data(year)
        except:
            sys.exit("Failed to resolve'api.sbif.cl'")
    try:
        with open("dolar.json", "r") as d:
            dolarv = json.load(d)
        with open("euro.json", "r") as e:
            eurov = json.load(e)
        us = dolarv["Dolares"]
        eu = eurov["Euros"]
    except:
        sys.exit("could not load json file")

    #find and return value for specified date.
    for usd in us:
        if input_date in usd["Fecha"]:
            dolar = float(usd["Valor"].replace(',', '.'))
    for eur in eu:
        if input_date in eur["Fecha"]:
            euro = float(eur["Valor"].replace(',', '.'))
    try:
        return dolar,euro
    except:
        sys.exit("value not found for specified date")

def json_data(year):
    #get data for dolar and euro with api for specified year in json format
    keys = {"apikey":"e6680d9a8a481244ae4953cce568e48354f5763f","formato":"json"}
    get_dolar = requests.get("https://api.sbif.cl/api-sbifv3/recursos_api/dolar/" + str(year), params=keys)
    get_euro = requests.get("https://api.sbif.cl/api-sbifv3/recursos_api/euro/" + str(year), params=keys)

    dolarv = get_dolar.json()
    eurov = get_euro.json()
    with open("dolar.json", "w") as file:
        json.dump(dolarv, file, indent=2)

    with open("euro.json", "w") as file:
        json.dump(eurov, file, indent=2)

def conv_par():
    #retrieve parameters of currency to be converted and amount. Return values.
    while True:
        try:
            curr_from = input("Enter currency you want to convert from: USD for 'US Dolar', EUR for 'Euro' , CLP for 'Chilean peso': ").lower()
            curr = ["usd","clp","eur"]
            if curr_from in curr:
                break
            #curr_from = "clp"
        except:
            print("Enter USD EUR or CLP")

    while True:
        try:
            curr_to = input("Enter currency you want to convert to: USD, EURO, CLP: ").lower()
            curr = ["usd","clp","eur"]
            if curr_to in curr:
                break
            #curr_to = "clp"
        except:
            print("Enter USD EUR or CLP")

    while True:
        try:
            q_from = float(input(f"Enter amount of {curr_from}: "))
            if q_from > 0:
                break
            #q_from = 1000
        except:
            print("Enter a valid amount")
    return curr_from, curr_to, q_from

def print_conv(dolar,euro,curr_from, curr_to, q_from):
    #Convert amount of currency given to either, Euro, Dolar or peso, to the specified currency. Return variable with output to print.
    clp = int("1")
    usd_usd = int("1")
    usd_euro = float(dolar/euro)
    usd_clp = float(dolar/clp)
    euro_usd = float(euro/dolar)
    euro_euro = int("1")
    euro_clp = float(euro/clp)
    clp_usd = float(dolar)
    clp_euro = float(euro)
    clp_clp = int("1")
    USD = str("USD").lower()
    EUR = str("EUR").lower()
    CLP = str("CLP").lower()

    if curr_from == USD and curr_to == USD:
        q_to = q_from * usd_usd
    elif curr_from == USD and curr_to == EUR:
        q_to = q_from * usd_euro
    elif curr_from == USD and curr_to == CLP:
        q_to = int(q_from * usd_clp)
    elif curr_from == EUR and curr_to == USD:
        q_to = q_from * euro_usd
    elif curr_from == EUR and curr_to == CLP:
        q_to = int(q_from * euro_clp)
    elif curr_from == EUR and curr_to == EUR:
        q_to = q_from * euro_euro
    elif curr_from == CLP and curr_to == USD:
        q_to = q_from / clp_usd
    elif curr_from == CLP and curr_to == CLP:
        q_to = int(q_from * clp_clp)
    elif curr_from == CLP and curr_to == EUR:
        q_to = q_from / clp_euro
    else:
        print("no value to return")
    convertion = f"{q_from:,.2f} {curr_from.upper()} = {q_to:,.2f} {curr_to.upper()}"
    exchange = q_to/q_from
    print(convertion)
    print("See file report.pdf")
    return convertion,exchange


#Print personal info for final project in pdf format
def ppdf(convertion,exchange, input_date):
    #Print data of convertion in PDF format
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 22)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 15, "Stanford", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 15, "Code in place 2024 == Final project", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.set_font_size(13)
    pdf.set_text_color(100, 100, 100)
    pdf.text(x=32, y=55, text=f"Currency converter for CLP (Chilean peso), USD (US Dolar) & EUR (Euro)")
    pdf.text(x=32, y=65, text=f"Your convertion here:")
    pdf.text(x=40, y=75, text=f"{convertion}")
    pdf.text(x=40, y=85, text=f"The exchange rate is {exchange} for date {input_date}")
    pdf.output("report.pdf")


if __name__ == "__main__":
    main()
