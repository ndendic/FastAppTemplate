from sre_parse import parse_template
from fasthtml.common import *
from fasthtml.core import APIRouter
from monsterui.franken import *
from .components.card import CardShowcase
from modules.shared.templates import app_template

rt = APIRouter()

@rt('/playground')
@app_template(title="Component Playground")
def get(request):
    """Playground page for testing components."""
    return Titled("Component Playground",
        Main(
            Container(
                # Card showcase section
                Section(
                    CardShowcase(),
                    cls="py-10"
                ),
                cls="space-y-4"
            ),
            cls="py-10"
        )
    )

@rt('/playground')
def post(request):
    # Handle POST request
    return {'message': 'Received a POST request'}

# Add other HTTP methods as needed
