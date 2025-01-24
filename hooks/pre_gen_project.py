import os
import shutil

def remove_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)

project_directory = os.path.join(os.getcwd(), "{{ cookiecutter.project_slug }}")

