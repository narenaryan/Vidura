from setuptools import setup, find_packages
from version import VERSION

with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.readlines()
    install_requires = [r.strip() for r in requirements if r.strip()]


setup(
    name='prompthub',
    version=VERSION,
    description='Prompt Hub SDK.',
    url='https://github.com/DataMini/PromptHub',
    author='lele',
    packages=find_packages(
        include=["prompthub.*", "prompthub"]
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=install_requires,
)
