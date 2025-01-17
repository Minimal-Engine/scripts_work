import os
import datetime
import pathlib as path
from subprocess import Popen

# Get OneDrive for Business folder location (modify if needed)
onedrive_folder = os.path.join(os.environ["USERPROFILE"], "OneDrive - BASF")

# Check if OneDrive folder exists
if not os.path.exists(onedrive_folder):
    print("OneDrive for Business folder not found.")
else:
    # Print OneDrive folder location
    print(f"OneDrive for Business folder location: {onedrive_folder}")

    # Open OneDrive folder in Explorer
    Popen(['explorer.exe', onedrive_folder])

today = datetime.date.today()

print((today))
