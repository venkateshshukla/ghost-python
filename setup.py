from setuptools import setup, find_packages
setup(
    name="ghost_api",
    version="0.1",
    packages=find_packages(),
    scripts=['ghost.py'],
    install_requires=['requests>=2.4.2'],
    author="Venkatesh Shukla",
    author_email="venkatesh.shukla.eee11@iitbhu.ac.in",
    description="Package to interact with Ghost Backend REST API",
    keywords="hello world example examples",
    url="https://github.com/venkateshshukla/ghost-python"
)
