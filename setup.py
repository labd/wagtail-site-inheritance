import re

from setuptools import find_packages, setup

docs_require = ["sphinx>=1.4.0"]

tests_require = [
    "coverage[toml]==5.2.1",
    "factory-boy==3.2.0",
    "freezegun==1.1.0",
    "pytest==6.2.4",
    "pytest-django==4.4.0",
    "pytest-cov==2.12.1",
    "wagtail-factories==2.0.1",
    "mock==4.0.3",
    # Linting
    "isort[pyproject]==4.3.21",
    "flake8==3.7.9",
    "flake8-blind-except==0.1.1",
    "flake8-debugger==3.1.0"
]

with open("README.md") as fh:
    long_description = re.sub(
        "<!-- start-no-pypi -->.*<!-- end-no-pypi -->\n",
        "",
        fh.read(),
        flags=re.M | re.S,
    )


setup(
    name="wagtail-site-inheritance",
    version="1.0.0",
    description="Site Inheritance for Wagtail",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/labd/wagtail-site-inheritance",
    author="Lab Digital",
    author_email="opensource@labdigital.nl",
    install_requires=[
        "Django>=2.2",
        "wagtail>=2.16,<4.0"
    ],
    tests_require=tests_require,
    extras_require={"docs": docs_require, "test": tests_require},
    entry_points={},
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 2",
        "Framework :: Wagtail :: 3",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    zip_safe=False,
)
