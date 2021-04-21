from setuptools import setup

with open("srcomapi/.version") as f:
    version = f.read().strip()

with open("README.md") as f:
    desc = f.read()

setup(
    name='srcomapi',
    version=version,
    author="blha303",
    author_email="alyssa.dev.smith+srcomapi@gmail.com",
    description="A Python 3 implementation of the speedrun.com REST API",
    long_description=desc,
    long_description_content_type="text/markdown",
    url="https://github.com/blha303/srcomapi",
    project_urls={
        "Bug tracker": "https://github.com/blha303/srcomapi/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.0",
    packages=['srcomapi'],
    package_data={'': ['.version']},
    include_package_data=True,
    install_requires=[
        'requests'
    ],
)
