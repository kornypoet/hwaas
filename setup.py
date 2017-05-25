import os
from setuptools import setup, find_packages

def get_version():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, 'hwaas/version.py')) as f:
        locals = {}
        exec(f.read(), locals)
        return locals['__version__']
    raise RuntimeError('No version info found.')

setup(
    name='hwaas',
    version=get_version(),
    url='https://github.com/kornypoet/hwaas',
    author='Travis Dempsey',
    author_email='dempsey.travis@gmail.com',
    description='Hello World as a Service',
    packages=find_packages(exclude=['tests']),
    install_requires=['rq'],
    entry_points={
        'console_scripts': [
            'hwaas = hwaas:main',
        ]
    }
)
