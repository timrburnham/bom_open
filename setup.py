from distutils.core import setup

setup(
    name='bom_open',
    version='0.1.2',
    packages=['bom_open',],
    author='Tim Burnham',
    author_email='timrburnham@gmail.com',
    url='https://github.com/timrburnham/bom_open',
    description='open() alternative which respects Unicode BOM',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='unlicense.org',
)
