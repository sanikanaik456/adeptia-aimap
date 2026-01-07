import json
import xml.etree.ElementTree as ET
import pandas as pd
from pathlib import Path


class DataIngestion:
    """
    Handles ingestion and basic preprocessing for CSV, JSON, and XML files.
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def ingest(self):
        if not self.file_path.exists():
            raise FileNotFoundError(f"{self.file_path} not found")

        suffix = self.file_path.suffix.lower()

        if suffix == ".csv":
            return self._read_csv()
        elif suffix == ".json":
            return self._read_json()
        elif suffix == ".xml":
            return self._read_xml()
        else:
            raise ValueError("Unsupported file format")

    def _read_csv(self):
        df = pd.read_csv(self.file_path)
        return {
            "data": df,
            "schema": self._extract_schema(df)
        }

    def _read_json(self):
        with open(self.file_path, "r") as f:
            data = json.load(f)

        df = pd.json_normalize(data)
        return {
            "data": df,
            "schema": self._extract_schema(df)
        }

    def _read_xml(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        records = []
        for child in root:
            record = {elem.tag: elem.text for elem in child}
            records.append(record)

        df = pd.DataFrame(records)
        return {
            "data": df,
            "schema": self._extract_schema(df)
        }

    @staticmethod
    def _extract_schema(df: pd.DataFrame):
        """
        Extracts column names and data types for mapping.
        """
        return {
            col: str(dtype)
            for col, dtype in zip(df.columns, df.dtypes)
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Data Ingestion Module")
    parser.add_argument("--input", required=True, help="Path to input data file")

    args = parser.parse_args()

    ingestion = DataIngestion(args.input)
    result = ingestion.ingest()

    print("Schema:")
    for col, dtype in result["schema"].items():
        print(f"{col}: {dtype}")
