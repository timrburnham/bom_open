from setuptools import setup

setup(
    name='bom_open',
    version='0.3.2',
    packages=['bom_open',],
    install_requires=['chardet'],
    setup_requires=['setuptools>=38.6.0'],
    author='Tim Burnham',
    author_email='timrburnham@gmail.com',
    url='https://github.com/timrburnham/bom_open',
    description='Python file/stdio context manager which detects encoding',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='unlicense.org',
)
