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

# fh_cfg["auto_id"] = True

logfire.configure()


project_root = os.path.dirname(os.path.abspath(__file__))

middleware = [Middleware(SessionMiddleware, secret_key=secrets.token_urlsafe(32))]

tailwind_css = Link(rel="stylesheet", href="/css/output.css", type="text/css")
custom_theme_css = Link(rel="stylesheet", href="/css/custom_theme.css", type="text/css")
flowbite_hdrs = (
    Script(src="https://cdn.tailwindcss.com"),
    Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.css",
    ),
    Script(src="/tailwind.config.js"),  # Updated to use static path
)
flowbite_ftrs = [
    Script(src="https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.js")
]
frankenui_headers = Theme.rose.headers()
franken_local = (
    Script(
        type="module", src="https://unpkg.com/franken-ui@1.1.0/dist/js/core.iife.js"
    ),
    Script(
        type="module", src="https://unpkg.com/franken-ui@1.1.0/dist/js/icon.iife.js"
    ),
    tailwind_css,
    custom_theme_css,
    Script("""const htmlElement = document.documentElement;
          if (
            localStorage.getItem("mode") === "dark" ||
            (!("mode" in localStorage) &&
              window.matchMedia("(prefers-color-scheme: dark)").matches)
          ) {
            htmlElement.classList.add("dark");
          } else {
            htmlElement.classList.remove("dark");
          }

          htmlElement.classList.add(localStorage.getItem("theme") || "uk-theme-yellow");
          """),
)
theme_toggle_js = Script(src="/js/themeToggle.js")


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
        r"/contact",
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
    # ftrs=flowbite_ftrs,
    htmlkw=dict(cls="bg-surface-light dark:bg-surface-dark"),
    # exception_handlers={404: custom_404_handler},
)

setup_custom_toasts(app)
app = add_routes(app)
logfire.instrument_starlette(app)

if __name__ == "__main__":
    serve(reload=True)
