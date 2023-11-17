
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

version = '0.1'
setup(name='objstore',
    version='{}'.format(version),
    description='Client/server for storing/retrieving Python data in RAM.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/devincornell/objstore',
    author='Devin J. Cornell',
    author_email='devinj.cornell@gmail.com',
    license='MIT',
    packages=find_packages(include=['objstore', 'objstore.*']),
    install_requires=['fastapi', 'unicorn'],
    zip_safe=False,
    download_url='https://github.com/devincornell/objstore/archive/v{}.tar.gz'.format(version)
)


