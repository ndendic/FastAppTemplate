from fasthtml.common import *
from fasthtml.svg import *
from monsterui.franken import *
from config import Settings
config = Settings()

def login_page():
    left = Div(
        cls="col-span-1 hidden flex-col justify-between bg-zinc-900 p-8 text-white lg:flex"
    )(
        Div(cls=(TextT.bold, TextT.default))(config.app_name),
        Blockquote(cls="space-y-2")(
            P(cls=TextT.lg)(
                '"This library has saved me countless hours of work and helped me deliver stunning designs to my clients faster than ever before."'
            ),
            Footer(cls=TextT.sm)("Sofia Davis"),
        ),
    )

    right = Div(cls="col-span-2 flex flex-col p-8 lg:col-span-1")(
        DivRAligned(
            A(
                Button("Register", cls=ButtonT.ghost, submit=False),
                href="/auth/register",
            )
        ),
        DivCentered(cls="flex-1")(
            Div(cls="space-y-6 w-[350px]")(
                Div(cls="flex flex-col space-y-2 text-center")(
                    H3("Sign in to your account"),
                    P(cls=TextFont.muted_sm)(
                        "Pick your favorite way to authenticate with us"
                    ),
                ),
                Form(cls="space-y-6", method="post")(
                    A(
                        Button(
                            UkIcon("github", cls="mr-2"),
                            "Github",
                            cls=(ButtonT.default, "w-full mb-2"),
                            submit=False,
                        ),
                        href="/auth/oauth/github",
                    ),
                    A(
                        Button(
                            Svg(
                                Path(
                                    fill_rule="evenodd",
                                    d="M12.037 21.998a10.313 10.313 0 0 1-7.168-3.049 9.888 9.888 0 0 1-2.868-7.118 9.947 9.947 0 0 1 3.064-6.949A10.37 10.37 0 0 1 12.212 2h.176a9.935 9.935 0 0 1 6.614 2.564L16.457 6.88a6.187 6.187 0 0 0-4.131-1.566 6.9 6.9 0 0 0-4.794 1.913 6.618 6.618 0 0 0-2.045 4.657 6.608 6.608 0 0 0 1.882 4.723 6.891 6.891 0 0 0 4.725 2.07h.143c1.41.072 2.8-.354 3.917-1.2a5.77 5.77 0 0 0 2.172-3.41l.043-.117H12.22v-3.41h9.678c.075.617.109 1.238.1 1.859-.099 5.741-4.017 9.6-9.746 9.6l-.215-.002Z",
                                    clip_rule="evenodd",
                                ),
                                aria_hidden="true",
                                xmlns="http://www.w3.org/2000/svg",
                                width="24",
                                height="24",
                                fill="currentColor",
                                viewbox="0 0 24 24",
                                cls="w-5 h-5 mr-2 dark:text-white",
                            ),
                            "Google",
                            cls=(ButtonT.default, "w-full"),
                            submit=False,
                        ),
                        href="/auth/oauth/google",
                    ),
                    DividerSplit("Or continue with", cls=TextFont.muted_sm),
                    Input(
                        placeholder="name@example.com",
                        name="email",
                        id="email",
                        type="email",
                    ),
                    Input(
                        placeholder="••••••••",
                        name="password",
                        id="password",
                        type="password",
                    ),
                    Button(
                        UkIcon("mail", cls="mr-2"),
                        "Sign in with Email",
                        cls=(ButtonT.primary, "w-full"),
                    ),
                    Div(cls=(TextFont.muted_sm, "flex items-center justify-between"))(
                        A(
                            "Forgot Password?",
                            href="/auth/forgot-password",
                            cls="text-sm",
                        ),
                    ),
                ),
                P(cls=(TextFont.muted_sm, "text-center"))(
                    "By clicking continue, you agree to our ",
                    A(
                        cls="underline underline-offset-4 hover:text-primary",
                        href="#demo",
                        uk_toggle=True,
                    )("Terms of Service"),
                    " and ",
                    A(
                        cls="underline underline-offset-4 hover:text-primary",
                        href="#demo",
                        uk_toggle=True,
                    )("Privacy Policy"),
                    ".",
                ),
            )
        ),
    )

    return Grid(left, right, cols=2, gap=0, cls="h-screen")
