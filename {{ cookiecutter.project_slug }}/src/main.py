import logfire
import secrets
# import modules
from fasthtml.common import *
from monsterui.all import *
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from modules.shared.toaster import setup_custom_toasts
from route_collector import add_routes

logfire.configure(send_to_logfire='if-token-present')

middleware = [Middleware(SessionMiddleware, secret_key=secrets.token_urlsafe(32))]

custom_theme_css = Link(rel="stylesheet", href="/css/custom_theme.css", type="text/css")

frankenui_headers = Theme.rose.headers()

def user_auth_before(req, sess):
    auth = req.scope["user"] = sess.get("user", None)
    if not auth:
        return RedirectResponse("/auth/login", status_code=303)


beforeware = Beforeware(
    user_auth_before,
    skip=[
        r"/favicon\.ico",
        r"/assets/.*",
        r".*\.css",
        r".*\.svg",
        r".*\.png",
        r".*\.jpg",
        r".*\.jpeg",
        r".*\.gif",
        r".*\.js",
        r"/auth/.*",
        r"/pricing",
        r"/about",
        r"/api/.*",
        "/",
    ],
)


app, rt = fast_app(
    before=beforeware,
    middleware=middleware,
    static_path="assets",
    live=True,
    pico=False,
    hdrs=(
        frankenui_headers,
        custom_theme_css,
        HighlightJS(langs=["python", "javascript", "html", "css"]),
    ),
    htmlkw=dict(cls="bg-surface-light dark:bg-surface-dark"),
)

setup_custom_toasts(app)
app = add_routes(app)
logfire.instrument_starlette(app)

if __name__ == "__main__":
    serve(reload=True)
