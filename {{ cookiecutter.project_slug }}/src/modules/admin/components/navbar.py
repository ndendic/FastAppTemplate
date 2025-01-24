import json

from fasthtml.common import *
from fasthtml.components import Uk_theme_switcher
from monsterui.franken import *
from modules.auth.models import User

from config import Settings
config = Settings()

hotkeys = [
    ("Profile", "⇧⌘P", "/user/profile"),
    ("Billing", "⌘B"),
    ("Settings", "⌘S"),
    # ("New Team", ""),
    ("Logout", "", "/auth/logout", False),
]


def NavSpacedLi(t, s=None, href="#", is_content=True):
    return Li(
        A(
            DivFullySpaced(P(t), P(s, cls=TextFont.muted_sm)),
            href=href + "#",
            hx_boost="true" if is_content else "false",
            hx_target="#content",
            hx_swap_oob=True,
        )
    )


def Avatar(
    url,
    h=20,  # Height
    w=20,  # Width
):  # Span with Avatar
    return Span(
        cls=f"relative flex h-{h} w-{w} shrink-0 overflow-hidden rounded-full bg-accent"
    )(
        Img(
            cls=f"aspect-square h-{h} w-{w}",
            alt="Avatar",
            loading="lazy",
            src=url,
        )
    )


def avatar_dropdown(request):
    user_data = request.session.get("user")
    if user_data:
        user_data = json.loads(user_data)
        user = User.get(user_data["id"])
        if user:
            return Div(
                Avatar(user.avatar_url, 8, 8)
                if user.avatar_url
                else DiceBearAvatar("Destiny", 8, 8),
                DropDownNavContainer(
                    NavHeaderLi(user.full_name, NavSubtitle(user.email)),
                    *[NavSpacedLi(*hk) for hk in hotkeys],
                ),
                cls="hidden lg:block"
            )
    return None


def theme_toggle():
    return Div(
    Button(
        UkIcon(icon='palette', uk_cloak=''),
        cls='uk-icon-button uk-icon-button-small uk-icon-button-outline'
    ),
    Div(
        Div('Customize', cls='uk-card-title uk-margin-medium-bottom'),
        Uk_theme_switcher(),
        uk_drop='mode: click; offset: 8',
        cls='uk-card uk-card-body uk-card-default uk-drop uk-width-large'
    ),
    cls='uk-inline'
)
def SidebarToggle():
    return Button(
        UkIcon("menu", height=20, width=20),
        cls="block lg:hidden p-2",  # Show on mobile, hide on desktop
        uk_toggle="target: #mobile-sidebar",
        aria_label="Toggle navigation menu",
    )

nav_items = [
    ("Home", "/"),
    ("Dashboard", "/dashboard"),
    ("Playground", "/playground"),
]
def TopNav(request):
    return NavBarContainer(
        NavBarLSide(
            NavBarNav(
                SidebarToggle(),  # Mobile toggle button
                # Hide navigation items on mobile
                NavBarNav(
                    *[NavSpacedLi(item[0], href=item[1]) for item in nav_items],
                    cls="hidden lg:flex items-center ml-16",  # Hide on mobile, show on desktop
                ),
            )
        ),
        NavBarRSide(
            DivRAligned(
                theme_toggle(),
                # Hide search on mobile                
                avatar_dropdown(request),
                cls="space-x-2",
            ),
            # cls="hidden lg:block"
        ),
        # Reduce padding on mobile
        cls="sticky top-0 border-b border-border px-2 lg:px-4 z-100 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
    )





def MobileDrawer():
    return Div(
        Button(
            UkIcon("menu", height=24, width=24),
            cls=ButtonT.ghost + " md:hidden",
            uk_toggle="target: #mobile-menu",
        ),
        Modal(
            Div(cls="p-6 bg-background")(
                H3("Menu", cls="text-lg font-semibold mb-4"),
                NavContainer(
                    *[
                        Li(
                            A(
                                label,
                                href=url,
                                cls="flex items-center p-2 hover:bg-muted rounded-lg transition-colors",
                            )
                        )
                        for label, url in nav_items
                    ],
                    Li(DividerLine(lwidth=2, y_space=4)),
                    Li(
                        A(
                            "Sign in",
                            href="/auth/login",
                            cls="flex items-center p-2 hover:bg-muted rounded-lg transition-colors",
                        )
                    ),
                    Li(
                        Button(
                            "Get Started",
                            cls=ButtonT.primary + " w-full mt-2",
                            onclick="window.location.href='/pricing'",
                        )
                    ),
                    cls=NavT.primary + " space-y-2",
                ),
            ),
            id="mobile-menu",
        ),
    )


def NewNav(request):
    return Header(
        cls="sticky top-0 z-100 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
    )(
        Div(cls="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16")(
            Div(cls="flex h-full justify-between items-center")(
                Div(cls="flex items-center gap-x-8")(
                    # Mobile menu drawer
                    MobileDrawer(),
                    # Logo
                    A(href="/", cls="flex items-center")(
                        Span(config.app_name, cls="font-bold text-xl")
                    ),
                    # Desktop navigation
                    Nav(cls="hidden md:flex items-center space-x-8")(
                        *[
                            A(
                                label,
                                href=url,
                                cls="text-sm font-medium transition-colors hover:text-foreground/80 text-foreground/60",
                            )
                            for label, url in nav_items
                        ]
                    ),
                ),
                # Desktop CTA buttons
                Div(cls="hidden md:flex items-center space-x-4")(
                    theme_toggle(),
                    Input(placeholder="Search"),
                    avatar_dropdown(request),
                ),
            )
        )
    )


def Navbar(request):
    return TopNav(request)
