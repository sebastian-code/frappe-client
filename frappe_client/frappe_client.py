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
        """Helper method to build any URL for API calls.

        :param doctype: A string with the name of the doctype, with the same capitalization used in the instance.
        """

        return f"{self.url}/api/resource/{doctype}"

    def __api_call__(self, method, doctype, payload):
        """Main method to build API calls on top of it for simpler calls to the API, through the instance of client.

        :param method: Recieves a string with the name of the intended HTML verb (POST, GET).
        :param doctype: A string with the name of the doctype, with the same capitalization used in the instance.
        :param payload: A value with the information for the API call.
        """
        if method and method.upper() == "POST":
            return self.session.post(
                self.__build_url__(doctype), data=json.dumps(payload)
            )

        return self.session.get(
            self.__build_url__(doctype), verify=self.verify, params=payload
        )

    def list_doc(
        self,
        doctype,
        fields='"*"',
        filters=None,
        limit_start=0,
        limit_page_length=0,
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

        return self.__api_call__(doctype=doctype, payload=params).json()

    def add_doc(self, doctype, new_record):
        """API call to create a new record of a given DocType.

        :param doctype: A string with the name of the doctype, with the same capitalization used in the instance.
        :param new_record: A dict type element with at least the required fields for the creation of a new record.
        """
        return self.__api_call__(
            method="POST", doctype=doctype, payload=new_record
        ).json()

    def get_doc(self, doctype, name, fields='"*"'):
        """This API call returns a single record from the given instance.

        :param doctype: A string with the name of the doctype, with the same capitalization used in the instance.
        :param name: Primary key identifier, as in `name` of the record.
        :param fields: (Optional) A list/tuple of string elements, containing the names of the required fields in the DocType, with the same capitalization used in the instance.
        """
        return self.__api_call__(
            doctype=f"{doctype}/{name}", payload=json.dumps(fields)
        ).json()
