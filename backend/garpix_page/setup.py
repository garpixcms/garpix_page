from setuptools import setup, find_packages
from os import path

here = path.join(path.abspath(path.dirname(__file__)), 'garpix_page')

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='garpix_page',
    version='2.13.0',
    description='',
    long_description=long_description,
    url='https://github.com/garpixcms/garpix_page',
    author='Garpix LTD',
    author_email='info@garpix.com',
    license='MIT',
    packages=find_packages(exclude=['testproject', 'testproject.*']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Django >= 1.11',
        'django-polymorphic-tree-for-garpix-page >= 2.0.1',
        'django-modeltranslation >= 0.16.2',
        'django-multiurl >= 1.4.0',
        'djangorestframework >= 3.12.4',
        'garpix_utils >= 1.4.0',
        'django-tabbed-admin >= 1.0.4',
        'model-bakery >= 1.4.0'
    ],
)
