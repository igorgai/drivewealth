"""
setup.py file for building components.
Nothing in this file should need to be edited, please see accompanying
package.json file if you need to adjust metadata about this package.
Borrowed almost wholesale from Armstrong http://armstrongcms.org/
"""

from setuptools import setup, find_packages
import json
import sys

info = json.load(open("package.json"))

version = '0.0.1.dev0'


def convert_to_str(d):
    """
    Recursively convert all values in a dictionary to strings
    This is required because setup() does not like unicode in
    the values it is supplied.
    """
    d2 = {}
    for k, v in list(d.items()):
        k = str(k)
        if type(v) in [list, tuple]:
            d2[k] = [str(a) for a in v]
        elif type(v) is dict:
            d2[k] = convert_to_str(v)
        else:
            d2[k] = str(v)
    return d2

info = convert_to_str(info)

setup_kwargs = {
    "author": "The Motley Fool",
    "author_email": "github@fool.com",
    "url": "https://github.com/themotleyfool/%s/" % info["name"],
    "packages": find_packages(),
    "include_package_data": True,
    "version": version,
    "classifiers": [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
}

setup_kwargs.update(info)

needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)

if needs_pytest:
    setup_kwargs["setup_requires"].append("pytest-runner==2.7.0")

setup(**setup_kwargs)
