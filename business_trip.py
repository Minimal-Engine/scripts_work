import os
import datetime
from pathlib import Path
from json import dump
import shutil
import logging

# Konfiguration des Loggings
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_onedrive_path() -> str:
    """Holt den OneDrive-Pfad des Benutzers aus den Umgebungsvariablen und verweist direkt auf den second_brain_work-Ordner."""
    onedrive_env_var = os.getenv('OneDriveCommercial') or os.getenv('OneDrive')
    if not onedrive_env_var:
        raise EnvironmentError("OneDrive path not found in environment variables")
    return os.path.join(onedrive_env_var, 'second_brain_work')


def get_trip_data(user_trip_path: str) -> dict:
    """Fragt die Reisedaten vom Benutzer ab und gibt sie als Dictionary zurück."""
    trip_data = {}
    trip_data["trip_base_folder"] = Path(user_trip_path)

    # Startdatum
    start_date = input("Start Business-Trips: (LEER für heute, Format: YYYY-MM-DD) ")
    if start_date == "":
        start_date = datetime.datetime.today().strftime('%Y-%m-%d')
    else:
        try:
            # Validierung des Datumsformats
            datetime.datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Ungültiges Datum. Bitte im Format YYYY-MM-DD eingeben.")
    trip_data["start_date"] = start_date

    # Anzahl der Übernachtungen
    numberofnights = input("Anzahl der Übernachtungen (ENTER für Eine): ")
    if numberofnights == "":
        numberofnights = 1
    else:
        try:
            numberofnights = int(numberofnights)
            if numberofnights < 0:
                raise ValueError("Die Anzahl der Übernachtungen darf nicht negativ sein.")
        except ValueError:
            raise ValueError("Bitte eine gültige Zahl für die Übernachtungen eingeben.")
    trip_data["numberofnights"] = numberofnights

    # Enddatum berechnen
    start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    if numberofnights == 0:
        stop_date_obj = start_date_obj  # Stop-Date ist identisch mit Start-Date
    else:
        stop_date_obj = start_date_obj + datetime.timedelta(days=numberofnights)
    stop_date = stop_date_obj.strftime('%Y-%m-%d')
    trip_data["stop_date"] = stop_date

    # Land des Business-Trips
    country_location = input("Land des Business-Trips (LEER für DE): ")
    if country_location == "":
        country_location = "DE"
    trip_data["country_location"] = country_location

    # Stadt des Business-Trips
    city_name = input("Stadt des Business-Trips (LEER für Berlin): ")
    if city_name == "":
        city_name = "Berlin"
    trip_data["city_name"] = city_name

    # Firma oder Anlass des Business-Trips
    trip_name = input("Firma oder Anlass des Business-Trips (LEER für Meeting): ")
    if trip_name == "":
        trip_name = "Meeting"
    trip_data["trip_name"] = trip_name

    # Auftragsnummer
    order_number = input("Auftragsnummer, Z-Nummer (optional): ")
    trip_data["order_number"] = order_number

    # Ordnerstruktur für die Reise
    trip_data_folders = {
        "hotel": True,
        "public_transport": True,
        "taxi_ridehailing": True,
        "car_rental": True,
        "flight": True,
        "meal_expense": True
    }
    trip_data["trip_data_folders"] = trip_data_folders

    return trip_data


def make_tripfolder(input_trip_data: dict) -> dict:
    """Erstellt das Verzeichnis und die Dateien für den Business-Trip."""
    os.chdir(input_trip_data["trip_base_folder"])
    trip_folder = Path(input_trip_data["start_date"] + "_" + input_trip_data["country_location"] + "_" + input_trip_data["city_name"] + "_" + input_trip_data["trip_name"])

    if trip_folder.exists():
        shutil.rmtree(trip_folder)

    trip_folder.mkdir(parents=True, exist_ok=True)

    for key, value in input_trip_data["trip_data_folders"].items():
        if value:
            (trip_folder / key).mkdir(exist_ok=True)

    output_trip_data = input_trip_data
    output_trip_data["trip_folder"] = str(trip_folder)

    md_file = trip_folder / (
        input_trip_data["start_date"] + "_"
        + input_trip_data["country_location"] + "_"
        + input_trip_data["city_name"] + "_"
        + input_trip_data["order_number"] + "_"
        + input_trip_data["trip_name"] + ".md")

    with open(md_file, 'w') as f:
        f.write("---\n")
        f.write("tags:\n")
        f.write("- dienstreise\n")
        f.write(f"- {input_trip_data['country_location']}\n")
        f.write(f"- {input_trip_data['city_name']}\n")
        f.write(f"- {input_trip_data['order_number']}\n")
        f.write("alias:\n")
        f.write("---\n")
        f.write(f"# {input_trip_data['start_date']}\n\n")
        f.write(f"# {input_trip_data['stop_date']}\n")
        f.write(f"## {input_trip_data['order_number']}\n")

    output_trip_data["md_file"] = str(md_file)

    json_file = trip_folder / "trip_data.json"
    with open(json_file, 'w') as f:
        dump(output_trip_data, f, indent=4, default=str)
    output_trip_data["json_file"] = str(json_file)

    logging.info("Folgende Informationen wurden in der JSON-Datei gespeichert:")
    logging.info(output_trip_data)
    return output_trip_data


if __name__ == "__main__":
    try:
        user_trip_path = os.path.join(get_onedrive_path(), '00_ORG', '00_04_BUSINESS-TRIPS')
        logging.info(f'Folgendes Verzeichnis wird für die Business-Trips verwendet: {Path(user_trip_path)}')
        trip_data = get_trip_data(user_trip_path)
        make_tripfolder(trip_data)
    except Exception as e:
        logging.error(f"Ein Fehler ist aufgetreten: {e}")