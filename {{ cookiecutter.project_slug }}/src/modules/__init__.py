from modules.auth.models import Priviledge, Role, RolePriviledge, User
{% if cookiecutter.include_blog == "y" %}
from modules.blog.models import BlogPost
{% endif %}
{% if cookiecutter.include_contact_form == "y" %}
from modules.contact.models import Contact
{% endif %}
{% if cookiecutter.include_subscriptions == "y" %}
from modules.subscriptions.models import (
    Product,
    Subscription,
    SubscriptionInvoice,
    Variant,
)
{% endif %}

from modules.shared.models import BaseTable


__all__ = [
{% if cookiecutter.include_blog == "y" %}
    "BlogPost",
{% endif %}
{% if cookiecutter.include_contact_form == "y" %}
    "Contact",
{% endif %}
{% if cookiecutter.include_subscriptions == "y" %}
    "Product",
    "Subscription",
    "SubscriptionInvoice",
    "Variant",
{% endif %}
    "BaseTable",
    "User",
    "Role",
    "Priviledge",
    "RolePriviledge",
]
