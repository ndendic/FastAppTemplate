import os
import shutil

def remove_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)

project_directory = os.path.join(os.getcwd(), "{{ cookiecutter.project_slug }}")

# Handle subscriptions
if "{{ cookiecutter.include_subscriptions }}" != "y":
    remove_directory(os.path.join(project_directory, "src", "modules", "subscriptions"))

# Handle blog
if "{{ cookiecutter.include_blog }}" != "y":
    remove_directory(os.path.join(project_directory, "src", "modules", "blog"))

# Handle docs
if "{{ cookiecutter.include_docs }}" != "y":
    remove_directory(os.path.join(project_directory, "src", "modules", "docs"))

# Handle contact form
if "{{ cookiecutter.include_contact_form }}" != "y":
    remove_directory(os.path.join(project_directory, "src", "modules", "contact"))

# Handle playground
if "{{ cookiecutter.include_playground }}" != "y":
    remove_directory(os.path.join(project_directory, "src", "modules", "playground"))