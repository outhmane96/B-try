from setuptools import setup, find_packages

# Read dependencies from requirements.txt
def parse_requirements(file):
    with open(file, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="btry",
    version="0.1.0",
    author="B-Try Team",
    author_email="",
    description="Python library that will work as a helper for the B-Try project.",
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=parse_requirements("requirements.txt"),
    tests_require=[
        'testfixtures',
        'pytest'
    ],
    test_suite="tests",
    license='Proprietary',
    classifiers=[
        "Programming Language :: Python :: 3.6",
    ]
)