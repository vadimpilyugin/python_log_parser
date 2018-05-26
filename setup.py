from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='log_parser',
      version='2.0',
      description='Log Parser is a program for analyzing log files',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3.5',
        'Topic :: Text Processing',
      ],
      keywords='log parser',
      url='http://github.com/vadimpilyugin/python_log_parser',
      author='vadimpilyugin',
      author_email='vadimpilyugin@gmail.com',
      license='LGPL',
      packages=['log_parser'],
      scripts=['bin/logparser'],
      install_requires=[
          'flask',
          'pyyaml'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,
      zip_safe=False)
