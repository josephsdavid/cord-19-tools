import setuptools


def readme():
    with open("README.md") as readme_file:
        return readme_file.read()


setuptools.setup(
    name="cord-19-tools",
    version="0.3.2",
    description="CORD 19 tools and utilities",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/josephsdavid/cord-19-tools",
    maintainer="David Josephs",
    maintainer_email="josephsd@smu.edu",
    # $ packages = setuptools.find_packages(exclude = [
    #    "*weights*", "*viz*", "*data*"
    # ]),
    packages=["cotools"],
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["xmltodict"],
)
