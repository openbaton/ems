#!/usr/bin/env python

from distutils.core import setup

setup(name='ElementManagementSystem',
      version='0.1',
      description='Element Management System. See ETSI NFV',
      author='Fraunhofer FOKUS',
      url='https://github.com/openbaton/',
      install_requires=[
          'stomp.py'
      ],
      packages=[
          'receiver','utils'
      ],
      )
