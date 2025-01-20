import os           # um Informationen zum Benutzer und für den Ablageordner zu finden
import datetime         # Handler für Reisedatum
import pathlib as path  # Handler für Ordner und Dateien
import json             # Handler zur Erzeugung von JSON-Dateien

trip_data = {}

start_date = input("Start Business-Trips: (LEER für heute)")
if start_date == "":
    start_date = datetime.datetime.today().strftime('%Y-%m-%d')
trip_data.update({"start_date": start_date})

stop_date = input("Enddatum des Business-Trips: ")
if stop_date == "":
    stop_date = start_date
trip_data.update({"stop_date": stop_date})

country_location = input("Land des Business-Trips: ")
if country_location == "":
    country_location = "DE"
trip_data.update({"country_location": country_location})

city_name = input("Stadt des Business-Trips: ")
if city_name == "":
    city_name = "Berlin"
trip_data.update({"city_name": city_name})

if start_date == stop_date:
    need_hotel = False
else:
    need_hotel = True
trip_data_bools = {}

trip_data_bools.update({"need_hotel": need_hotel})

trip_data_bools.update({"public_transport": True})
trip_data_bools.update({"car_rental": True})
trip_data_bools.update({"flight": True})
trip_data_bools.update({"meal_expense": True})

trip_data.update({"trip_data_bools": trip_data_bools})
print(trip_data)

'''
def make_tripfolder (input_trip_data: dict) -> dict:

    # guck ob was zu Startdatum drin steht

    # guck ob was zum Enddatum drin steht

    # guck ob die anderen Variablen abgefragt werden.

    # erzeuge auf dieser Grundlage alle Ordner entsprechend meiner Vogaben

    # erzeuge eine JSON-File und leg sie und das Stammlaufwerk des Business-Trips

    # spuck ein dictionary aus.

    output_trip_data = input_trip_data

    return ('output_trip_data')
'''
