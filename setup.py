from setuptools import setup

setup(name='uuid0',
      version='0.1.0',
      description='A library to make better UUIDs for databases and web apps',
      url='http://github.com/oaclafm/uuid0',
      author='oaclafm',
      author_email='oaclafm@gmail.com',
      license='MIT',
      packages=['uuid0', 'uuid0.django'],
      requires=['pybase62'],
      zip_safe=False)
