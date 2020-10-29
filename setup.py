# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in erpnext_pos_coupon/__init__.py
from erpnext_pos_coupon import __version__ as version

setup(
	name='erpnext_pos_coupon',
	version=version,
	description='Applying Coupon In POS',
	author='Tridz',
	author_email='info@tridz.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
