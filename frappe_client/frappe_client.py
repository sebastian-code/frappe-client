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

    def __init__(self, url, verify=True):
        self.verify = verify
        self.session = requests.Session()
        self.session.headers = headers
        self.url = url

    def __build_url__(self, command):
        """Helper method to build any URL for API calls.

        :param command: A string with the destination endpoint and its core arguments.
        """
        return f"{self.url}/api/resource/{command}"

    def get_doc(self, doctype, name, fields='"*"'):
        """This API call returns a single record from a given DocType.

        :param doctype: A string with the name of the doctype, with the same capitalization used in the instance.
        :param name: Primary key identifier, as in `name` of the record.
        :param fields: (Optional) A list/tuple of string elements, containing the names of the required fields in the DocType, with the same capitalization used in the instance.
        """
        return self.session.get(
            self.__build_url__(f"{doctype}/{name}"),
            verify=self.verify,
            params=json.dumps(fields),
        ).json()

    def post_doc(self, doctype, payload):
        """API call to create a new record of a given DocType.

        :param doctype: A string with the name of the doctype, with the same capitalization used in the instance.
        :param payload: A dict type element with at least the required fields for the creation of a new record.
        """
        return self.session.post(
            self.__build_url__(doctype), data=json.dumps(payload)
        ).json()

    def put_doc(self, doctype, name, payload):
        """API method call to update a record identified by its `name` and DocType.

        :param doctype: A string with the name of the doctype, with the same capitalization used in the instance.
        :param name: Primary key identifier under the `name` field.
        :param payload: A dict type element with fields to be updated and the new values.
        """
        return self.session.put(
            self.__build_url__(f"{doctype}/{name}"), data=json.dumps(payload)
        ).json()

    def delete_doc(self, doctype, name):
        return self.session.delete(self.__build_url__(f"{doctype}/{name}")).json()

    def list_doc(
        self,
        doctype,
        fields="*",
        filters=None,
        limit_start=None,
        limit_page_length=None,
        order_by=None,
    ):
        """API call method to list the records in a single DocType.

        :param doctype: A string with the name of the doctype, with the same capitalization used in the instance.
        :param fields: (Optional) A list/tuple of string elements, containing the names of the required fields in the DocType, with the same capitalization used in the instance.
        :param filters: (Optional) A list/tuple of tuples with the filters to apply to the query, where each filter is of the format: [field, operator, value]
        :param limit_start: (Optional) Int value with the first position to start the query from.
        :param limit_page_length: (Optional) Int value with the pagination length.
        """
        params = {
            "fields": json.dumps(fields),
        }
        if filters:
            params["filters"] = json.dumps(filters)
        if limit_start:
            params["limit_start"] = limit_start
        if limit_page_length:
            params["limit_page_length"] = limit_page_length
        if order_by:
            params["order_by"] = order_by

        return self.session.get(self.__build_url__(f"{doctype}"), params=params).json()
