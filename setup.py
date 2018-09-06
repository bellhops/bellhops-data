import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bellhops_data",
    version="0.0.1",
    author=["Abraar Ahmed", "Naveen Lekkalapudi"],
    author_email=["abraar@getbellhops.com", "naveen.lekkalapudi@getbellhops.com"],
    description="Shared python library for data science and engineering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bellhops/bellhops-data",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
    ],
    install_requires=[
            'pandas==0.22.0',
            'numpy==1.14.5',
            'psycopg2==2.7.5',
            'sqlalchemy==1.1.10'
      ]
)
