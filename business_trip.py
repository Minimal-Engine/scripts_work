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

    start_date = input("Start Business-Trips: (LEER für heute)")
    if start_date == "":
        start_date = datetime.datetime.today().strftime('%Y-%m-%d')
    trip_data["start_date"] = start_date

    numberofnights = input("Anzahl der Übernachtungen (ENTER für Eine): ")
    if numberofnights == "":
        numberofnights = 1
    else:
        numberofnights = int(numberofnights)

    stop_date = (datetime.datetime.today() + datetime.timedelta(days=numberofnights)).strftime('%Y-%m-%d')
    trip_data["stop_date"] = stop_date
    trip_data["numberofnights"] = numberofnights

    country_location = input("Land des Business-Trips: ")
    if country_location == "":
        country_location = "DE"
    trip_data["country_location"] = country_location

    city_name = input("Stadt des Business-Trips: ")
    if city_name == "":
        city_name = "Berlin"
    trip_data["city_name"] = city_name

    trip_name = input("Firma oder Anlass des Business-Trips: ")
    if trip_name == "":
        trip_name = "Meeting"
    trip_data["trip_name"] = trip_name

    order_number = input("Auftragsnummer, Z-Nummer:")
    trip_data["order_number"] = order_number

    trip_data_folders = {
        "hotel": True,
        "public_transport": True,
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