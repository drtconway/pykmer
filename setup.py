from setuptools import setup

setup(name='pykmer',
        version='0.1',
        description='A pure python k-mer sequence analysis toolkit',
        url='http://github.com/drtconway/pykmer',
        author='Tom Conway',
        author_email='tconway@au1.ibm.com',
        license='Apache2',
        packages=['pykmer'],
        tests_require=['pytest'],
        test_suite='tests',
        zip_safe=False)
