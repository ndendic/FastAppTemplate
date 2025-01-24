from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # Application Settings
    app_name: str = "{{ cookiecutter.project_name }}"
    app_version: str = "{{ cookiecutter.version }}"
    app_description: str = "{{ cookiecutter.project_description }}"
    
    # Feature Flags
    has_subscriptions: bool = {{ cookiecutter.include_subscriptions == 'y' }}
    has_blog: bool = {{ cookiecutter.include_blog == 'y' }}
    has_docs: bool = {{ cookiecutter.include_docs == 'y' }}
    has_contact_form: bool = {{ cookiecutter.include_contact_form == 'y' }}
    has_playground: bool = {{ cookiecutter.include_playground == 'y' }}
    
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
    
    # Payment Settings
    lemonsqeezy_api_key: str | None = "{{ cookiecutter.lemonsqeezy_api_key }}"
    lemonsqeezy_store_id: str | None = "{{ cookiecutter.lemonsqeezy_store_id }}"
    lemonsqeezy_webhook_secret: str | None = "{{ cookiecutter.lemonsqeezy_webhook_secret }}"
    
    # Integration Settings
    notion_key: str | None = "{{ cookiecutter.notion_key }}"
    notion_database_id: str | None = "{{ cookiecutter.notion_database_id }}"

    @property
    def is_using_supabase(self) -> bool:
        return self.db_service == "supabase" or self.auth_method == "supabase"

    @property
    def is_using_oauth(self) -> bool:
        return bool(self.google_oauth_id or self.github_oauth_id)

    @property
    def is_using_subscriptions(self) -> bool:
        return bool(self.lemonsqeezy_api_key)

