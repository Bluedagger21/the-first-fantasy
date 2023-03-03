from distutils.core import setup
import py2exe, sys, os

setup(console=[{"script":"main.py",
                "dest_base": "TheFirstFantasy"}],
      zipfile=None,
      options={"py2exe": {
          "dist_dir": "..\dist",
          "bundle_files": 1,
          "compressed": True}
               }
      )
