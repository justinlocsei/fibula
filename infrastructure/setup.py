from setuptools import find_packages, setup

setup(
    name='fibula',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click==6.4'
    ],
    entry_points="""
        [console_scripts]
        fib=fibula.cli:cli
    """
)
