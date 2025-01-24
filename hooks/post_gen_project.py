#!/usr/bin/env python
import os
import shutil

def remove_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print(f"✓ Removed {directory}")

def main():
    print("Running post-generation script...")
    project_directory = os.getcwd()

    # Handle optional modules
    if "{{ cookiecutter.include_subscriptions }}" != "y":
        remove_directory(os.path.join(project_directory, "src", "modules", "subscriptions"))
    
    if "{{ cookiecutter.include_blog }}" != "y":
        remove_directory(os.path.join(project_directory, "src", "modules", "blog"))
    
    if "{{ cookiecutter.include_docs }}" != "y":
        remove_directory(os.path.join(project_directory, "src", "modules", "docs"))
    
    if "{{ cookiecutter.include_contact_form }}" != "y":
        remove_directory(os.path.join(project_directory, "src", "modules", "contact"))
    
    if "{{ cookiecutter.include_playground }}" != "y":
        remove_directory(os.path.join(project_directory, "src", "modules", "playground"))

    # Setup environment file
    # try:
    #     env_example = os.path.join(project_directory, '.env.example')
    #     env_file = os.path.join(project_directory, '.env')
        
    #     if os.path.exists(env_example):
    #         shutil.copy2(env_example, env_file)
    #         print("✓ Successfully created .env file from .env.example")
    #     else:
    #         print("! Warning: .env.example file not found")
            
    # except Exception as e:
    #     print(f"! Error creating .env file: {str(e)}")

    print("Project generation completed!")

if __name__ == "__main__":
    main() 