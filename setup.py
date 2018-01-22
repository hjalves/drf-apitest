#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='drf-apitests',
    version='0.1a4',
    description='API testing tools for Django REST Framework',
    url='https://github.com/hjalves/drf-apitests',
    author='Humberto Alves',
    author_email='hjalves@live.com',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='drf api testing',
    packages=find_packages(),
    install_requires=[
        'Django>=1.9',
        'djangorestframework',
        'djangorestframework-jwt',
        'PyYAML'
    ],
    #include_package_data=True,
    zip_safe=False,
    tests_require=['pytest'],
)
