from distutils.core import setup, Extension

module1 = Extension('gcd_module',
                    sources = ['gcd_module.c'])

setup (name = 'GCD package',
       version = '1.0',
       description = 'This is a package for gcd_module',
       ext_modules = [module1])