import logfire

from config import Settings
from modules.auth.services.fasthtml_auth import FastHTMLAuth
from modules.auth.services.supabase_auth import SupabaseAuth

logfire.configure(send_to_logfire='if-token-present')


class AuthService:
    def __init__(self):
        self.auth_method = Settings().auth_method

        if self.auth_method == "supabase":
            self.auth = SupabaseAuth()
        elif self.auth_method == "fasthtml":
            self.auth = FastHTMLAuth()
        else:
            raise ValueError(f"Unsupported auth method: {self.auth_method}")

    async def login(self, request, email, password):
        return await self.auth.login(request, email, password)

    async def oauth_login(self, request, provider, code=None):
        return await self.auth.oauth_login(request, provider, code)

    async def logout(self, request, session):
        return await self.auth.logout(request, session)

    async def register(self, request, password, email):
        return await self.auth.register(request, password, email)

    async def request_password_reset(self, request, email):
        return await self.auth.request_password_reset(request, email)

    async def reset_password(self, request, token, new_password):
        return await self.auth.reset_password(request, token, new_password)

    async def login_otp(self, request, email, password):
        return await self.auth.login_otp(request, email, password)
