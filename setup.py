# DON'T IMPORT ANY MODULE FROM THE PACKAGE !
import setuptools


with open("README.md", "r") as file:
    LONG_DESCRIPTION = file.read()


NAME = "pyrustic"
VERSION = "0.0.8"
AUTHOR = "Pyrustic Evangelist"
EMAIL = "pyrustic@protonmail.com"
DESCRIPTION = "Lightweight framework and software suite to help develop, package, and publish Python desktop applications"
URL = "https://github.com/pyrustic/pyrustic"


setuptools.setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=["rustiql", "jupitest", "hubway"],
    entry_points={
        "console_scripts": [
            "pyrustic = pyrustic.manager.main:main",
        ],
    },
    python_requires='>=3.5',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
