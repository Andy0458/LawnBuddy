from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='lawnbuddy',
    version='0.1.0',
    description='Software for Lawnbuddy Autonomous Mower to be run on RaspberryPi',
    long_description=readme,
    author='Andrew Brown',
    author_email='andrew@ajbrown.me',
    url='https://github.com/Andy0458/LawnBuddy',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)