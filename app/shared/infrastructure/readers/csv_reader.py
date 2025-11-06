"""
Reads CSV files.
Used when trying to read CSV files and map its contents into the database.
"""
from typing import Optional

import httpx
import csv
from io import StringIO

async def read_csv_from_url(url: str, timeout: float = 10.0) -> Optional[list[dict]]:
    """
    Reads a CSV file from a URL.

    :param timeout: Timeout for the HTTP request in seconds.
    :param url: The URL of the CSV file.
    :return: The CSV file contents.
    """
    try:
        # Configure the client with timeout settings
        timeout_config = httpx.Timeout(timeout, connect=10.0)
        async with httpx.AsyncClient(timeout=timeout_config) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            content = response.text

        csv_file = StringIO(content)
        reader = csv.DictReader(csv_file)
        return [row for row in reader]

    except httpx.ConnectTimeout:
        print(f"Connection timeout while trying to fetch CSV from {url}")
        return None
    except httpx.ReadTimeout:
        print(f"Read timeout while trying to fetch CSV from {url}")
        return None
    except httpx.HTTPStatusError as e:
        print(f"HTTP error {e.response.status_code} while fetching CSV from {url}")
        return None
    except httpx.RequestError as e:
        print(f"Network error while fetching CSV from {url}: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error while reading CSV from {url}: {str(e)}")
        return None