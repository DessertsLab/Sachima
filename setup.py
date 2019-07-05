from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="sachima",
    version="2019.7.3",
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
        # "aenum",
        # "pandas",
        # "Flask",
        # "nameko",
        # "redis",
        # "cython >= 0.29.6",
        # "thriftpy >= 0.3.9",
        # "impyla == 0.15a1",
        # "pymysql",
        # "SQLAlchemy",
    ],
    include_package_data=True,
    package_data={"": ["*.css"]},
)
