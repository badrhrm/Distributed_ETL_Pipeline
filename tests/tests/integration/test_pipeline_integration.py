import pytest
import os
import pandas as pd
import shutil
from extraction_logic import extract_all_data
from transformation_logic import load_and_clean_data, transform_all_data, save_results
from load_logic import load_all_data

@pytest.fixture
def setup_environment(monkeypatch, tmp_path):
    # Configuration d'une fausse base pour extraction
    os.environ['DB_SERVER'] = 'localhost'
    os.environ['DB_DATABASE'] = 'fake'
    os.environ['DB_USERNAME'] = 'user'
    os.environ['DB_PASSWORD'] = 'pass'

    # Création de faux fichiers CSV si besoin
    csv_file = tmp_path / "physical_shop_sales.csv"
    csv_file.write_text("Date,Book Title,Quantity,Unit Price\n2023-01-01,Book A,2,12.0")

    # Simuler le bon chemin vers le fichier CSV
    base_path = tmp_path.parent
    monkeypatch.setattr("extraction_logic.os.path.dirname", lambda x=None: str(base_path))
    monkeypatch.setattr("extraction_logic.os.path.exists", lambda path: True)
    monkeypatch.setattr("extraction_logic.pd.read_csv", lambda path: pd.read_csv(csv_file))

    return tmp_path

def test_pipeline_end_to_end(setup_environment, tmp_path):
    # Simule l'extraction (remplace la connexion DB par CSV uniquement ici)
    extracted = extract_all_data()
    assert "physical_shop_sales" in extracted

    # Transformation
    online_df, physical_df = load_and_clean_data(extracted)
    transformed = transform_all_data(online_df, physical_df)

    # Sauvegarde dans output/
    output_dir = tmp_path / "output"
    save_results(transformed, output_dir=str(output_dir))

    # Chargement simulé depuis les fichiers transformés
    data_for_loading = {}
    for file in os.listdir(output_dir):
        path = os.path.join(output_dir, file)
        data_for_loading[file.replace(".csv", "")] = open(path, 'rb').read()

    loaded = load_all_data(data_for_loading, output_dir=str(output_dir))
    assert "combined" in loaded
    assert not loaded["combined"].empty
