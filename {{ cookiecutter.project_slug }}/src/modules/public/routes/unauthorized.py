from fasthtml.common import *
from fasthtml.core import APIRouter
from modules.shared.templates import page_template

rt = APIRouter()

@rt("/unauthorized")
@page_template("Unauthorized")
def page(request):
    return Div(cls="min-h-[50vh] flex items-center justify-center")(
        Div(cls="text-center space-y-4")(
            H1("401 - Unauthorized", cls="text-4xl font-bold"),
            P("Sorry, you don't have permission to access this page.", cls="text-lg text-gray-600"),
            P("Please sign in or contact the administrator if you believe this is a mistake.", cls="text-gray-500"),
            Div(cls="mt-6")(
                A("Go to Homepage", href="/", cls="uk-button uk-button-primary mr-4"),
                A("Sign In", href="/auth/login", cls="uk-button uk-button-default")
            )
        )
    ) 