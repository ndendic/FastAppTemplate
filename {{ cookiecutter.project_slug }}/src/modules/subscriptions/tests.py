import os

import dotenv
import requests

dotenv.load_dotenv()
lemon_api_key = os.getenv("LEMONSQEEZY_API_KEY")
store_id = os.getenv("LEMONSQEEZY_STORE_ID")
webhook_secret = os.getenv("LEMONSQEEZY_WEBHOOK_SECRET")


def get_products():
    url = "https://api.lemonsqueezy.com/v1/products"
    params = {"filter[store_id]": store_id}
    headers = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {lemon_api_key}",
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def get_variants():
    url = "https://api.lemonsqueezy.com/v1/products"
    headers = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {lemon_api_key}",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def create_checkout(product_id: str, id: str, email: str, user_name: str):
    url = "https://api.lemonsqueezy.com/v1/checkouts"
    headers = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {lemon_api_key}",
    }
    data = {
        "data": {
            "type": "checkouts",
            "attributes": {
                # "checkout_options": {"embed": True},
                "checkout_data": {
                    "email": email,
                    "name": user_name,
                    "custom": {"id": id},
                },
            },
            "relationships": {
                "store": {
                    "data": {"type": "stores", "id": store_id},
                },
                "variant": {"data": {"type": "variants", "id": product_id}},
            },
        }
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200 or response.status_code == 201:
        return response.json()
    else:
        response.raise_for_status()


# data: json = create_checkout("524123", "123456789","marko@gmail.com", "Marko Markovic")
# print(data)
# buy_now_url = data.get("data", {}).get("attributes", {}).get("url", "URL not found")
products = get_products()
variants = get_variants()
# print("Products:\n", products.get("data"))
# print("Variants:\n", variants.get("data"))
