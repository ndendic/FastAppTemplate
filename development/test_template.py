
from cookiecutter.main import cookiecutter
import shutil
from pathlib import Path

def test_template():
    # Clean previous test
    output_dir = Path("test_output")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    
    # Run cookiecutter
    cookiecutter(
        '../',
        no_input=True,
        output_dir=output_dir,
        extra_context={
            'project_name': 'Test Project',
            'database_backend': 'postgresql',
            'auth_provider': 'email',
            'payment_processor': 'stripe',
            'include_admin_panel': 'y',
            'include_api': 'y',
            'include_docs': 'y'
        }
    )

if __name__ == "__main__":
    test_template()
    