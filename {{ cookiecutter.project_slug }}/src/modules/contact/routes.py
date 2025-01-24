from fasthtml.common import *
from fasthtml.core import APIRouter
from fasthtml.svg import *

from modules.contact.components.contact_form import contact_form
from modules.contact.models import Contact
from modules.shared.templates import page_template

rt = APIRouter()


@rt("/contact", methods=["POST"])
async def contact_post(request):
    form_data = await request.form()

    contact = Contact(
        name=form_data.get("name"),
        email=form_data.get("email"),
        subject=form_data.get("subject"),
        message=form_data.get("message"),
        status="new",
    )
    contact.save()

    return Div(
        H1("Thank you for your message! We'll get back to you soon."),
    )


@rt("/contact", methods=["GET"])
@page_template(title="Contact Us")
def contact_page(request):
    return Div(cls="container mx-auto py-8")(
        H1("Contact Us", cls="text-3xl font-bold text-center mb-8"),
        P(
            "Have a question or feedback? We'd love to hear from you.",
            cls="text-gray-600 text-center mb-8",
        ),
        contact_form(),
    )
