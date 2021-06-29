from setuptools import setup, find_packages

from anobbs_core import AppConstant

setup(
    name=AppConstant.NAME,
    version=AppConstant.VERSION,
    packages=find_packages(),
    description=AppConstant.DESC,
    url=AppConstant.URL,
    author=AppConstant.AUTHOR_NAME,
    author_email=AppConstant.AUTHOR_EMAIL,
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        # Core
        "click",
        "pyyaml",
        "requests",
        "treelib",
        "pymongo",

        # Http Module
        "flask",
        "flask-restful",
        "flask-cors",
    ],
    entry_points={
        "console_scripts": [],
    },
)
