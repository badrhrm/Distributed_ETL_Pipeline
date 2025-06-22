import os
import shutil
import json
import pytest
import pandas as pd
from load_logic import load_all_data

def make_table_bytes(records):
    """Convertit une liste de dicts en bytes JSON"""
    return json.dumps(records).encode('utf-8')

@pytest.fixture
def sample_data():
    return {
        "books": make_table_bytes([
            {"id": 1, "title": "Book A"},
            {"id": 2, "title": "Book B"}
        ]),
        "users": make_table_bytes([
            {"id": 10, "name": "Alice"},
            {"id": 11, "name": "Bob"}
        ])
    }

@pytest.fixture
def output_dir(tmp_path):
    return str(tmp_path)

def test_load_all_data_success(sample_data, output_dir):
    loaded = load_all_data(sample_data, output_dir)

    # Vérifie que les DataFrames sont correctement chargés
    assert "books" in loaded
    assert isinstance(loaded["books"], pd.DataFrame)
    assert loaded["books"].shape == (2, 2)

    # Vérifie que les fichiers CSV ont été créés
    for table in sample_data:
        path = os.path.join(output_dir, f"{table}.csv")
        assert os.path.exists(path)

        # Relecture pour vérification
        df = pd.read_csv(path)
        assert not df.empty

def test_load_all_data_with_invalid_json(output_dir):
    invalid_data = {
        "broken_table": b"{bad json: true"
    }

    result = load_all_data(invalid_data, output_dir)
    assert "broken_table" not in result  # Doit être ignoré à cause de l'erreur
    csv_path = os.path.join(output_dir, "broken_table.csv")
    assert not os.path.exists(csv_path)
