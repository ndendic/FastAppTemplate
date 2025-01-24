from fasthtml.common import *
from fasthtml.svg import *
from monsterui.all import *

features = [
    (
        "rocket",
        "Quick Setup",
        "Get up and running in less than 5 minutes with our streamlined setup process.",
    ),
    (
        "shield",
        "Built-in Security",
        "Enterprise-grade security features included out of the box.",
    ),
    (
        "database",
        "Database Ready",
        "Pre-configured database setup with migrations and models.",
    ),
    (
        "layout",
        "Modern UI",
        "Beautiful, responsive UI components powered by MonsterUI.",
    ),
    (
        "code",
        "Developer Friendly",
        "Well-documented codebase with best practices baked in.",
    ),
    (
        "users",
        "Auth & Users",
        "Complete authentication and user management system.",
    ),
]


def FeaturesHeading():
    return Div(
        Div(
            H2(
                "Designed for business teams like yours",
                cls="mb-4 text-4xl tracking-tight font-extrabold",
            ),
            P(
                "Here at {{ cookiecutter.project_name }} we focus on markets where technology, innovation, and capital can unlock long-term value and drive economic growth.",
                cls=TextFont.muted_lg,
            ),
            cls="max-w-screen-md mb-8 lg:mb-16",
        ),
    )


def FeaturesCard(icon, title, description):
    return Div(
        DivHStacked(
            Div(
                UkIcon(icon, height=20, width=20, cls="text-primary"),
                cls="rounded-full",
            ),
            H3(title, cls="font-bold"),
        ),
        P(
            description,
            cls=TextFont.muted_lg + " mt-1",
        ),
        cls="bg-popover border border-gray-900 dark:border-gray-400 space-y-2 rounded-lg p-4",
    )


def FeaturesSection():
    return Div(
        Div(
            FeaturesHeading(),
            Div(
                *[
                    FeaturesCard(icon, title, description)
                    for icon, title, description in features
                ],
                cls="space-y-8 md:grid md:grid-cols-2 lg:grid-cols-3 md:gap-12 md:space-y-0",
            ),
            cls="py-8 px-4 mx-auto max-w-screen-xl sm:py-16 lg:px-6",
        ),
    )
