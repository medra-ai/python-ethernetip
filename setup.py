import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

package_name = 'ethernetip'
description = 'Basic EtherNet/IP scanner'
readme = open('README.md').read()
requirements = ['dpkt']

# PyPI Readme
long_description = open('README.md').read()

# Pull in the package
package = __import__(package_name)
package_version = package.__version__
if "bdist_msi" in sys.argv:
    # The MSI build target does not support a 4 digit version, e.g. '1.2.3.4'
    # therefore we remove the last digit.
    package_version, _, _ = package_version.rpartition('.')

setup(name=package_name,
      version=package_version,
      author=package.__author__,
      author_email=package.__author_email__,
      url=package.__url__,
      description=description,
      long_description=long_description,
      packages=['ethernetip'],
      install_requires=requirements,
      license='MIT',
      zip_safe=False,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: English',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
      ])
