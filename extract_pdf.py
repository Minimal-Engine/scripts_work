from pathlib import Path
import os
from pypdf import PdfReader  # Verwenden von pypdf

# Get the home directory
home = str(Path.home())

# Defining the download folder
download_folder = os.path.join(home, 'Downloads')

def get_pdf_files(directory):
    """Sucht nach PDF-Dateien im angegebenen Verzeichnis."""
    files = Path(directory).rglob('*.pdf')
    return [str(file) for file in files]

def print_pdf_text(file_path):
    """Liest und druckt den Text einer PDF-Datei."""
    try:
        reader = PdfReader(file_path)  # Verwenden von PdfReader aus pypdf
        for page in reader.pages:
            print(page.extract_text())  # Verwenden von extract_text() für jede Seite
    except Exception as e:
        print(f"Unable to open or read file: {file_path}. Error: {e}")

# Suche nach PDF-Dateien im Download-Ordner
pdf_files = get_pdf_files(download_folder)

# Drucke den Text der gefundenen PDF-Dateien
for file in pdf_files:
    print(f"\nFile: {file}")
    print_pdf_text(file)

