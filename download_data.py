"""
Script to download the cycling accidents dataset from data.gouv.fr
"""

import requests
from pathlib import Path

def download_dataset():
    """
    Download the BAAC cycling accidents dataset from data.gouv.fr.
    """
    # URL du dataset sur data.gouv.fr
    url = "https://www.data.gouv.fr/api/1/datasets/r/4c75d6c0-c927-48ca-92db-5bcce9f17ae7"
    
    # Créer le dossier data/ s'il n'existe pas
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    output_path = data_dir / "accidentsVelofull.csv"
    
    # Télécharger si le fichier n'existe pas déjà
    if output_path.exists():
        print(f"Dataset already exists at {output_path}")
        print(f"   Size: {output_path.stat().st_size / (1024*1024):.1f} MB")
        return
    
    print(f"Downloading dataset from data.gouv.fr...")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  #Lève une exception si erreur HTTP
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Dataset downloaded successfully!")
        print(f"   Location: {output_path}")
        print(f"   Size: {output_path.stat().st_size / (1024*1024):.1f} MB")
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading dataset: {e}")
        print(f"   Please download manually from:")
        print(f"   https://www.data.gouv.fr/fr/datasets/accidents-de-velo/")

if __name__ == "__main__":
    download_dataset()