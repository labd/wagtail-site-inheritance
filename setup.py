import glob
import os.path
import subprocess

from setuptools import Command, find_packages, setup
from setuptools.command.sdist import sdist as _sdist

docs_require = ["sphinx>=1.4.0"]

tests_require = [
    "coverage>=3.7.0",
    "pytest>=3.6",
    "pytest-django==3.5.1",
    "wagtail-factories==2.0.0",
    # Linting
    "isort==4.2.5",
    "flake8>=3.6.0",
    "flake8-blind-except==0.1.1",
    "flake8-debugger==1.4.0",
]

# Custom setuptools commands
class sdist(_sdist):
    def run(self):
        self.run_command("prepare")
        _sdist.run(self)


try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
except ImportError:
    bdist_wheel = None
else:

    class bdist_wheel(_bdist_wheel):
        def run(self):
            self.run_command("prepare")
            _bdist_wheel.run(self)


class prepare(Command):
    user_options = []

    def run(self):
        self.compile_po_files()

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def compile_po_files(self):
        for filename in glob.glob("**/*.po", recursive=True):
            base, __ = os.path.splitext(filename)
            target = "%s.mo" % base
            subprocess.run(["msgfmt", filename, "-o%s" % target])


setup(
    name="wagtail-site-inheritance",
    version="0.0.1",
    description="Something I made",
    long_description=open("README.rst", "r").read(),
    url="https://github.com/labd/wagtail-site-inheritance",
    author="Michael van Tellingen",
    author_email="",
    install_requires=["Django>=2.2", "wagtail>=2.6"],
    tests_require=tests_require,
    extras_require={"docs": docs_require, "test": tests_require},
    use_scm_version=True,
    entry_points={},
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Wagtail :: 2",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    cmdclass={"sdist": sdist, "bdist_wheel": bdist_wheel, "prepare": prepare},
    zip_safe=False,
)
