from fasthtml.common import *
from fasthtml.svg import *
from monsterui.franken import *


def contact_form():
    return Card(
        Form(cls="space-y-2", method="post")(
            Grid(
                LabelInput(
                    "Name",
                    id="name",
                    name="name",
                    required=True,
                ),
                LabelInput(
                    "Email",
                    id="email",
                    name="email",
                    type="email",
                    required=True,
                ),
                cols=2,
                gap=4,
            ),
            LabelInput(
                "Subject",
                id="subject",
                name="subject",
                required=True,
            ),
            LabelTextArea(
                "Message",
                id="message",
                name="message",
                rows="4",
                required=True,
            ),
            Button(
                "Send Message",
                cls=ButtonT.primary,
                hx_post="/contact",
                hx_target="#content",
                # hx_swap_oob=True,
            ),
        )
    )
