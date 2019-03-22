from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="sachima",
    version="2019.3.13",
    author="nocmk2",
    author_email="jianye.zhang@gmail.com",
    description="A package for Data Analyst",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/DessertsLab/Sachima",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "aenum >= 2.1.2",
        "pandas >= 0.24.2",
        "Flask >= 1.0.2",
        "nameko >=2.12.0",
        "redis >= 3.2.1",
        "cython >= 0.29.6",
        "thriftpy >= 0.3.9",
        "impyla == 0.15a1",
        "pymysql >= 0.9.3",
        "SQLAlchemy >= 1.3.1",
    ],
    include_package_data=True,
    package_data={"": ["*.css"]},
)
