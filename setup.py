from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="sachima",
    version="2020.8.20.1",
    author="nocmk2",
    author_email="jianye.zhang@gmail.com",
    description="Better data analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DessertsLab/Sachima",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "aenum",
        "click",
        # "pandas",
        "Flask",
        # "nameko",
        "redis",
        # "cython >= 0.29.6",
        # "thriftpy >= 0.3.9",
        # "impyla == 0.16.2",
        # "pymysql",
        # "SQLAlchemy",
        # "tqdm"
    ],
    include_package_data=True,
    package_data={"": ["*.css"], "example":["*.csv"]},
    # scripts=["sachima/bin/sachima"],
    entry_points={"console_scripts": ["sachima = sachima.cli:sachima"]},
)
