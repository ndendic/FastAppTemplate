from typing import ClassVar

from sqlmodel import Field

from modules.shared.models import BaseTable


class Contact(BaseTable, table=True):
    display_name: ClassVar[str] = "Contact Messages"
    sidebar_icon: ClassVar[str] = "mail"

    name: str = Field(..., title="Name")
    email: str = Field(..., title="Email")
    subject: str = Field(..., title="Subject")
    message: str = Field(..., title="Message", schema_extra={"input_type": "textarea"})

    table_view_fields = ["name", "email", "subject", "created_at"]
    detail_page_fields = ["name", "email", "subject", "message", "created_at"]

    field_groups = {
        "Contact Information": ["name", "email"],
        "Message Details": ["subject", "message"],
    }
