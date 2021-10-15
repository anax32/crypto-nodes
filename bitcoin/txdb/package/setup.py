import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="btctx",
    version="0.0.1",
    author="ed",
    author_email="ed@bayis.co.uk",
    description="Bitcoin Transaction Database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bayinfosys/btctxdb",
    packages=[
        "btctx",
        "btctx.log",
        "btctx.persist",
        "btctx.query",
        "btctx.rpc",
    ],
    package_data={
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "boto3",
        "pymongo",
        "requests"
    ],
    extras_require={
        "tests": ["pytest", "mock"]
    }
)
