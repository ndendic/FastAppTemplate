# 🚀 FastHTML Boilerplate Creator

FastHTML Boilerplate Creator is a powerful tool that allows users to quickly generate customized SaaS boilerplate projects using FastHTML. This service streamlines the process of setting up a new application by providing a user-friendly interface to configure various aspects of the project.

## ✨ Features

- 🔐 User authentication and authorization
- 🎨 Customizable app name and branding
- 💾 Flexible backend options (Supabase, SQLAlchemy-supported databases)
- 🔑 Authentication options (Supabase, FastHTML auth)
- 🎯 Frontend customization
- 🚢 Deployment options (Docker, cloud platforms)

## 🏁 Getting Started

1. First, create your project using cookiecutter:
   ```bash
   pip install cookiecutter
   cookiecutter gh:ndendic/FastAppTemplate
   ```

2. We recommend using `uv` for faster Python package management. Install it if you haven't already:
   ```bash
   pip install uv
   ```

3. Create a virtual environment using uv:
   ```bash
   uv venv
   ```

4. Activate the virtual environment:
   ```bash
   # On Linux/MacOS:
   source .venv/bin/activate
   
   # On Windows:
   .venv\Scripts\activate
   ```

5. Install the project in editable mode:
   ```bash
   uv pip install -e .
   ```

6. Set up the database:
   ```bash
   # Create database migrations
   app migrations
   
   # Apply the migrations
   app migrate
   ```

7. Seed the initial privilege data:
   ```bash
   uv run seed_data.py
   ```

8. Run the application:
   ```bash
   app run
   ```

🌐 The application will be available at `http://localhost:5001`.

## 🔄 Automatic Route Collection

The template features an automatic route collection system that scans the modules for `rt` APIRouters and registers all routes automatically. Here's how it works:

1. Create a new page in the under your module `src/modules/your_module` directory:
```python
# app/src/modules/hello/hello.py
from fasthtml.common import *
from fasthtml.core import APIRouter

rt = APIRouter()

@rt("/hello")
def get(request):
    return "Hello, World!"
```

2. The route collector will automatically find and register this route - no manual registration needed!

## 🗄️ Database System

The template includes a database system built on SQLModel with a custom BaseTable class.

### 📝 Creating Models

Create new models by extending the BaseTable class:

```python
from sqlmodel import Field
from modules.shared.models import BaseTable

class Product(BaseTable, table=True):
    name: str = Field(nullable=False)
    price: float = Field(nullable=False)
    description: str = Field(default="")
```

### 💾 Database Operations

The BaseTable class provides several convenient methods:

```python
# Create/Update
product = Product(name="Widget", price=9.99)
product.save()

# Query
all_products = Product.all()
specific_product = Product.get(product_id)

# Update
Product.update(product_id, {"price": 19.99})

# Delete
Product.delete(product_id)
```

### 🔄 Database Migrations

The template uses Alembic for database migrations. If you're using SQLite, make sure you specify absolute database DATABSE_URL in your .env file.

1. After creating or modifying models, generate a migration:
```bash
alembic revision --autogenerate -m "Add product table"
```
or
```bash
app migrations
```


2. Apply the migration:
```bash
alembic upgrade head
```
or
```bash
app migrate
```

## 🔐 Authentication System

The template includes a complete authentication system with the following features:

- 👤 User registration and login
- 🔑 Password reset functionality 
- 🌐 OAuth support - under development 🚧
- 📱 OTP (One-Time Password) support - emails are sent using Resend
- 🔒 Session management

## 🎛️ Admin Dashboard

The template includes an automatic admin dashboard that is dynamically generated based on your models. Any model that inherits from `BaseTable` in `models.py` will automatically get:

- 📊 Auto-generated CRUD interface
- 🔍 Search and filtering capabilities
- 📝 Form generation based on model fields
- 🎨 Customizable display options through class variables:
  ```python
  class YourModel(BaseTable):
      display_name: ClassVar[str] = "Your Model Name"
      sidebar_icon: ClassVar[str] = "table"
      table_view_fields: ClassVar[List[str]] = ["field1", "field2"]
      detail_page_fields: ClassVar[List[str]] = ["field1", "field2", "field3"]
      field_groups: ClassVar[Dict[str, List[str]]] = {
          "Group 1": ["field1", "field2"],
          "Group 2": ["field3"]
      }
  ```


## 🎨 Template System

The template system provides a flexible way to structure your application's pages with built-in permission handling. It offers two main types of templates:

### 🌐 Public Pages
```python
@page_template(title="Your Page Title")
def your_public_page(request):
    return YourContent()
```

### 🔐 Protected App Pages
```python
@app_template(title="Dashboard", requieres="admin")
def your_protected_page(request):
    return YourContent()
```

The template system automatically:
- 🏗️ Handles layout structure (navbar, sidebar, content areas)
- 🔒 Manages permission checks
- 🔄 Supports HTMX partial rendering
- 📱 Provides responsive design

### 🔑 Permission System Integration

The permission system is deeply integrated with both models and templates:

1. **Role-Based Access Control**:
```python
class User(BaseTable):
    role: str = Field(foreign_key="role.name")
    
    @property
    def priviledges(self) -> list[str]:
        return RolePriviledge.query(
            search_value=self.role,
            fields=["priviledge_name"]
        )
```

2. **Permission Decorators**:
```python
@app_template(requieres="admin")  # Only users with 'admin' privilege can access
def admin_page(request):
    return AdminContent()
```

3. **Component-Level Permissions**:
in this example `SidebarGroup` will requiere `admin` priviledge
```python
from modules.shared.validators import priviledged_component
# Show content only if user has required privilege
def SideBar(request):
   return Div(
   # ...
      priviledged_component(
         SidebarGroup("Admin", tables, "folder-dot"),
         request,
         priviledge="admin",
      )
   # ...
   )
```

The system uses a hierarchical approach:
- 👥 Users have Roles
- 🔑 Roles have Privileges
- 🚪 Pages/Components require specific Privileges
- 🔒 Models define CRUD Privileges

## Development Commands

The project includes it's own mini CLI with various helpful commands:

### Basic Commands

- `app run` - Start the FastHTML development server
- `app migrations` - Create DB migrations
- `app migrate` - Migrates changes to db DB
- `app module <module_name>` - creates new module with boilerplate code inside `src/modules`

## 🤝 Contributing

We welcome contributions to the FastHTML SaaS Boilerplate Creator! Please read our [Contributing Guidelines](CONTRIBUTING.md) for more information on how to get started.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
