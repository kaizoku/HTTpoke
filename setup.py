#!/usr/bin/env python

from setuptools import setup

setup(name		    = 'httpoke',
      version		= '0.1',
      description	= 'Tests the given webserver for enabled HTTP methods.',
      author		= 'kaizoku',
      author_email	= 'kaizoku@phear.cc',
      py_modules	= ['httpoke'],
      license		= 'WTF',
      url		    = 'http://github.com/kaizoku/httpoke',
      entry_points  = {
          'console_scripts': ['httpoke = httpoke.httpoke:main']
          },
)
