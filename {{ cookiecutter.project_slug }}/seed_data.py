# app/scripts/seed_data.py
from modules.auth.models import Role


def seed_roles():
    roles = [
        {"name": "admin", "description": "Full system access"},
        {"name": "authenticated", "description": "Basic authenticated user"},
    ]

    print("Seeding roles...")
    for role_data in roles:
        role = Role(**role_data)
        role.save()
    print(f"Seeded {len(roles)} roles successfully!")


if __name__ == "__main__":
    seed_roles()
