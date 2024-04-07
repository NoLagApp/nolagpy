from setuptools import setup, find_packages

setup(
    name='nolagpy',
    version='0.1',
    packages=find_packages(),
    author='NoLag Systems PTY LTD',
    author_email='tech@nolag.app',
    description='NoLag SDK for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/NoLagApp/nolagpy',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
