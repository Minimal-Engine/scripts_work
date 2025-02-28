import os                 # um Informationen zum Benutzer und für den Ablageordner zu finden
import datetime           # Handler für Reisedatum
from pathlib import Path  # Handler für Ordner und Dateien
from json import dump     # Handler für JSON-Dateien

# Hol dir das Onedrive-Laufwerk des Benutzers:

onedrive_env_var = os.getenv('OneDriveCommercial') or os.getenv('OneDrive')
if not onedrive_env_var:
    raise EnvironmentError("OneDrive path not found in environment variables")

user_trip_path = onedrive_env_var + '\\second_brain_work\\00_ORG\\00_04_BUSINESS-TRIPS'

print('Folgendes Verzeichnis wird für die Business-Trips verwendet:')
print(Path(user_trip_path))

# Frag die Reisedaten ab

trip_data = {}
trip_data.update({"trip_base_folder": Path(user_trip_path)})

# Startdatum

start_date = input("Start Business-Trips: (LEER für heute)")
if start_date == "":
    start_date = datetime.datetime.today().strftime('%Y-%m-%d')
trip_data.update({"start_date": start_date})

# Anzahl der Übernachtungen und Enddatum

numberofnights = input("Anzahl der Übernachtungen (ENTER für Eine): ")
if numberofnights == "":
    numberofnights = 1


stop_date = (datetime.datetime.today()+datetime.timedelta(numberofnights)).strftime('%Y-%m-%d')
trip_data.update({"stop_date": stop_date})
trip_data.update({"numberofnights": numberofnights})

# Zielland des Trips

country_location = input("Land des Business-Trips: ")
if country_location == "":
    country_location = "DE"
trip_data.update({"country_location": country_location})

# Zielstand des Trips

city_name = input("Stadt des Business-Trips: ")
if city_name == "":
    city_name = "Berlin"
trip_data.update({"city_name": city_name})

# Anlass oder Firma des Trips

trip_name = input("Firma oder Anlass des Business-Trips: ")
if trip_name == "":
    trip_name = "Meeting"
trip_data.update({"trip_name": trip_name})

# Optional: Auftragsnummer

order_number = input("Auftragsnummer, Z-Nummer:")
trip_data.update({"order_number": order_number})

# Ordnerstruktur für die Reise

trip_data_folders = {}
trip_data_folders.update({"hotel": True})
trip_data_folders.update({"public_transport": True})
trip_data_folders.update({"car_rental": True})
trip_data_folders.update({"flight": True})
trip_data_folders.update({"meal_expense": True})
trip_data.update({"trip_data_folders": trip_data_folders})

# Funktion zum Erstellen des Verzeichnisses und der Dateien


def make_tripfolder(input_trip_data: dict) -> dict:

    # Wechsle ins Basisverzeichnis des Business-Trips

    os.chdir(input_trip_data["trip_base_folder"])

    # Erzeuge ein Verzeichnis Startdatum+Land+Stadt+Anlass

    trip_folder = Path(input_trip_data["start_date"] + "_" + input_trip_data["country_location"] + "_" + input_trip_data["city_name"] + "_" + input_trip_data["trip_name"])
    trip_folder.mkdir(parents=True, exist_ok=True)

    # erzeuge aus dem Dict alle Unterordner die auf True gesetzt sind

    for key, value in input_trip_data["trip_data_folders"].items():
        if value is True:
            (trip_folder / key).mkdir(exist_ok=True)

    # spuck ein dictionary aus, inkusive Pfad zur JSON-Datei

    output_trip_data = input_trip_data
    output_trip_data.update({"trip_folder": str(trip_folder)})

    # Erzeuge eine Markdown-Datei mit den Reisedaten
    md_file = trip_folder / (
        trip_data["start_date"] + "_"
        + trip_data["country_location"] + "_"
        + trip_data["city_name"] + "_"
        + trip_data["order_number"] + "_"
        + trip_data["trip_name"] + ".md")
    with open(md_file, 'w') as f:
        f.write("# " + trip_data["trip_name"] + "\n")
        f.write("## " + trip_data["start_date"] + " - " + trip_data["stop_date"] + "\n")
        f.write("## " + trip_data["country_location"] + " - " + trip_data["city_name"] + "\n")
        f.write("## " + trip_data["order_number"] + "\n")
    output_trip_data.update({"md_file": str(md_file)})

    # erzeuge eine JSON-File, leg sie in das Stammlaufwerk des Business-Trips
    json_file = trip_folder / "trip_data.json"
    with open(json_file, 'w') as f:
        dump(output_trip_data, f, indent=4, default=str)
    output_trip_data.update({"json_file": str(json_file)})

    print("Folgende Informationen wurden in der JSON-Datei gespeichert:")
    print(output_trip_data)
    return (output_trip_data)


make_tripfolder(trip_data)
