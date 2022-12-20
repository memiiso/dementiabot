import os
import pathlib

from setuptools import setup, find_packages

setup_py_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(setup_py_dir)

with open("requirements.txt", "r") as fh:
    requirements = fh.readlines()
    install_requires = [req.strip() for req in requirements if
                        not req.strip().startswith('#') and not req.strip().startswith('http') and req.strip()]
    dependency_links = [req.strip() for req in requirements if req.strip().startswith('http')]

setup(
    name='dementiabot',
    # entry_points={ # @TODO 
    #     'console_scripts': [
    #         'dementiabot = dementiabot:main',
    #     ],
    # },
    version='2.0.11',
    packages=find_packages(),
    author="Memiiso Organization",
    description='Python dementiabot',
    long_description=pathlib.Path(__file__).parent.joinpath("README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    url='https://github.com/memiiso/dementiabot',
    ## TODO  download_url='https://github.com/memiiso/dementiabot/archive/master.zip',
    include_package_data=True,
    license="Apache License 2.0",
    test_suite='tests',
    install_requires=install_requires, # @TODO any better way to do it?
    dependency_links=dependency_links,
    python_requires='>=3',
)
