import requests


class BaseAPIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def get(self, endpoint:str):
        url = f"{self.base_url}{endpoint}"

        response = self.session.get(url, timeout=10)

        response.raise_for_status()
        return response

    def post(self, endpoint:str, payload:dict):
        url = f"{self.base_url}{endpoint}"

        response= self.session.post(url, json = payload, timeout=10)

        response.raise_for_status()
        return response

    def delete(self, endpoint: str, id: int):
        url = f"{self.base_url}{endpoint}/{id}"

        response = self.session.delete(url, timeout = 10)
        response.raise_for_status()
        return response
        
    def put(self, endpoint: str, payload: dict, id: int):
        url = f"{self.base_url}{endpoint}/{id}"

        response = self.session.put(url, json = payload, timeout = 10)
        response.raise_for_status()
        return response

