# %% ../example_dashboard.ipynb
from fasthtml.common import *
from fasthtml.core import APIRouter
from fasthtml.svg import *
from monsterui.franken import *
from typing import List

from .models import BlogPost
from .components import BlogList
from modules.shared.templates import app_template

rt = APIRouter()


def load_markdown(filename: str) -> str:
    """Load markdown content from file"""
    content_path = f"assets/content/blog/{filename}.md"
    try:
        with open(content_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "# Error\nMarkdown file not found"


@rt("/blog")
@app_template("Blog", requieres="authenticated")
def get(request):
    """Blog posts listing page."""
    posts: List[BlogPost] = BlogPost.query(
        sorting_field="date",
        sort_direction="desc"
    )
    return Div(
        DivCentered(H1("Our Blog"),Span("We use an agile approach to test assumptions and connect with the needs of your audience early and often.")),
        BlogList(posts)
    )


@rt("/blog/{blog_post}")
@app_template("Blog Post", requieres="authenticated")
def page(request):
    blog_post = request.path_params["blog_post"]
    blog_content = load_markdown(blog_post)
    return Div(cls="space-y-4")(render_md(blog_content))
