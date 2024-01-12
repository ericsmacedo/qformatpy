from setuptools import setup, find_packages

setup(
    name='qformatpy',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    author='Eric Macedo',
    author_email='ericsmacedo@gmail.com',
    description='A Python library for Q format representation and overflow handling.',
    long_description=open('README.md').read(),
    url='https://github.com/ericsmacedo/qformatpy',
    license='MIT',
)
