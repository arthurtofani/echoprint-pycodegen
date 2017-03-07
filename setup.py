from setuptools import setup, find_packages

import imp

#version = imp.load_source('librosa.version', 'librosa/version.py')

setup(
    name='echoprint-pycodegen',
    version='1.0',
    description='Python version of echoprint-codegen',
    author='Arthur Tofani',
    author_email='arthur.tofani@usp.br',
    url='http://github.com/arthurtofani/echoprint-pycodegen',
    download_url='http://github.com/arthurtofani/echoprint-pycodegen/releases',
    packages=find_packages(),
    package_data={'': ['example_data/*']},
    long_description="""A python module for audio and music processing.""",
    classifiers=[
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Sound/Audio :: Analysis",
    ],
    keywords='audio music sound',
    license='ISC',
    install_requires=[
        'audioread >= 2.0.0',
        'numpy >= 1.8.0',
        'scipy >= 0.13.0',
        'spectrum >= 0.6.1',
    ]
)
