from setuptools import setup, find_packages
setup(name = 'worch-ups',
      version = '0.0',
      description = 'Worch/waf tools and features for working with UPS.',
      author = 'Brett Viren',
      author_email = 'brett.viren@gmail.com',
      license = 'GPLv2',
      url = 'http://github.com/brettviren/worch-ups',
      namespace_packages = ['worch'],
      packages = ['worch','worch.upstools'],
      install_requires = [
          'worch',
          'ups_utils'
      ],
      dependency_links = [
          'http://github.com/brettviren/worch/tarball/proper-install#egg=worch',
          'http://github.com/brettviren/python-ups-utils/tarball/master#egg=ups_utils',
      ]
)
