from fasthtml.common import *
from monsterui.all import *

def hero():
    return Section(
            Div(
                Div(
                    H1(
                        "Bliz Boilerplate",
                        cls="text-4xl font-bold tracking-tight sm:text-6xl",
                    ),
                    P(
                        "Launch your project in minutes, not months. Everything you need to start building your next great idea.",
                        cls=TextFont.muted_lg + " mt-6",
                    ),
                    Form(
                        Div(
                            Div(
                                Label(
                                    "Email address",
                                    fr="member_email",
                                    cls="hidden mb-2 text-sm font-medium",
                                ),
                                Input(
                                    placeholder="Enter your email",
                                    type="email",
                                    name="member[email]",
                                    id="member_email",
                                    required="",
                                    cls="block md:w-96 w-full p-3 pl-4 text-sm  border rounded-lg",
                                ),
                                cls="relative w-auto mr-3",
                            ),
                            Div(
                                Button("Try for free", cls=ButtonT.primary + " text-lg px-8 py-3"),
                                
                            ),
                            cls="flex items-center mb-3 mt-3",
                        ),
                        Div(
                            "Instant signup. No credit card required. ",
                            A(
                                "Terms of Service",
                                href="#",
                                cls="hover:underline",
                            ),
                            " and ",
                            A(
                                "Privacy Policy",
                                href="#",
                                cls="hover:underline",
                            ),
                            ".",
                            cls=TextFont.muted_sm,
                        ),
                        action="#",
                    ),
                    cls="mr-auto place-self-center lg:col-span-7 xl:col-span-8",
                ),
                Div(
                    Img(
                        src="/content/site/vecteezy_rocket-launch-in-space-flat-illustration_29453025.svg",
                        # src="https://flowbite.s3.amazonaws.com/blocks/marketing-ui/hero/mobile-app.svg",
                        alt="phone illustration",
                    ),
                    cls="hidden lg:mt-0 lg:col-span-5 xl:col-span-4 lg:flex",
                ),
                cls="grid max-w-screen-xl px-4 mx-auto lg:gap-12 xl:gap-0 lg:grid-cols-12",
            ),
        ),
        