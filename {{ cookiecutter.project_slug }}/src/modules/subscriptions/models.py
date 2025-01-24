from datetime import datetime
from typing import ClassVar, List, Optional
from uuid import UUID

import sqlalchemy
from sqlmodel import Field, Relationship

from modules.shared.models import BaseTable


class Product(BaseTable, table=True):
    type: str = Field(default="products")
    id: str = Field(primary_key=True)
    store_id: int = Field(title="Store ID")
    name: str = Field(index=True)
    description: str = Field(title="Product Description")
    status: str = Field(title="Status", schema_extra={"icon": "check_circle"})
    status_formatted: str = Field(
        title="Status Formatted", schema_extra={"icon": "check_circle"}
    )
    price: int = Field(title="Price")
    price_formatted: str = Field(title="Price Formatted")
    from_price: int = Field(title="From Price")
    to_price: int = Field(title="To Price")
    role_name: str = Field(
        foreign_key="role.name",
        title="Role Name",
        nullable=True,
        schema_extra={
            "icon": "user-check",
            "input_type": "select",
            "related_model": "Role",
            "related_field": "name",
        },
    )

    variants: List["Variant"] = Relationship(back_populates="product")

    # Class-level metadata for frontend rendering
    read_priviledge: ClassVar[str] = "admin"
    display_name: ClassVar[str] = "Products"
    sidebar_item: ClassVar[bool] = True
    sidebar_icon: ClassVar[str] = "package"
    table_view_fields: ClassVar[List[str]] = [
        "name",
        "price_formatted",
        "status_formatted",
        "role_name",
    ]
    detail_page_fields: ClassVar[List[str]] = [
        "id",
        "store_id",
        "type",
        "name",
        "role_name",
        "description",
        "status",
        "status_formatted",
        "price",
        "price_formatted",
        "from_price",
        "to_price",
        "test_mode",
    ]
    detail_page_title: ClassVar[Optional[str]] = "Product Details"


class Variant(BaseTable, table=True):
    type: str = Field(default="variants")
    id: str = Field(primary_key=True)
    product_id: str = Field(
        foreign_key="product.id", title="Product ID", schema_extra={"icon": "package"}
    )
    name: str = Field(index=True)
    description: Optional[str] = Field(title="Variant Description")
    price: int = Field(title="Price", nullable=True)
    is_subscription: bool = Field(title="Is Subscription")
    interval: Optional[str] = Field(title="Interval", nullable=True)
    interval_count: Optional[int] = Field(title="Interval Count", nullable=True)
    has_free_trial: bool = Field(title="Has Free Trial")
    trial_interval: Optional[str] = Field(title="Trial Interval", nullable=True)
    trial_interval_count: Optional[int] = Field(
        title="Trial Interval Count", nullable=True
    )
    status: str = Field(
        title="Status", schema_extra={"icon": "check-circle"}, nullable=True
    )
    status_formatted: str = Field(
        title="Status Formatted", schema_extra={"icon": "check-circle"}, nullable=True
    )
    price_formatted: str = Field(title="Price Formatted", nullable=True)

    product: Product = Relationship(back_populates="variants")

    # Class-level metadata for frontend rendering
    read_priviledge: ClassVar[str] = "admin"
    display_name: ClassVar[str] = "Variants"
    sidebar_item: ClassVar[bool] = True
    sidebar_icon: ClassVar[str] = "tag"
    table_view_fields: ClassVar[List[str]] = [
        "name",
        "price_formatted",
        "is_subscription",
        "status_formatted",
    ]
    detail_page_fields: ClassVar[List[str]] = [
        "id",
        "product_id",
        "name",
        "description",
        "price",
        "price_formatted",
        "is_subscription",
        "interval",
        "interval_count",
        "has_free_trial",
        "trial_interval",
        "trial_interval_count",
        "status",
        "status_formatted",
    ]
    detail_page_title: ClassVar[Optional[str]] = "Variant Details"

    class Config:
        arbitrary_types_allowed = True


