import os
import shutil
import subprocess
from pathlib import Path

def create_lambda_package():
    package_dir = Path("package")
    zip_file = Path("lambda-deployment.zip")

    # Clean up previous builds
    if package_dir.exists():
        shutil.rmtree(package_dir)
    if zip_file.exists():
        zip_file.unlink()

    # Create package directory
    package_dir.mkdir()

    # Install dependencies
    subprocess.run(["pip", "install", "boto3", "loguru", "requests", "--target", str(package_dir)], check=True)

    # Copy main.py and btry library
    shutil.copy("main.py", package_dir)
    shutil.copytree("src/btry", package_dir / "btry")

    # Create zip file
    shutil.make_archive(zip_file.stem, 'zip', package_dir)

    # Clean up package directory
    shutil.rmtree(package_dir)
    print(f"Deployment package created: {zip_file}")

if __name__ == "__main__":
    create_lambda_package()
