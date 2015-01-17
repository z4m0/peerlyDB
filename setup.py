#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="peerlyDB",
    version="0.1.0",
    description="PeerlyDB is a database based on Kademlia",
    author="Marti Zamora",
    license="MIT",
    url="https://github.com/z4m0/peerlyDB",
    packages=find_packages(),
    requires=["twisted", "rpcudp"],
    install_requires=['twisted>=14.0', "rpcudp>=1.0"]
)
