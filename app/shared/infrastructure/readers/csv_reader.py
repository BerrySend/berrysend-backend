"""
Reads CSV files.
Used when trying to read CSV files and map its contents into the database.
"""
import httpx
import csv
from io import StringIO

async def read_csv_from_url(url: str) -> list[dict]:
    """
    Reads a CSV file from a URL.

    :param url: The URL of the CSV file.
    :return: The CSV file contents.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        content = response.text

    csv_file = StringIO(content)
    reader = csv.DictReader(csv_file)
    return [row for row in reader]