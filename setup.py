from setuptools import setup, find_packages

setup(
    name='app',
    version='0.2',
    packages=find_packages(),
    url='',
    license='Apache',
    author='Some One',
    zip_safe=False,
    include_package_data=True,
    install_requires=["flask"],
    author_email='none.of-your@bussiness.org',
    description='Getting into python and providing a nice ui to search my endless collection of music and ebooks'
)
