from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # Application Settings
    app_name: str = "{{ cookiecutter.project_name }}"
    app_version: str = "{{ cookiecutter.version }}"
    app_description: str = "{{ cookiecutter.project_description }}"
    
    # Database Settings
    database_url: str = "{{ cookiecutter.database_url }}"
    db_service: str = "{{ cookiecutter.database_backend }}"
    
    # Authentication Settings
    auth_method: str = "{{ cookiecutter.auth_provider }}"
    
    # Supabase Settings (if using Supabase)
    supabase_url: str | None = "{{ cookiecutter.supabase_url }}"
    supabase_key: str | None = "{{ cookiecutter.supabase_key }}"
    supabase_service_key: str | None = "{{ cookiecutter.supabase_service_key }}"
    
    # Email Settings
    smtp_server: str = "{{ cookiecutter.smtp_server }}"
    smtp_port: int = {{ cookiecutter.smtp_port }}
    smtp_username: str = "{{ cookiecutter.smtp_username }}"
    smtp_password: str = "{{ cookiecutter.smtp_password }}"
    resend_api_key: str = "{{ cookiecutter.resend_api_key }}"
    
    # OAuth Settings
    google_oauth_id: str | None = "{{ cookiecutter.google_oauth_id }}"
    google_oauth_secret: str | None = "{{ cookiecutter.google_oauth_secret }}"
    github_oauth_id: str | None = "{{ cookiecutter.github_oauth_id }}"
    github_oauth_secret: str | None = "{{ cookiecutter.github_oauth_secret }}"

    @property
    def is_using_supabase(self) -> bool:
        return self.db_service == "supabase" or self.auth_method == "supabase"

    @property
    def is_using_oauth(self) -> bool:
        return bool(self.google_oauth_id or self.github_oauth_id)

    @property
    def is_using_subscriptions(self) -> bool:
        return bool(self.lemonsqeezy_api_key)

