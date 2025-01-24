from fasthtml.common import *
from fasthtml.components import Uk_theme_switcher
from monsterui import *
from monsterui.franken import *
from config import Settings
config = Settings()

def MobileDrawer():
    nav_items = [
        ("Home", "/"),
        ("About", "/about"),
        ("Pricing", "/pricing"),
    ]

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

def theme_toggle():
    return Div(
    Button(
        UkIcon(icon='palette', uk_cloak=''),
        cls='uk-icon-button uk-icon-button-small uk-icon-button-outline'
    ),
    Div(
        Div('Customize', cls='uk-card-title uk-margin-medium-bottom'),
        # Uk_theme_switcher(),
        Uk_theme_switcher(custom_palette="""[
            {"background": "#10b981", "key": "uk-theme-grass", "text": "Grass"},
            {"background": "#0099AD", "key": "uk-theme-lightsky", "text": "Light Sky"},
            {"background": "#E74D3C", "key": "uk-theme-mandarino", "text": "Mandarino"},
            {"background": "#364049", "key": "uk-theme-calm", "text": "Calm"}
            ]"""
        ),
        uk_drop="mode: click; offset: 8",
        cls="uk-card uk-card-body uk-card-default uk-drop uk-width-large",
    ),
    cls='uk-inline'
)

def Navbar():
    nav_items = [
        ("Home", "/"),
        ("About", "/about"),
        ("Pricing", "/pricing"),
    ]

    return Header(
        cls="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
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
                    A(
                        "Sign in",
                        href="/auth/login",
                        cls="text-sm font-medium transition-colors hover:text-primary",
                    ),
                    Button(
                        "Get Started",
                        cls=ButtonT.primary,
                        onclick="window.location.href='/pricing'",
                    ),
                    theme_toggle(),

                ),
            )
        )
    )
