import os
import platform
import sys
from urllib.request import urlretrieve

def install_tailwind():
    # Detect operating system
    system = platform.system().lower()

    # Set the download URL for Tailwind CLI based on the OS
    if system == "windows":
        tailwind_url = "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-windows-x64.exe"
        tailwind_path = "tailwindcss.exe"
    elif system == "darwin":  # macOS
        tailwind_url = "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-macos-arm64"
        tailwind_path = "tailwindcss"
    else:  # Assume Linux or WSL
        tailwind_url = "https://github.com/tailwindlabs/tailwindcss/releases/latest/download/tailwindcss-linux-x64"
        tailwind_path = "tailwindcss"

    # Download the Tailwind CLI
    try:
        print(f"Downloading Tailwind CLI from {tailwind_url}...")
        # Create the full path in the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(current_dir, tailwind_path)
        
        # Download the file
        urlretrieve(tailwind_url, full_path)
        print("Tailwind CLI downloaded successfully.")

        # Make it executable (for Unix-based systems)
        if system != "windows":
            os.chmod(full_path, 0o755)

        print(f"Tailwind CLI installation completed. Saved to: {full_path}")
    except Exception as e:
        print(f"Failed to install Tailwind CLI: {str(e)}")
        print(f"Current directory: {current_dir}")
        print(f"Attempted to save to: {full_path}")

if __name__ == "__main__":
    install_tailwind()