class Subscription(BaseTable, table=True):
    type: str = Field(default="subscriptions")
    id: str = Field(primary_key=True)
    store_id: int
    customer_id: int
    order_id: int
    order_item_id: int
    product_id: int
    variant_id: int
    product_name: str = Field(title="Subscrition", schema_extra={"icon": "package"})
    variant_name: str = Field(title="Variant", schema_extra={"icon": "package"})
    user_name: str = Field(title="User Name", schema_extra={"icon": "user"})
    user_email: str = Field(title="User Email", schema_extra={"icon": "email"})
    status: str = Field(title="Status", schema_extra={"icon": "check-circle"})
    status_formatted: str = Field(title="Status", schema_extra={"icon": "check-circle"})
    card_brand: Optional[str] = None
    card_last_four: Optional[str] = None
    pause: Optional[str] = None
    cancelled: bool
    trial_ends_at: Optional[datetime] = Field(
        sa_type=sqlalchemy.DateTime(timezone=True), nullable=True, title="Trial ends at"
    )
    billing_anchor: int
    customer_portal: str
    update_payment_method: str
    customer_portal_update_subscription: str
    renews_at: datetime = Field(
        sa_type=sqlalchemy.DateTime(timezone=True), nullable=True, title="Renews at"
    )
    ends_at: Optional[datetime] = Field(
        sa_type=sqlalchemy.DateTime(timezone=True), nullable=True, title="Ends at"
    )
    test_mode: bool
    role: str = Field(
        default="free", title="User Role", schema_extra={"icon": "user-check"}
    )
    user_id: UUID = Field(
        foreign_key="user.id",
        nullable=True,
        title="User ID",
        schema_extra={
            "icon": "user",
            "input_type": "select",
            "related_model": "User",
            "related_field": "id",
        },
    )

    # * Class-level metadata for frontend rendering
    read_priviledge: ClassVar[str] = "admin"
    display_name: ClassVar[str] = "Subscriptions"
    sidebar_item: ClassVar[bool] = True
    sidebar_icon: ClassVar[str] = "credit-card"
    table_view_fields: ClassVar[List[str]] = [
        "user_email",
        "id",
        "product_name",
        "variant_name",
        "status_formatted",
        "renews_at",
        "trial_ends_at",
        "role",
    ]
    detail_page_fields: ClassVar[List[str]] = [
        "id",
        "store_id",
        "customer_id",
        "order_id",
        "order_item_id",
        "product_id",
        "variant_id",
        "product_name",
        "variant_name",
        "user_name",
        "user_email",
        "status",
        "status_formatted",
        "card_brand",
        "card_last_four",
        "pause",
        "cancelled",
        "trial_ends_at",
        "billing_anchor",
        "renews_at",
        "ends_at",
        "test_mode",
        "customer_portal",
        "update_payment_method",
        "customer_portal_update_subscription",
        "role",
    ]
    detail_page_title: ClassVar[Optional[str]] = "Subscription Details"

    class Config:
        arbitrary_types_allowed = True


class SubscriptionInvoice(BaseTable, table=True):
    id: str = Field(primary_key=True)
    store_id: int = Field(title="Store ID")
    subscription_id: int = Field(title="Subscription ID")
    customer_id: int = Field(title="Customer ID")
    user_name: str = Field(title="User Name", schema_extra={"icon": "user"})
    user_email: str = Field(title="User Email", schema_extra={"icon": "email"})
    billing_reason: str
    card_brand: str
    card_last_four: str
    currency: str = Field(title="Currency")
    currency_rate: str = Field(title="Currency Rate")
    status: str = Field(title="Status", schema_extra={"icon": "check-circle"})
    status_formatted: str = Field(
        title="Status Formatted", schema_extra={"icon": "check-circle"}
    )
    refunded: bool = Field(title="Refunded")
    refunded_at: Optional[datetime] = Field(
        sa_type=sqlalchemy.DateTime(timezone=True), nullable=True
    )
    subtotal: int = Field(title="Subtotal Amount")
    discount_total: int = Field(title="Discount Amount")
    tax: int = Field(title="Tax Amount")
    tax_inclusive: bool = Field(title="Tax Inclusive")
    total: int = Field(title="Total Amount")
    refunded_amount: int = Field(title="Refunded Amount")
    subtotal_usd: int = Field(title="Subtotal Amount (USD)")
    discount_total_usd: int = Field(title="Discount Amount (USD)")
    tax_usd: int = Field(title="Tax Amount (USD)")
    total_usd: int = Field(title="Total Amount (USD)")
    refunded_amount_usd: int = Field(title="Refunded Amount (USD)")
    subtotal_formatted: str = Field(title="Subtotal Amount Formatted")
    discount_total_formatted: str = Field(title="Discount Amount Formatted")
    tax_formatted: str = Field(title="Tax Amount Formatted")
    total_formatted: str = Field(title="Total Amount Formatted")
    refunded_amount_formatted: str = Field(title="Refunded Amount Formatted")
    invoice_url: str = Field(title="Invoice URL")
    created_at: datetime = Field(sa_type=sqlalchemy.DateTime(timezone=True))
    updated_at: datetime = Field(sa_type=sqlalchemy.DateTime(timezone=True))
    test_mode: bool

    # Class-level metadata for frontend rendering
    read_priviledge: ClassVar[str] = "admin"
    create_priviledge: ClassVar[str] = "admin"
    update_priviledge: ClassVar[str] = "admin"
    delete_priviledge: ClassVar[str] = "admin"
    display_name: ClassVar[str] = "Subscription Invoices"
    sidebar_item: ClassVar[bool] = True
    sidebar_icon: ClassVar[str] = "file-text"
    table_view_fields: ClassVar[List[str]] = [
        "user_email",
        "status_formatted",
        "total_formatted",
        "created_at",
    ]
    detail_page_fields: ClassVar[List[str]] = [
        "id",
        "store_id",
        "subscription_id",
        "customer_id",
        "user_name",
        "user_email",
        "billing_reason",
        "card_brand",
        "card_last_four",
        "currency",
        "currency_rate",
        "status",
        "status_formatted",
        "refunded",
        "refunded_at",
        "subtotal",
        "discount_total",
        "tax",
        "tax_inclusive",
        "total",
        "refunded_amount",
        "subtotal_usd",
        "discount_total_usd",
        "tax_usd",
        "total_usd",
        "refunded_amount_usd",
        "subtotal_formatted",
        "discount_total_formatted",
        "tax_formatted",
        "total_formatted",
        "refunded_amount_formatted",
        "invoice_url",
        "created_at",
        "updated_at",
        "test_mode",
    ]
    detail_page_title: ClassVar[Optional[str]] = "Subscription Invoice Details"

    class Config:
        arbitrary_types_allowed = True
