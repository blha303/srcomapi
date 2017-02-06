from setuptools import setup

with open("srcomapi/.version") as f:
    version = f.read().strip()

setup(
    name='srcomapi',
    version=version,
    packages=['srcomapi'],
    package_data={'': ['.version']},
    include_package_data=True,
    install_requires=[
        'requests'
    ],
)
