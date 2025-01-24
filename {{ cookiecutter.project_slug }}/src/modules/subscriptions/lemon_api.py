import hashlib
import hmac
import os
from datetime import datetime

import dotenv
import requests
from starlette.exceptions import HTTPException
from starlette.requests import Request

from modules.auth.models import User

from .models import (
    Product,
    Subscription,
    SubscriptionInvoice,
    Variant,
)

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
        products_data = response.json().get("data", [])
        for product_data in products_data:
            attributes = product_data["attributes"]
            attributes["id"] = product_data["id"]
            attributes["type"] = product_data["type"]
            print("PRODUCT DATA \n", attributes)
            Product.upsert(data=attributes)
        return products_data
    else:
        response.raise_for_status()


def get_variants():
    url = "https://api.lemonsqueezy.com/v1/variants"
    headers = {
        "Accept": "application/vnd.api+json",
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {lemon_api_key}",
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        variants_data = response.json().get("data", [])
        for variant_data in variants_data:
            attributes = variant_data["attributes"]
            attributes["id"] = variant_data["id"]
            attributes["type"] = variant_data["type"]
            price = variant_data["attributes"]["price"] / 100
            attributes["price_formatted"] = str(price)
            print("VARIANT DATA \n", attributes)
            Variant.upsert(attributes)
        return variants_data
    else:
        response.raise_for_status()


def create_checkout(product_id: str, user_id: str, email: str, user_name: str):
    print(
        "Creating checkout for product_id: ",
        product_id,
        " user_id: ",
        user_id,
        " email: ",
        email,
        " user_name: ",
        user_name,
    )
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
                "checkout_data": {
                    "email": email,
                    "name": user_name,
                    "custom": {"user_id": user_id},
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


def verify_signature(payload: bytes, signature: str) -> bool:
    computed_signature = hmac.new(
        webhook_secret.encode(), payload, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(computed_signature, signature)


def parse_lemon_datetime(date_string: str) -> datetime:
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")


def get_product_role(product_id: str) -> Product:
    product = Product.get(product_id)
    if not product:
        raise HTTPException(status_code=400, detail="Role for this product not found")
    return product


def update_user_role(id: str, subscription: Subscription):
    user = User.get(id, alt_key="id")
    if user:
        if subscription.status == "active" or subscription.status == "on_trial":
            product = Product.get(subscription.product_id)
            user.role = product.role_name
            user.save()
        else:
            user.role = None
            user.save()


def update_or_create_subscription(response: dict) -> Subscription:
    subscription = response["data"]
    subscription_id = subscription["id"]
    subscription_data = subscription["attributes"]
    user_id = response["meta"]["custom_data"]["user_id"]
    existing_subscription = Subscription.get(subscription_id)

    if existing_subscription:
        valid_fields = Subscription.__fields__.keys()
        subscription_data["id"] = subscription_id
        subscription_data["customer_portal"] = subscription_data["urls"][
            "customer_portal"
        ]
        subscription_data["update_payment_method"] = subscription_data["urls"][
            "update_payment_method"
        ]
        subscription_data["customer_portal_update_subscription"] = subscription_data[
            "urls"
        ]["customer_portal_update_subscription"]
        subscription_data.pop("urls")
        for key, value in subscription_data.items():
            if key in [
                "renews_at",
                "ends_at",
                "created_at",
                "updated_at",
                "trial_ends_at",
            ]:
                value = parse_lemon_datetime(value) if value else None
            if key in valid_fields:
                setattr(existing_subscription, key, value)
        subscription = existing_subscription
    else:
        subscription_data["id"] = subscription_id
        subscription_data["renews_at"] = (
            parse_lemon_datetime(subscription_data["renews_at"])
            if subscription_data["renews_at"]
            else None
        )
        subscription_data["ends_at"] = (
            parse_lemon_datetime(subscription_data["ends_at"])
            if subscription_data["ends_at"]
            else None
        )
        subscription_data["created_at"] = parse_lemon_datetime(
            subscription_data["created_at"]
        )
        subscription_data["updated_at"] = parse_lemon_datetime(
            subscription_data["updated_at"]
        )
        subscription_data["trial_ends_at"] = (
            parse_lemon_datetime(subscription_data["trial_ends_at"])
            if subscription_data["trial_ends_at"]
            else None
        )
        subscription_data["customer_portal"] = subscription_data["urls"][
            "customer_portal"
        ]
        subscription_data["update_payment_method"] = subscription_data["urls"][
            "update_payment_method"
        ]
        subscription_data["customer_portal_update_subscription"] = subscription_data[
            "urls"
        ]["customer_portal_update_subscription"]
        if user_id:
            subscription_data["user_id"] = user_id
        subscription_data.pop("urls")
        subscription = Subscription(**subscription_data)
    subscription.save()

    update_user_role(user_id, subscription)

    return subscription


def handle_subscription_event(data: dict):
    update_or_create_subscription(data)


def handle_subscription_payment(data: dict):
    invoice_data = data["data"]["attributes"]
    invoice_id = data["data"]["id"]

    # Check if the invoice already exists
    existing_invoice = SubscriptionInvoice.get(invoice_id)
    if existing_invoice:
        # Update existing invoice
        for key, value in invoice_data.items():
            if key in ["created_at", "updated_at", "refunded_at"]:
                value = parse_lemon_datetime(value) if value else None
            elif key == "urls":
                value = value["invoice_url"]
                key = "invoice_url"
            setattr(existing_invoice, key, value)
        invoice = existing_invoice
    else:
        # Create new invoice
        invoice_data["id"] = invoice_id
        invoice_data["created_at"] = parse_lemon_datetime(invoice_data["created_at"])
        invoice_data["updated_at"] = parse_lemon_datetime(invoice_data["updated_at"])
        invoice_data["refunded_at"] = (
            parse_lemon_datetime(invoice_data["refunded_at"])
            if invoice_data["refunded_at"]
            else None
        )
        invoice_data["invoice_url"] = invoice_data["urls"]["invoice_url"]
        invoice_data.pop("urls")
        invoice = SubscriptionInvoice(**invoice_data)
        SubscriptionInvoice.upsert(invoice.dict())


event_handlers = {
    "subscription_created": handle_subscription_event,
    "subscription_updated": handle_subscription_event,
    "subscription_cancelled": handle_subscription_event,
    "subscription_resumed": handle_subscription_event,
    "subscription_expired": handle_subscription_event,
    "subscription_paused": handle_subscription_event,
    "subscription_unpaused": handle_subscription_event,
    "subscription_payment_success": handle_subscription_payment,
    "subscription_payment_failed": handle_subscription_payment,
    "subscription_payment_refunded": handle_subscription_payment,
    "subscription_payment_recovered": handle_subscription_payment,
}


async def subscription_webhook(request: Request):
    payload = await request.body()
    signature = request.headers.get("X-Signature")

    if not signature:
        raise HTTPException(status_code=400, detail="X-Signature header is missing")

    if not verify_signature(payload, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")

    data = await request.json()
    event_name = data["meta"]["event_name"]

    if event_name in event_handlers:
        event_handlers[event_name](data)

    return {"status": "success"}
