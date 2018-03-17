from distutils.core import setup

setup(
    name='bom_open',
    version='0.1',
    packages=['bom_open',],
    author='Tim Burnham',
    author_email='timrburnham@gmail.com',
    description='open() alternative which respects BOM from file',
    long_description=open('README.md').read(),
    license='unlicense.org',
)
