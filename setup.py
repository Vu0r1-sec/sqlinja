import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sqlinja",
    version="0.2.0",
    author="V0ur1",
    author_email="jb.astarie@ordanchesolutions.fr",
    description="SqlInja  is a Python library designed to automate exploitation of SQL blind injection (time-based or boolean-based).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vu0r1-sec/sqlinja",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)