"""Frappe client core module."""

from base64 import b64encode

from decouple import config
import requests


class FrappeClient:
    API_KEY = config("API_KEY")
    API_SECRET = config("API_SECRET")
    token = str(b64encode(f"{API_KEY}:{API_SECRET}".encode("utf-8")), "utf-8")
    headers = {
        "Authorization": f"Basic {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    def __init__(self, verify=True, url=None):
        self.verify = verify
        self.session = requests.Session()
        self.session.headers = headers
        self.url = url

    def __build_url__(self, doctype):
        return f"{self.url}/api/resource/{doctype}"
