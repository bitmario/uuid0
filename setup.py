from setuptools import setup

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Framework :: Django",
    "Topic :: Software Development :: Libraries :: Python Modules",
]

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='uuid0',
      version='0.1.2',
      description='A library to make better timestamped UUIDs for databases and web apps',
      long_description=readme(),
      url='https://github.com/oaclaf/uuid0',
      author='oaclaf',
      author_email='oaclafm@gmail.com',
      license='MIT',
	  classifiers=CLASSIFIERS,
      packages=['uuid0', 'uuid0.django'],
      install_requires=['pybase62'],
      zip_safe=False)
