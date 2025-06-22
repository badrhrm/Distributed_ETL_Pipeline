import pandas as pd
import os
import shutil
import pytest

from transformation_logic import (
    load_and_clean_data,
    transform_all_data,
    save_results
)

@pytest.fixture
def mock_data_dictionary():
    # Données simulées pour les tests
    books = pd.DataFrame({
        "book_id": [1, 2],
        "name": ["Book A", "Book B"],
        "category": ["Fiction", "Non-fiction"]
    })

    authors = pd.DataFrame({
        "author_id": [1, 2],
        "name": ["Author A", "Author B"]
    })

    users = pd.DataFrame({
        "user_id": [100, 101],
        "gender": ["Male", "Female"]
    })

    orders = pd.DataFrame({
        "order_id": [1000, 1001],
        "user_id": [100, 101],
        "order_date": ["2023-01-10", "2023-01-15"]
    })

    order_items = pd.DataFrame({
        "order_id": [1000, 1001],
        "book_id": [1, 2],
        "quantity": [2, 1],
        "price_at_order": [15.0, 25.0]
    })

    physical_shop_sales = pd.DataFrame({
        "Date": ["2023-01-05", "2023-01-12"],
        "Book Title": ["Book A", "Book B"],
        "Quantity": [3, 2],
        "Unit Price": [12.0, 20.0]
    })

    return {
        "books": books,
        "authors": authors,
        "users": users,
        "orders": orders,
        "order_items": order_items,
        "physical_shop_sales": physical_shop_sales
    }

def test_load_and_clean_data(mock_data_dictionary):
    online_df, physical_df = load_and_clean_data(mock_data_dictionary)

    # Vérifie la forme des données nettoyées
    assert not online_df.empty
    assert not physical_df.empty

    # Vérifie colonnes clés
    for df in [online_df, physical_df]:
        assert all(col in df.columns for col in ["date", "product_name", "quantity", "price", "shop", "category", "gender"])

def test_transform_all_data(mock_data_dictionary):
    online_df, physical_df = load_and_clean_data(mock_data_dictionary)
    result = transform_all_data(online_df, physical_df)

    assert isinstance(result, dict)
    expected_keys = [
        "combined", "items_by_period", "revenue_by_period", "category_breakdown",
        "top_products", "comparison", "gender_comparison", "favorite_category"
    ]
    for key in expected_keys:
        assert key in result
        assert isinstance(result[key], pd.DataFrame)

    # Vérifie que les colonnes sont bien générées
    assert "revenue" in result["combined"].columns
    assert result["combined"]["revenue"].sum() > 0

def test_save_results_creates_csv(tmp_path, mock_data_dictionary):
    online_df, physical_df = load_and_clean_data(mock_data_dictionary)
    results = transform_all_data(online_df, physical_df)

    output_dir = tmp_path / "test_output"
    save_results(results, output_dir=str(output_dir))

    # Vérifie que tous les fichiers sont bien créés
    expected_files = [
        "combined.csv", "items_by_period.csv", "revenue_by_period.csv",
        "category_breakdown.csv", "top_products.csv", "comparison.csv",
        "gender_comparison.csv", "favorite_category.csv"
    ]

    for file in expected_files:
        assert (output_dir / file).exists()
