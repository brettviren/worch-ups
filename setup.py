from setuptools import setup, find_packages
setup(name = 'worch-ups',
      version = '0.1',
      description = 'Worch/waf tools and features for working with UPS.',
      author = 'Brett Viren',
      author_email = 'brett.viren@gmail.com',
      license = 'GPLv2',
      url = 'http://github.com/brettviren/worch-ups',
      namespace_packages = ['worch'],
      packages = ['worch','worch.upstools'],
      install_requires = [
          'worch >= 1.0',
          'ups_utils >= 0.1'
      ],
      dependency_links = [
          'http://github.com/brettviren/worch/tarball/master#egg=worch-1.0',
          'http://github.com/brettviren/python-ups-utils/tarball/master#egg=ups_utils-0.1',
      ]
)
