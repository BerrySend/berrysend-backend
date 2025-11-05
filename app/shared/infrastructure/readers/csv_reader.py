"""
Reads CSV files.
Used when trying to read CSV files and map its contents into the database.
"""
from dataclasses import dataclass
import requests
import csv
from io import StringIO

@dataclass
class CsvFileReader:

    @staticmethod
    def read(url: str) -> list[dict]:
        """
        Opens a CSV file and returns its contents as a list of dictionaries.

        :param url: The url to access the CSV file.
        :return: The list of dictionaries with the contents of the CSV file.
        """
        response = requests.get(url)
        response.raise_for_status()
        f = StringIO(response.text)
        return list(csv.DictReader(f))