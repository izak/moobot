from setuptools import setup, find_packages

setup(name='moobot',
      version='1',
      description='An extensible IRC bot written in python',
      long_description='An extensible IRC bot, written in python',  
      author='Izak Burger',
      author_email='isburger@gmail.com',
      url='http://github.com/izak',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir = {'' : 'src'},
      entry_points = {
          'console_scripts': [
              'moobot = moobot.bot:main',
          ]
      },
      )
