import os
import shutil
import subprocess
from pathlib import Path

def create_package():
    package_dir = Path("package")
    zip_file = Path("lambda-deployment.zip")
    
    # Clean up previous builds
    if package_dir.exists():
        shutil.rmtree(package_dir)
    if zip_file.exists():
        zip_file.unlink()
    
    # Create the package directory
    package_dir.mkdir()

    # Install dependencies
    print("Installing dependencies...")
    subprocess.run(["pip", "install", "boto3", "loguru", "--target", str(package_dir)], check=True)
    subprocess.run(["pip", "install", ".", "--target", str(package_dir)], check=True)

    # Copy main script
    print("Copying project files...")
    shutil.copy("main.py", package_dir)

    # Copy only the `btry` subdirectory from `src`
    btry_src = Path("src/btry")
    btry_dest = package_dir / "btry"
    shutil.copytree(btry_src, btry_dest, dirs_exist_ok=True)

    # Create a zip file
    print("Creating zip package...")
    shutil.make_archive(zip_file.stem, 'zip', package_dir)

    # Clean up package directory
    shutil.rmtree(package_dir)
    print(f"Deployment package created: {zip_file}")

if __name__ == "__main__":
    create_package()
