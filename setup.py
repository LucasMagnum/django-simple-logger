import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-simple-logger',
    version='0.0.3',
    packages=['simplelogger'],
    include_package_data=True,
    license='BSD License',
    description='An easy way to you record yours system logging messages and request exceptions.',
    long_description=README,
    url='https://github.com/LucasMagnum/django-simple-logger',
    author='Lucas Magnum Lopes Oliveira',
    author_email='contato@lucasmagnum.com.br',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)