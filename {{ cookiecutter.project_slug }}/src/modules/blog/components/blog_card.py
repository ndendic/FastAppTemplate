from fasthtml.common import *
from fasthtml.svg import *
from monsterui.franken import *
from dateutil import parser


def BlogCard(post):
    """Blog post card component using FrankenUI."""
    datetime_obj = parser.isoparse(post.date)
    date_str = datetime_obj.strftime("%d/%m/%Y")

    return Div(
        Img(src=post.img_path, cls="rounded-lg") if post.img_path else None,
        # ! TODO: Add category
        # Span(
        #     post.category,
        #     cls="bg-purple-100 text-purple-800 text-xs font-semibold mr-2 px-2.5 py-0.5 rounded dark:bg-purple-200 dark:text-purple-900",
        # ),
        DivFullySpaced(
            H3(
                A(post.title, href=f"/blog/{post.slug}"),
                cls="my-1 font-bold tracking-tight",
            ),
            Span(
                date_str,
                cls="text-sm text-gray-500",
            ),
        ),
        Div(P(post.description), cls="mb-5"),
        A(
            "Read More →",
            href=f"/blog/{post.slug}",
            cls="bg-primary px-4 py-2 rounded-lg",
        ),
        cls="bg-secondary border border-gray-900 dark:border-gray-400 rounded-lg p-4",
    )
