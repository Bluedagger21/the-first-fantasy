'''
Last changed by: Dale Everett
'''
from distutils.core import setup
import py2exe

setup(console=[{"script":"main.py",
          "dest_base": "TheFirstFantasy"}],
      options={"py2exe": {
          "dist_dir": "..\dist"}
               }
      )
