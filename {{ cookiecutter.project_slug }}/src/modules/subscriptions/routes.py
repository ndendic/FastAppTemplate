import json
import logfire

from fasthtml.common import *
from fasthtml.core import APIRouter
from starlette.responses import RedirectResponse

from modules.auth.models import User
from modules.shared.toaster import add_custom_toast

from .lemon_api import (
    create_checkout,
    get_products,
    get_variants,
    subscription_webhook,
)

logfire.configure()


rt = APIRouter()


@rt("/subs/create-checkout/{product_id}")
def get(request):
    user_data = json.loads(request.session.get("user"))
    product_id = request.path_params.get("product_id", "")
    user: User = User.get(user_data.get("id"))
    data: json = create_checkout(product_id, user.id, user.email, user.full_name)
    buy_now_url = data.get("data", {}).get("attributes", {}).get("url", "URL not found")
    if buy_now_url == "URL not found":
        return add_custom_toast(
            request.session, "Error: Buy Now URL not found", "error"
        )
    return RedirectResponse(buy_now_url)


@rt("/api/subs/webhook")
async def post(request):
    return await subscription_webhook(request)


@rt("/subs/products")
def get(request):
    get_products()
    get_variants()
    return add_custom_toast(request.session, "Products and Variants updated", "success")
