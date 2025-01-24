from fasthtml.common import *
from monsterui.franken import *
from modules import *
from modules.shared.validators import priviledged_component

models = BaseTable.__subclasses__()
print("Found models:", [model.__name__ for model in models])
tables = [
    (
        model.sidebar_icon,
        model.display_name,
        f"/table/{model.__name__.lower()}",
    )
    for model in models
    if model.sidebar_item
]


discoved_data = [
    ("play-circle", "Listen Now"),
    ("binoculars", "Browse"),
    ("rss", "Radio"),
]
library_data = [
    ("play-circle", "Playlists"),
    ("music", "Songs"),
    ("user", "Made for You"),
    ("users", "Artists"),
    ("bookmark", "Albums"),
]
playlists_data = [("library", "Recently Added"), ("library", "Recently Played")]

nav_items = [
    ("home", "Home", "/"),
    ("layout-dashboard", "Dashboard", "/dashboard"),
    ("beaker", "Playground", "/playground"),
    ("user", "Profile", "/user/profile"),
    ("log-out", "Logout", "/auth/logout"),
]


def SidebarButton(icon, text, href="#"):
    return Li(
        A(
            DivLAligned(
                UkIcon(icon, height=20, width=20, cls="text-muted-foreground"),
                P(text, cls="sidebar-text text-muted-foreground"),
                cls="space-x-2",
            ),
            href=href + "#",
            hx_boost="true",
            hx_target="#content",
            hx_swap_oob=True,
        )
    )


def SidebarGroup(text, data, icon=None):
    return NavParentLi(
        A(
            DivLAligned(
                UkIcon(icon, height=20, width=20) if icon else "",
                H4(text, cls="sidebar-text uk-text-primary"),
                cls="space-x-2 uk-text-primary",
            )
        ),
        NavContainer(parent=True)(*[SidebarButton(*o) for o in data]),
    )


def PanelButton(icon, text, href="#"):
    return Li(
        A(
            DivLAligned(
                UkIcon(icon, height=20, width=20, cls="text-muted-foreground"),
                P(text, cls="text-muted-foreground"),
                cls="space-x-2",
            ),
            href=href + "#",
            hx_boost="true",
            hx_target="#content",
            hx_swap_oob=True,
        )
    )


def PanelGroup(text, data, icon=None):
    return NavParentLi(
        A(
            DivLAligned(
                UkIcon(icon, height=20, width=20) if icon else "",
                H4(text, cls="uk-text-primary"),
                cls="space-x-2 uk-text-primary",
            )
        ),
        NavContainer(parent=True)(*[PanelButton(*o) for o in data]),
    )


def PinButton():
    return Button(
        UkIcon("chevron-right", cls="transform transition-transform pin-icon"),
        cls="pin-button",
        onclick="this.closest('.sidebar').classList.toggle('pinned'); this.querySelector('.pin-icon').classList.toggle('rotate-180')",
    )


def SidebarContent(request):
    return Div(
        Style("""
            .sidebar { 
                flex-direction: column;
            }
            .sidebar-text { 
                opacity: 0;
                white-space: nowrap;
                transition: opacity 0.3s;
            }
            .group:hover .sidebar-text,
            .pinned .sidebar-text {
                opacity: 1;
            }
            .sidebar-content {
                flex-grow: 1;
                overflow-y: auto;
                padding-bottom: 5rem;
                scrollbar-width: none;
                -ms-overflow-style: none;
            }
            .sidebar-content::-webkit-scrollbar {
                display: none;
            }
            .pin-button {
                position: fixed;
                bottom: 1rem;
                left: 1rem;
                background: none;
                border: none;
                cursor: pointer;
                padding: 0.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                color: inherit;
                z-index: 10;
            }
            .pin-button:hover {
                color: var(--primary-color);
            }
            .pinned {
                width: 15rem;
                position: fixed;
                left: 0;
                display: none;
            }
            @media (min-width: 1024px) {
                .pinned {
                    display: flex;
                }
            }
            .pinned .pin-icon {
                transform: rotate(180deg);
            }
            .uk-nav-primary>li>a {
                margin: .25rem;
                border-radius: .375rem;
                padding: 0.51rem 13px;
            }
            .uk-nav-sub {
                margin-left: 1.25rem;
                margin-right: .25rem;
                border-left-width: 1px;
                border-color: hsl(var(--border));
            }
        """),
        Div(
            NavContainer(uk_nav=True, parent=True)(
                # Icon logo
                DivCentered(
                    UkIcon(
                        "github",
                        height=20,
                        width=20,
                        cls="m-2 flex items-center h-[40px]",
                    )
                ),
                # SidebarButton("table", "Dashboard", href="/dashboard"),
                priviledged_component(
                    SidebarGroup("Admin", tables, "folder-dot"),
                    request,
                    priviledge="admin",
                ),
                SidebarGroup("Discover", discoved_data, "compass"),
                SidebarGroup("Library", library_data, "album"),
                SidebarGroup("Playlists", playlists_data, "list"),
                cls=(NavT.primary, "space-y-3"),
            ),
            cls="sidebar-content",
        ),
        # PinButton(),
    )


def Sidebar(request):
    return Div(
        # Main sidebar - hidden on small screens
        Div(
            cls="!hidden lg:!flex flex-col h-screen fixed top-0 left-0 bg-background border-r border-border transition-all duration-300 hover:w-60 w-14 group z-50",
            style="overflow-x: hidden;",
        )(SidebarContent(request)),
        
        # Offcanvas sidebar for mobile
        Div(
            Div(
                Button(
                    UkIcon("x", height=20, width=20),
                    type="button",
                    uk_close="",
                    cls="uk-offcanvas-close",
                ),
                Div(
                    NavContainer(uk_nav=True, parent=True)(
                        DivCentered(
                            UkIcon(
                                "github",
                                height=20,
                                width=20,
                                cls="m-2 flex items-center h-[40px]",
                            )
                        ),
                        # Add navigation items at the top of the mobile menu
                        PanelGroup("Main", nav_items, "square-menu"),
                        priviledged_component(
                            PanelGroup("Admin", tables, "folder-dot"),
                            request,
                            priviledge="admin",
                        ),
                        PanelGroup("Discover", discoved_data, "compass"),
                        PanelGroup("Library", library_data, "album"),
                        PanelGroup("Playlists", playlists_data, "list"),
                        cls=(NavT.primary, "space-y-1"),
                    ),
                    cls="sidebar-content py-2",  # Added some padding
                ),
                cls="uk-offcanvas-bar p-2",  # Reduced padding
            ),
            id="mobile-sidebar",
            uk_offcanvas="overlay: true",
        ),
    )
