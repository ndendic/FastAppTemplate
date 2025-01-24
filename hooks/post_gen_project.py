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

    print("Project generation completed!")

if __name__ == "__main__":
    main() 