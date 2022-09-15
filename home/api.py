import requests

base_url = "http://127.0.0.1:8000"


class CitAPI:
    @classmethod
    def get_analytics(cls):
        url = f"{base_url}/api/"
        response = requests.request("GET", url).json()
        return response

    @classmethod
    def get_customers(cls, **kwargs):
        url = f"{base_url}/api/customer/"

        search = kwargs.get("search")
        account_status = kwargs.get("acct_status")

        payload = dict()
        payload["search"] = kwargs.get("search")
        payload["account_status"] = kwargs.get("acct_status")

        response = requests.request("GET", url, params=payload).json()
        return response

    @classmethod
    def get_customer_by_id(cls, customer_id):
        url = f"{base_url}/api/customer/{customer_id}/"

        response = requests.request("GET", url).json()
        return response

    @classmethod
    def update_customer(cls, customer_id, **kwargs):
        url = f"{base_url}/api/customer/{customer_id}/"

        payload = dict()
        payload["account_status"] = kwargs.get("active_status")
        payload["limit"] = kwargs.get("limit")

        response = requests.request("PUT", url, data=payload).json()
        return response

    @classmethod
    def get_transfer(cls, **kwargs):
        url = f"{base_url}/api/transfers/"

        payload = dict()
        payload["transfer_type"] = kwargs.get("transfer_type")

        response = requests.request("GET", url, params=payload).json()
        return response

