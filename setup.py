from setuptools import setup, find_packages

from anonymous_bbs import AppConstant

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
        "click",
        "pyyaml",
        "requests",
        "treelib",
    ],
    entry_points={
        "console_scripts": [f'anobbs=anonymous_bbs.app:cli']
    },
)
