from setuptools import find_packages, setup

setup(
    name='fibula',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'boto==2.39.0',
        'click==6.4',
        'python-digitalocean==1.8'
    ],
    entry_points="""
        [console_scripts]
        fib=fibula.cli:cli
    """
)
