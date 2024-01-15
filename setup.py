from setuptools import setup, find_packages

setup(
    name='kdna',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'kdna = kdna.commands.server:list',
        ],
    },
)