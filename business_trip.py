import os

# OneDrive folder location (can be customized if needed)
onedrive_folder = os.path.join(os.environ["USERPROFILE"], "OneDrive")
dienstreisen_folder = os.path.join(onedrive_folder, "Dienstreisen")

# Check if OneDrive folder exists
if not os.path.exists(onedrive_folder):
    print("OneDrive folder not found. Script cannot continue.")

# Check if Dienstreisen folder exists within OneDrive
if not os.path.exists(dienstreisen_folder):
    # Create Dienstreisen folder
    os.makedirs(dienstreisen_folder)
    print("Dienstreisen folder created successfully!")

else:
    print("Dienstreisen folder already exists.")