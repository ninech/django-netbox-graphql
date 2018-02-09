import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-netbox-graphql',
    version='0.0.4',
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Django module which provides a GraphQL API for Netbox (For django 1.11)',
    long_description=README,
    url='https://github.com/ninech/django-netbox-graphql',
    author='nine.ch',
    author_email='dev@nine.ch',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    keywords='django netbox graphql python',
    install_requires=[
        'graphene-django==1.3',
        'graphene==1.4',
        'graphql-core==1.1',
    ],
    extras_require={
        'test': [
            'snapshottest',
            'factory_boy'
        ]
    },
)
