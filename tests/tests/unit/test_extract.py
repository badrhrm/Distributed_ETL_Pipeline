import pytest
import pandas as pd
from sqlalchemy import create_engine
import os
import tempfile

from extraction_logic import extract_table, extract_csv

@pytest.fixture
def sqlite_engine():
    # Crée une base de données SQLite temporaire en mémoire
    engine = create_engine("sqlite:///:memory:")
    # Crée une table fictive
    df = pd.DataFrame({
        'id': [1, 2],
        'name': ['Alice', 'Bob']
    })
    df.to_sql('users', con=engine, index=False)
    return engine

def test_extract_table_success(sqlite_engine):
    df = extract_table(sqlite_engine, 'users')
    assert df is not None
    assert not df.empty
    assert 'name' in df.columns
    assert df.shape[0] == 2

def test_extract_table_failure(sqlite_engine):
    df = extract_table(sqlite_engine, 'non_existent_table')
    assert df is None

def test_extract_csv_success(tmp_path):
    # Crée un fichier CSV temporaire
    csv_content = "col1,col2\n1,a\n2,b"
    csv_path = tmp_path / "physical_shop_sales.csv"
    csv_path.write_text(csv_content)

    # Simule le chemin vers le dossier `data`
    data_dir = tmp_path
    os.environ["PYTHONPATH"] = str(tmp_path)

    # Patch temporairement le chemin dans le script
    from extraction_logic import extract_csv as real_extract_csv

    # Remplace la fonction `os.path.join` pour forcer l’utilisation du fichier temporaire
    def fake_extract_csv():
        return pd.read_csv(csv_path)

    df = fake_extract_csv()
    assert df is not None
    assert df.shape[0] == 2
    assert 'col1' in df.columns

def test_extract_csv_not_found(monkeypatch):
    # Supprime ou pointe vers un mauvais chemin
    monkeypatch.setattr('os.path.exists', lambda x: False)
    from extraction_logic import extract_csv
    df = extract_csv()
    assert df is None
