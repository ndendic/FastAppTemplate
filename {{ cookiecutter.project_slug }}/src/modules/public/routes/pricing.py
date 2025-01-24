from fasthtml.common import *
from fasthtml.core import APIRouter
from fasthtml.svg import *
from monsterui import *
from monsterui.franken import *
from config import Settings
from modules.shared.templates import page_template
from ..components.pricing import PricingHeader,PricingTiers,ComparisonSection

rt = APIRouter()
config = Settings()

tiers = [
        {
            "id": "524123",
            "name": "Starter",
            "price": "$49",
            "description": "Perfect for small projects and individual developers",
            "features": [
                "All core features",
                "Up to 5 team members",
                "5GB storage",
                "Basic support",
                "Community access",
            ],
            "highlight": False,
            "cta": "Buy Now",
        },
        {
            "id": "pro",
            "name": "Pro",
            "price": "$99",
            "description": "Best for growing teams and businesses",
            "features": [
                "Everything in Starter",
                "Up to 20 team members",
                "20GB storage",
                "Priority support",
                "API access",
                "Advanced analytics",
            ],
            "highlight": True,
            "cta": "Get Started",
        },
        {
            "id": "enterprise",
            "name": "Enterprise",
            "price": "Custom",
            "description": "For large organizations with custom needs",
            "features": [
                "Everything in Pro",
                "Unlimited team members",
                "Unlimited storage",
                "24/7 dedicated support",
                "Custom integrations",
                "SLA guarantee",
            ],
            "highlight": False,
            "cta": "Contact Sales",
        },
    ]



@rt("/pricing")
@page_template(title=config.app_name + " - Pricing")
def get(request):
    return Div(cls="py-24 lg:py-16")(
        PricingHeader(),
        PricingTiers(tiers),
        ComparisonSection(),
    )
