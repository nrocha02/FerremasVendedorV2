# FerremasVendedorV2/services.py
import requests
from django.conf import settings

def get_products():
    url = f"{settings.MONGODB_API_URL}/action/find"
    headers = {
        "Content-Type": "application/json",
        "Access-Control-Request-Headers": "*",
        "api-key": settings.MONGODB_API_KEY
    }
    payload = {
        "dataSource": settings.MONGODB_DATA_SOURCE,
        "database": settings.MONGODB_DATABASE,
        "collection": "producto",
        "projection": {
            "_id": 1,
            "nombre": 1,
            "precio": 1,
            "stock": 1,
            "_class": 1
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    print("URL:", url)
    print("Headers:", headers)
    print("Payload:", payload)
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.content)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()
