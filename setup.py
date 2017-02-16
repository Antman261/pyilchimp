from setuptools import setup


def readme():
    with open('READMErst.txt') as f:
        return f.read()


setup(name='pyilchimp',
      version='0.1.1',
      description='Wrapper library for Mailchimp\'s 3.0 API',
      long_description=readme(),
      classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
      ],
      url='https://github.com/Antman261/pyilchimp',
      author='Anthony Manning-Franklin',
      author_email='anthony.manning.franklin@gmail.com.com',
      license='MIT',
      packages=['pyilchimp'],
      install_requires=[
          'simplejson',
          'requests',
          'six',
      ],
      keywords='API RESTful wrapper Mailchimp EDM',
      include_package_data=True,
      zip_safe=False)
