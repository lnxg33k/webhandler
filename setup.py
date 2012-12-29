#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name="webhandler",
    packages=find_packages(),
    description="A handler for PHP system functions & also an alternative 'netcat' handler",
    long_description="""WebHandler tries to simulate a 'Linux bash prompt' to handle and process:
    - PHP program execution functions (e.g. `system`, `passthru`, `exec`, etc)
    - Bind shell connections (e.g. `nc <ip> <port>`)
    - Reserve shell connections (e.g. `nc -lvvp 1234`)
    """,
    author=["lnxg33k", "g0tmi1k"],
    author_email=['ahmedelantry@gmail.com', 'have.you.g0tmi1k@gmail.com'],
    url="https://github.com/lnxg33k/webhandler/",
    download_url="https://github.com/lnxg33k/webhandler/archive/master.zip",
    platforms=['any'],

    license="GPLv3+",

    scripts=['webhandler.py'],

    classifiers=[
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python'],
)
