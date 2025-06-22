import pytest
from extraction_logic import extract_all_data
from transformation_logic import load_and_clean_data, transform_all_data, save_results
from load_logic import load_all_data
import os

def test_etl_pipeline_performance(benchmark, tmp_path):
    def full_etl():
        extracted = extract_all_data()
        online_df, physical_df = load_and_clean_data(extracted)
        transformed = transform_all_data(online_df, physical_df)
        save_results(transformed, output_dir=str(tmp_path / "output"))
        data_for_loading = {
            k: v.to_json(orient="records").encode("utf-8") for k, v in transformed.items()
        }
        load_all_data(data_for_loading, output_dir=str(tmp_path / "loaded"))

    benchmark(full_etl)
