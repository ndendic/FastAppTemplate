from datetime import datetime
from typing import ClassVar, List, Optional
import sqlalchemy
from sqlmodel import Field
from modules.shared.models import BaseTable

class BlogPost(BaseTable, table=True):
    title: str = Field(
        index=True,
        schema_extra={"icon": "type", "input_type": "text"}
    )
    description: str = Field(
        sa_type=sqlalchemy.Text,
        schema_extra={"icon": "align-left", "input_type": "textarea"}
    )
    slug: str = Field(
        unique=True, 
        index=True,
        schema_extra={"icon": "link", "input_type": "text"}
    )
    date: datetime = Field(
        sa_type=sqlalchemy.DateTime(timezone=True),
        schema_extra={"icon": "calendar", "input_type": "date"}
    )
    img_path: Optional[str] = Field(
        default=None,
        schema_extra={"icon": "image", "input_type": "text"}
    )
    content: str = Field(
        sa_type=sqlalchemy.Text,
        schema_extra={"icon": "file-text", "input_type": "markdown"}
    )

    # Metadata
    display_name: ClassVar[str] = "Blog Post"
    sidebar_icon: ClassVar[str] = "file-text"
    default_sort_field: ClassVar[str] = "date"
    table_view_fields: ClassVar[List[str]] = [
        "title",
        "description",
        "slug",
        "date",
    ]
    detail_page_fields: ClassVar[List[str]] = [
        "title",
        "description",
        "slug",
        "date",
        "img_path",
        "content",
        "routes"
    ]
    field_groups: ClassVar[dict[str, List[str]]] = {
        "Basic Info": ["title", "description", "slug", "date"],
        "Content": ["content"],
        "Additional": ["img_path", "routes"]
    }

    def __str__(self):
        return self.title
