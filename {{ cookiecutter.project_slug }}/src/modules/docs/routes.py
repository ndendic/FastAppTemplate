# %% ../example_dashboard.ipynb

from fastcore.utils import *
from fasthtml.common import *
from fasthtml.core import APIRouter
from fasthtml.svg import *
from monsterui import *
from monsterui.franken import *

from modules.shared.templates import app_template

from .notion import NotionPage,dbs_with_links

rt = APIRouter()


def load_markdown(filename: str) -> str:
    """Load markdown content from file"""
    content_path = f"assets/content/docs/{filename}.md"
    try:
        with open(content_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "# Error\nMarkdown file not found"


@rt("/docs")
@app_template("Documentation", requieres="authenticated")
def page(request):
    blog_content = load_markdown("design")
    return Div(cls="space-y-4")(render_md(blog_content))


@rt("/docs/{document}")
@app_template("Documentation", requieres="authenticated")
def page(request):
    doc = request.path_params["document"]
    blog_content = load_markdown(doc)
    return Div(cls="space-y-4")(render_md(blog_content))


@rt("/notion/{page_id}")
@app_template("Notion", requieres="authenticated")
def get(request):
    notion_page = NotionPage()

    page_id = request.path_params["page_id"]
    try:
        # Fetch blocks
        blocks = notion_page.get_page_blocks(page_id)

        # Convert to FastHTML components
        components = notion_page.blocks_to_components(blocks)

        content = Div(*components)
        content_mod = NotStr(apply_classes(content.__html__()))
        return content_mod

    except Exception as e:
        return Titled(
            "Error Loading Page", P(f"Could not load Notion content: {str(e)}")
        )


@rt("/notion")
@app_template("Notion", requieres="authenticated")
def get(request):
    try:
        dbs = dbs_with_links()
        return Titled("Notion Databases", Ul(*dbs))
    except Exception as e:
        return Titled(
            "Error Loading Page", P(f"Could not load Notion content: {str(e)}")
        )
