from setuptools import setup, find_packages


setup(name='dictionary',
    version='0.1',
    url='https://github.com/ipicspro/dictionary',
    license='MIT',
    author='IS',
    author_email='info@ecommaker.com',
    description='Dictionary',
    #packages=find_packages(exclude=['tests']),
    packages=['dictionary'],
    long_description=open('README.md').read(),
    zip_safe=False,
    setup_requires=['nose'],
#   dependency_links=['emoji'],
    install_requires=['emoji'],
    test_suite='nose.collector')

