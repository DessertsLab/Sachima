import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sachima",
    version="2019.1a8",
    author="nocmk2",
    author_email="jianye.zhang@gmail.com",
    description="A package for Data Analyst",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DessertsLab/Sachima",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
