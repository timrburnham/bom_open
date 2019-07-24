from setuptools import setup

setup(
    name='bom_open',
    version='0.4',
    packages=['bom_open',],
    python_requires='>=3.4',
    install_requires=['chardet'],
    author='Tim Burnham',
    author_email='timrburnham@gmail.com',
    url='https://github.com/timrburnham/bom_open',
    description='Context manager to open encoded text file or stdin/stdout',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='unlicense.org',
)
