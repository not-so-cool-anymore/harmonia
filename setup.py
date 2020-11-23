import setuptools

with open('README.md') as readme:
    long_description = readme.read()

setuptools.setup(
    name='harmonia',
    version='0.0.1',
    author='Ivan Zlatanov',
    author_email='i_zlatanov@protonmail.com',
    description='A lightweight tool that syncs two PostgreSQL databases by creating and rebuilding from their backup.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/not-so-cool-anymore/harmonia/',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0'   
)