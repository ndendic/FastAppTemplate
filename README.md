# 🚀 FastHTML SaaS Boilerplate Creator

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
   cookiecutter gh:ndendic/cc-fastapp
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

## 📚 Documentation

For more detailed information about the project, please refer to the following documentation:

- 📐 [Design Documentation](docs/design.md)
- 📖 [User Guide](docs/user_guide.md)
- 💻 [Developer Guide](docs/developer_guide.md)
- 🔌 [API Reference](docs/api_reference.md)

## 🤝 Contributing

We welcome contributions to the FastHTML SaaS Boilerplate Creator! Please read our [Contributing Guidelines](CONTRIBUTING.md) for more information on how to get started.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
