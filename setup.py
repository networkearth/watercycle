from setuptools import setup, find_packages

setup(
    name="watercycle",
    version="0.0.1",
    author="Marcel Gietzmann-Sanders",
    author_email="marcelsanders96@gmail.com",
    packages=find_packages(include=["watercycle", "watercycle*"]),
    install_requires=[
        "aws-cdk-lib==2.154.1",
        "boto3==1.35.50",
        "click==8.1.7",
    ],
    entry_points={
        "console_scripts": [
            "watercycle = watercycle.cli:cli",
        ]
    },
)
