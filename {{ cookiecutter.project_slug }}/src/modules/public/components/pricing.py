from fasthtml.common import *
from monsterui.all import *


def PricingHeader():
    return (
        Div(
            H2(
                "Designed for business teams like yours",
                cls="mb-4 text-4xl tracking-tight font-extrabold",
            ),
            P(
                "Here we focus on markets where technology, innovation, and capital can unlock long-term value and drive economic growth.",
                cls="mb-5 font-light sm:text-xl",
            ),
            cls="mx-auto max-w-screen-md text-center mb-8 lg:mb-12",
        ),
    )

def PricingTiers(tiers: list[dict]):
    return Div(
        cls="isolate mx-auto mt-12 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3 max-w-7xl"
    )(
        *[
            Card(
                Div(
                    H2(tier["name"], cls="font-bold"),
                    P(
                        tier["description"],
                        cls=TextFont.muted_sm + " sm:text-lg",
                    ),
                    cls="space-y-1",
                ),
                Div(
                    Span(tier["price"], cls="mr-2 text-5xl font-extrabold"),
                    Span("/month", cls="text-gray-500 dark:text-gray-400"),
                    cls="flex justify-center items-baseline my-8",
                ),
                Ul(
                    *[
                        Li(
                            Svg(
                                Path(
                                    fill_rule="evenodd",
                                    d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z",
                                    clip_rule="evenodd",
                                ),
                                fill="currentColor",
                                viewbox="0 0 20 20",
                                xmlns="http://www.w3.org/2000/svg",
                                cls="flex-shrink-0 w-5 h-5 text-green-500 dark:text-green-400",
                            ),
                            Span(feature),
                            cls="flex items-center space-x-3",
                        )
                        for feature in tier["features"]
                    ],
                    role="list",
                    cls="mb-8 space-y-4 text-left",
                ),
                Button(
                    tier["cta"],
                    href="#",
                    cls=ButtonT.primary + "w-full",
                ),
                cls="bg-secondary border border-gray-900 dark:border-gray-400",
            )
            for tier in tiers
        ]
    )


def ComparisonSection():
    features = [
        (
            "Core Features",
            ["Authentication", "Database Setup", "API Endpoints", "Admin Panel"],
        ),
        (
            "Team Features",
            ["Team Management", "Role-based Access", "Audit Logs", "Team Analytics"],
        ),
        (
            "Support",
            ["Documentation", "Community Forum", "Email Support", "Priority Support"],
        ),
        ("Security", ["2FA", "SSO", "Data Encryption", "Security Audits"]),
    ]

    return Div(cls="py-24 sm:py-32")(
        Div(cls="mx-auto max-w-7xl px-6 lg:px-8")(
            Div(cls="mx-auto max-w-2xl lg:text-center")(
                H2(
                    "Feature Comparison",
                    cls="text-3xl font-bold tracking-tight sm:text-4xl",
                ),
                P(
                    "Detailed breakdown of what's included in each plan",
                    cls=TextFont.muted_lg + " mt-6",
                ),
            ),
            Table(
                cls="mt-16 w-full border-collapse text-left block overflow-x-auto sm:table"
            )(
                Thead(cls="bg-muted")(
                    Tr(
                        Th("Features", cls="py-4 px-6 font-semibold"),
                        Th("Starter", cls="py-4 px-6 font-semibold"),
                        Th("Pro", cls="py-4 px-6 font-semibold"),
                        Th("Enterprise", cls="py-4 px-6 font-semibold"),
                    )
                ),
                Tbody(
                    *[
                        Tr(
                            Td(category, cls="py-4 px-6 font-medium border-t"),
                            *[
                                Td(
                                    UkIcon(
                                        "check" if i < len(items) else "x",
                                        cls=f"size-5 {'text-primary' if i < len(items) else 'text-muted-foreground'}",
                                    ),
                                    cls="py-4 px-6 border-t text-center",
                                )
                                for i in range(3)
                            ],
                        )
                        for category, items in features
                    ]
                ),
            ),
        )
    )
