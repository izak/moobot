from setuptools import setup, find_packages

setup(name='upfrontbackuptools',
      version='2',
      description='Upfront Systems\' Backup tools',
      long_description='Includes python and shell scripts used for backup purpos
es',  
      author='Izak Burger',
      author_email='izak@upfrontsystems.co.za',
      url='http://www.upfrontsystems.co.za/Members/izak',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir = {'' : 'src'},
      scripts=('ftpsync.py', 'tarbackup.py'),
      )
