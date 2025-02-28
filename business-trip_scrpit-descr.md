# Script to generate a folder for a businiess trip

## General desricption

The script shall generate a folder structure for a business-trip, including sub-folders for Transfer, Hotels etc.
Ideally it shall be a function. After executing, the folders shall be generated after the user has entered certain details, including:

- Start (DONE)
- Stop (Buggy, Anzahl der Übernachtungen als int, kann aber nicht weiter zählen)
- Country of Location (DONE)
- City of trip
- Hotel needed
- Taxi/Ride-hailing/Train needed (public_transport)
- Rental Car needed (rental_car)
- Flight needed (flights)
- Meal expenses

It might be a good idea to just pass a json file into that function with all the information.
The script may also generate:

- A Markdown file in the Business-trip-folder with all the information (DONE)
- A calendar entry in outlook (shall be possible locally with outlook.exe-command )
- For GET/MD: The word document containing all relevant information for that trip to send it to my superior an the team-assistant

All mentioned variables shall have 