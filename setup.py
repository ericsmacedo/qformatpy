from setuptools import setup, find_packages

setup(
    name='qformatpy',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'numpy',
    ],
    author='Eric Macedo',
    author_email='ericsmacedo@gmail.com',
    description='A Python library for Q format representation and overflow handling.',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    url='https://github.com/ericsmacedo/qformatpy',
    license='MIT',
)
