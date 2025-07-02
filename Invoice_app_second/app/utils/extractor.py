import re, json
from bs4 import BeautifulSoup

def extract_json_from_output(text: str) -> dict:
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if not match:
        match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON parse error: {e}")
    raise ValueError("No valid JSON object found")

def extract_tables(html: str):
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")
    table_str = "\n\n".join(f"[Table {i}]\n{str(t)}" for i, t in enumerate(tables))
    return tables, table_str, soup
