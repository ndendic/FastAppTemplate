# Developer Guide

## Setting Up the Development Environment

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fasthtml-saas-boilerplate-creator.git
   cd fasthtml-saas-boilerplate-creator
   ```

2. Create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up pre-commit hooks for code quality:
   ```
   pip install pre-commit
   pre-commit install
   ```

## Project Structure

```
fasthtml/
├── main.py
├── app/
│   ├── __init__.py
│   ├── auth/
│   ├── config/
│   ├── generators/
│   ├── models/
│   ├── routes/
│   ├── templates/
│   └── utils/
├── assets/
├── tests/
├── docs/
└── requirements.txt
```

## Best Practices

1. Use FastHTML's routing decorators for clean code organization:
   ```python
   @app.route("/")
   def index(request):
       return {"message": "Welcome to FastHTML SaaS Boilerplate Creator"}
   ```

2. Utilize FastHTML's built-in form handling and validation:
   ```python
   from fasthtml import Form, fields

   class ProjectConfigForm(Form):
       app_name = fields.String(required=True)
       backend = fields.Select(choices=["supabase", "sqlalchemy"])
       # Add more fields as needed
   ```

3. Implement proper error handling and logging:
   ```python
   import logging

   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   try:
       # Your code here
   except Exception as e:
       logger.error(f"An error occurred: {str(e)}")
       # Handle the error appropriately
   ```

4. Write unit tests for all major components:
   ```python
   import pytest
   from fasthtml.testclient import TestClient
   from main import app

   client = TestClient(app)

   def test_index():
       response = client.get("/")
       assert response.status_code == 200
       assert response.json() == {"message": "Welcome to FastHTML SaaS Boilerplate Creator"}
   ```

5. Use FastHTML's Beforeware for authentication and authorization:
   ```python
   from fasthtml import Beforeware

   @app.beforeware
   def auth_middleware(request):
       if not request.user.is_authenticated:
           return redirect("/login")
   ```

6. Leverage FastHTML's FT components for reusable UI elements:
   ```python
   from fasthtml import FT

   class Navbar(FT):
       def render(self):
           return """
           <nav>
               <a href="/">Home</a>
               <a href="/projects">Projects</a>
               <a href="/account">Account</a>
           </nav>
           """
   ```

## Adding New Features

1. Create a new branch for your feature:
   ```
   git checkout -b feature/new-feature-name
   ```

2. Implement the feature using FastHTML best practices.

3. Write tests for your new code in the `tests/` directory.

4. Update relevant documentation in the `docs/` directory.

5. Submit a pull request for review:
   - Push your branch to the repository
   - Create a pull request on GitHub
   - Describe your changes and link to any relevant issues

## Deployment

1. Use FastHTML's `serve()` function for production deployment:
   ```python
   if __name__ == "__main__":
       import uvicorn
       uvicorn.run(app, host="0.0.0.0", port=8000)
   ```

2. Consider using a process manager like Supervisor or PM2 to keep your application running.

3. Set up monitoring and logging:
   - Use a service like Sentry for error tracking
   - Implement application-level logging
   - Set up server-level monitoring (e.g., CPU, memory, disk usage)

4. Use a reverse proxy (e.g., Nginx) in production:
   - Configure SSL/TLS
   - Handle assets file serving
   - Implement caching if needed

## Troubleshooting

- Check FastHTML documentation for common issues and solutions.
- Use FastHTML's debug mode during development:
  ```python
  app.debug = True
  ```
- Consult the project's issue tracker on GitHub for known problems and solutions.
- When encountering errors, check the application logs and server logs for more information.
- Use debugging tools like pdb or an IDE debugger to step through code and identify issues.

## Contributing

1. Fork the repository on GitHub.
2. Create a new branch for your contribution.
3. Make your changes and ensure all tests pass.
4. Update documentation as needed.
5. Submit a pull request with a clear description of your changes.

## Code Style

- Follow PEP 8 guidelines for Python code style.
- Use meaningful variable and function names.
- Write clear and concise comments and docstrings.
- Use type hints where appropriate.

## Versioning

We use Semantic Versioning (SemVer) for version numbers. When making changes:

- Increment the major version for incompatible API changes.
- Increment the minor version for new functionality in a backwards-compatible manner.
- Increment the patch version for backwards-compatible bug fixes.

## Additional Resources

- [FastHTML Documentation](https://fasthtml.github.io/)
- [Starlette Documentation](https://www.starlette.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [HTMX Documentation](https://htmx.org/docs/)
- [Pico CSS Documentation](https://picocss.com/docs/)

Remember to keep this guide updated as the project evolves and new best practices or tools are adopted.
