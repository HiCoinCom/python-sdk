"""
ChainUp Custody Python SDK Setup
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chainup-custody-sdk",
    version="1.1.0",
    author="ChainUp Custody",
    author_email="support@chainup.com",
    description="ChainUp Custody Python SDK - WaaS and MPC API client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChainUp-Custody/python-sdk",
    packages=find_packages(exclude=["tests", "tests.*", "examples"]),
    package_data={
        "chainup_custody_sdk": ["py.typed"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "pycryptodome>=3.15.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "mypy>=1.0.0",
            "black>=23.0.0",
            "isort>=5.12.0",
            "flake8>=6.0.0",
        ],
        "docs": [
            "sphinx>=6.0.0",
            "sphinx-rtd-theme>=1.2.0",
        ],
    },
    keywords="waas mpc chainup custody wallet blockchain cryptocurrency crypto api sdk",
    project_urls={
        "Documentation": "https://github.com/ChainUp-Custody/python-sdk#readme",
        "Bug Reports": "https://github.com/ChainUp-Custody/python-sdk/issues",
        "Source": "https://github.com/ChainUp-Custody/python-sdk",
    },
)
