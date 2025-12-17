import os
import requests
import sys
import zipfile
import io
import shutil

# Constants
DATA_DIR = "data"
DATASETS = {
    "on-street-parking-bays.csv": "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/on-street-parking-bays/exports/csv?lang=en&timezone=Australia%2FMelbourne&use_labels=true&delimiter=%2C",
    "on-street-parking-bay-sensors.csv": "https://data.melbourne.vic.gov.au/api/explore/v2.1/catalog/datasets/on-street-parking-bay-sensors/exports/csv?lang=en&timezone=Australia%2FMelbourne&use_labels=true&delimiter=%2C",
}

# 2019 Data URL (ZIP file)
DATASET_2019_URL = "https://opendatasoft-s3.s3.amazonaws.com/downloads/archive/7pgd-bdf2.zip"
DATASET_2019_FILENAME = "On-street_Car_Parking_Sensor_Data_-_2019.csv"

def download_file(url, filepath):
    """Downloads a file from a URL to a local path with a progress bar."""
    print(f"Downloading {filepath}...")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_length = r.headers.get('content-length')
            
            with open(filepath, 'wb') as f:
                if total_length is None: 
                    f.write(r.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    for chunk in r.iter_content(chunk_size=8192): 
                        if chunk: 
                            dl += len(chunk)
                            f.write(chunk)
                            # Progress bar
                            done = int(50 * dl / total_length)
                            sys.stdout.write(f"\r[{'=' * done}{' ' * (50-done)}] {dl//(1024*1024)}MB")
                            sys.stdout.flush()
        print(f"\nSaved to {filepath}")
        return True
    except Exception as e:
        print(f"\nError downloading {filepath}: {e}")
        return False

def download_and_unzip_2019(url, target_dir):
    """Downloads the 2019 ZIP, extracts it, and renames the CSV."""
    zip_path = os.path.join(target_dir, "2019_data.zip")
    print(f"\nProcessing 2019 Data (ZIP Download)...")
    
    if download_file(url, zip_path):
        print("Extracting ZIP file...")
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Find the CSV in the zip
                csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]
                if not csv_files:
                    print("Error: No CSV found in ZIP.")
                    return

                extracted_file = csv_files[0]
                zip_ref.extract(extracted_file, target_dir)
                
                # Move/Rename to expected filename
                src = os.path.join(target_dir, extracted_file)
                dst = os.path.join(target_dir, DATASET_2019_FILENAME)
                if src != dst:
                    if os.path.exists(dst):
                        os.remove(dst)
                    os.rename(src, dst)
                
                print(f"Extracted and saved as {dst}")
                
            # Cleanup ZIP
            os.remove(zip_path)
            print("Removed temporary ZIP file.")
            
        except zipfile.BadZipFile:
            print("Error: Downloaded file is not a valid ZIP.")

def main():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created directory: {DATA_DIR}")

    # 1. Download Standard CSVs
    print("--- Downloading Standard Datasets ---")
    for filename, url in DATASETS.items():
        filepath = os.path.join(DATA_DIR, filename)
        if os.path.exists(filepath):
            print(f"Skipping {filename}: Already exists.")
        else:
            download_file(url, filepath)

    # 2. Download and Handle 2019 ZIP
    target_2019 = os.path.join(DATA_DIR, DATASET_2019_FILENAME)
    if os.path.exists(target_2019):
        print(f"\nSkipping 2019 Data: {DATASET_2019_FILENAME} already exists.")
    else:
        download_and_unzip_2019(DATASET_2019_URL, DATA_DIR)

    print("\nAll downloads complete!")

if __name__ == "__main__":
    main()
