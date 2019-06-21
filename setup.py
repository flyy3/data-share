import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="data-share",
    version="0.0.1",
    author="Yana",
    author_email="joydanevery@gmail.com",
    description="A blockchain data package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/flyy3/data-share.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
)