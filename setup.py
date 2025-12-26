"""
ChainUp Custody Python SDK Setup
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chainup-custody-sdk",
    version="1.0.0",
    author="ChainUp Custody",
    author_email="support@chainup.com",
    description="ChainUp Custody Python SDK - WaaS and MPC API client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChainUp-Custody/python-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "pycryptodome>=3.15.0",
    ],
    keywords="waas mpc chainup custody wallet blockchain cryptocurrency",
)
