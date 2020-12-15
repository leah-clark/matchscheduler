from setuptools import setup

setup(
    name='server',
    packages=['server', 'data_processing'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)