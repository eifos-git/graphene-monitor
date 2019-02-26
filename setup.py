#!/usr/bin/env python3

from setuptools import setup

VERSION = "0.0.1"

setup(
    name="graphene-monitor",
    version=VERSION,
    description="Monitor for Graphene Blockchains",
    long_description=open("README.md").read(),
    download_url="",
    author="Blockchain B.V.",
    author_email="info@BlockchainProjectsBV.com",
    maintainer="Blockchain B.V.",
    maintainer_email="info@BlockchainProjectsBV.com",
    url="",
    keywords=["graphene", "blockchain", "monitor"],
    packages=["monitor"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Games/Entertainment",
    ],
    # entry_points={"console_scripts": ["monitor = monitor.cli.cli:main"]},
    install_requires=open("requirements.txt").readlines(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    include_package_data=True,
)
