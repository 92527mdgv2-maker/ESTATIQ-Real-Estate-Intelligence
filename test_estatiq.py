from pathlib import Path
import unittest

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


class TestESTATIQ(unittest.TestCase):

    def test_raw_zillow_dataset_exists(self):
        self.assertTrue(
            (DATA_DIR / "zillow_city.csv").is_file(),
            "The original Zillow dataset is missing."
        )

    def test_cleaned_dataset_exists(self):
        self.assertTrue(
            (DATA_DIR / "zillow_cleaned.csv").is_file(),
            "Run explore_data.py to generate the cleaned dataset."
        )

    def test_cleaned_dataset_structure(self):
        df = pd.read_csv(
            DATA_DIR / "zillow_cleaned.csv",
            nrows=10
        )
        self.assertIn("RegionName", df.columns)
        self.assertIn("State", df.columns)
        self.assertIn("RegionID", df.columns)

    def test_model_results_exist(self):
        self.assertTrue(
            (DATA_DIR / "model_results.csv").is_file()
        )

    def test_model_results_are_valid(self):
        results = pd.read_csv(DATA_DIR / "model_results.csv")

        self.assertFalse(results.empty)
        self.assertIn("Model", results.columns)
        self.assertIn("MAE", results.columns)
        self.assertIn("RMSE", results.columns)

        self.assertTrue(
            (pd.to_numeric(results["MAE"], errors="coerce") >= 0).all()
        )
        self.assertTrue(
            (pd.to_numeric(results["RMSE"], errors="coerce") >= 0).all()
        )

    def test_model_predictions_exist(self):
        self.assertTrue(
            (DATA_DIR / "model_predictions.csv").is_file()
        )

    def test_model_predictions_not_empty(self):
        predictions = pd.read_csv(
            DATA_DIR / "model_predictions.csv",
            nrows=10
        )
        self.assertFalse(predictions.empty)

    def test_xgboost_and_lightgbm_models_exist(self):
        results = pd.read_csv(DATA_DIR / "model_results.csv")
        model_names = results["Model"].astype(str).str.lower()
        self.assertTrue(model_names.str.contains("xgboost").any())
        self.assertTrue(model_names.str.contains("lightgbm").any())


if __name__ == "__main__":
    unittest.main()
    