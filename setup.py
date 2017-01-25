from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        pytest.main(self.test_args)

setup(name='pykmer',
        version='0.2.1',
        description='A pure python k-mer sequence analysis toolkit',
        url='http://github.com/drtconway/pykmer',
        author='Tom Conway',
        author_email='tconway@au1.ibm.com',
        license='Apache2',
        keywords='bioinformatics genomics pathogenomics',
        packages=find_packages(),
        install_requires=['docopt'],
        tests_require=['pytest'],
        cmdclass = {'test': PyTest},
        zip_safe=False)
