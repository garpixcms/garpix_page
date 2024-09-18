from setuptools import setup, find_packages
from os import path

here = path.join(path.abspath(path.dirname(__file__)), 'garpix_page')

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='garpix_page',
    version='2.49.0-rc6',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/garpixcms/garpix_page',
    project_urls={
        'Documentation': 'https://docs.garpixcms.ru/packages/garpix_page/',
        'GitHub': 'https://github.com/garpixcms/garpix_page/',
        'Changelog': 'https://github.com/garpixcms/garpix_page/blob/master/CHANGELOG.md/',
    },
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
        'Django >= 1.11, < 5',
        'django-polymorphic-tree-for-garpix-page >= 2.2.2',
        'django-modeltranslation >= 0.16.2',
        'django-multiurl-for-garpix-page >= 1.6.0',
        'djangorestframework >= 3.12.4',
        'garpix_utils >= 1.10.0-rc24',
        'django-tabbed-admin-for-garpixcms >= 1.1.0',
        'model-bakery >= 1.4.0',
        'garpix-admin-lock >= 1.3.2',
        'psycopg2-binary >=2.9.3',
        'celery >= 5.2.7'
    ],
)
