# app/scripts/seed_data.py
from modules.auth.models import Role, Priviledge, RolePriviledge


def seed_roles():
    roles = [
        {"name": "admin", "description": "Full system access"},
        {"name": "authenticated", "description": "Basic authenticated user"},
    ]
    privileges = [
        {"name": "admin", "description": "Full system access"},
        {"name": "authenticated", "description": "Basic authenticated user"},
    ]

    print("Seeding roles...")
    for role_data in roles:
        role = Role(**role_data)
        role.save()
    print(f"Seeded {len(roles)} roles successfully!")

    print("Seeding privileges...")
    for privilege_data in privileges:
        privilege = Priviledge(**privilege_data)
        privilege.save()
    print(f"Seeded {len(privileges)} privileges successfully!")

    print("Seeding role privileges...")
    for role_data in roles:
        role_priviledges = RolePriviledge(role_name=role_data["name"], priviledge_name=role_data["name"])
        role_priviledges.save()
    print(f"Seeded {len(privileges)} role privileges successfully!")


if __name__ == "__main__":
    seed_roles()
